"""Hosted uploads and durable worker queue on the existing PostgreSQL schema (SPEC §11.1).

Project row locks serialize replay checks. A worker holds a PostgreSQL session advisory lock
for its run: another worker skips it, and a crashed worker releases it automatically. Completed
artifacts are published before committing the final status, so a retry can finish persistence
without asking the models again. Raw model calls use DbCallLog's independent transactions.
"""

import hashlib
import json
import os
import tempfile
from collections.abc import Callable
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from sqlalchemy import Engine, select, text
from sqlalchemy.orm import Session

from notinspec import __version__
from notinspec.config import ConfigError, load_config
from notinspec.db import models, save
from notinspec.db.importer import _artifacts
from notinspec.ingestion import Ingestion, plan_ingestion
from notinspec.oidc import ForbiddenUpload, WorkflowIdentity, authorize
from notinspec.upload import extract_archive, process_upload

MAX_UPLOAD_BYTES = 25 * 1024 * 1024
ClaimsRunner = Callable[[Ingestion, Path, str, tuple[str, ...]], dict[str, Any]]


class ReplayConflict(ValueError):
    """The same GitHub run and attempt sent different inputs; HTTP 409."""


class UploadTooLarge(ValueError):
    """The archive exceeds the service's or project's limit; HTTP 413."""


def upload_meta(value: str) -> dict[str, Any]:
    """Only display/baseline metadata comes from the client, never commit identity."""
    import re

    try:
        doc = json.loads(value)
    except ValueError as error:
        raise ConfigError("meta must be JSON") from error
    if (
        not isinstance(doc, dict)
        or set(doc) != {"schema_version", "head_sha", "base_sha"}
        or type(doc["schema_version"]) is not int
        or doc["schema_version"] != 0
    ):
        raise ConfigError("meta needs schema_version 0, head_sha and base_sha")
    for name in ("head_sha", "base_sha"):
        if doc[name] is not None and (
            not isinstance(doc[name], str) or not re.fullmatch(r"[0-9a-f]{40}", doc[name])
        ):
            raise ConfigError(f"meta {name} must be null or a 40-character lowercase SHA")
    return doc


class HostedService:
    def __init__(self, engine: Engine, uploads_dir: Path, runs_dir: Path, public_url: str) -> None:
        self.engine = engine
        self.uploads_dir = uploads_dir
        self.runs_dir = runs_dir
        self.public_url = public_url.rstrip("/")

    def _project(self, session: Session, identity: WorkflowIdentity) -> models.Project:
        project = session.scalar(
            select(models.Project)
            .where(models.Project.repository_id == identity.repository_id)
            .with_for_update()
        )
        if project is None:
            raise ForbiddenUpload("repository is not registered")
        authorize(
            identity,
            repository_id=project.repository_id,
            default_branch=project.default_branch,
            workflow_path=project.workflow_path,
        )
        return project

    def accept(
        self, identity: WorkflowIdentity, archive: bytes, meta: dict[str, Any]
    ) -> tuple[dict[str, str], bool]:
        if len(archive) > MAX_UPLOAD_BYTES:
            raise UploadTooLarge("archive is larger than 25 MB")
        digest = hashlib.sha256(archive).hexdigest()
        with Session(self.engine) as session, session.begin():
            project = self._project(session, identity)
            if project.max_upload_bytes is not None and len(archive) > project.max_upload_bytes:
                raise UploadTooLarge("archive exceeds the registered project's size limit")
            previous = session.scalar(
                select(models.Upload).where(
                    models.Upload.project_id == project.id,
                    models.Upload.github_run_id == identity.github_run_id,
                    models.Upload.github_run_attempt == identity.github_run_attempt,
                )
            )
            if previous is not None:
                if previous.archive_sha256 != digest:
                    raise ReplayConflict(
                        "this GitHub run attempt already uploaded different inputs"
                    )
                run = session.get(models.Run, previous.run_id)
                assert run is not None
                return self._accepted(run.public_id), False
            self.uploads_dir.mkdir(parents=True, exist_ok=True)
            with tempfile.NamedTemporaryFile(
                dir=self.uploads_dir, suffix=".tmp", delete=False
            ) as f:
                temporary = Path(f.name)
                f.write(archive)
            try:
                # Validate selection before accepting a run; never execute uploaded code.
                with tempfile.TemporaryDirectory(prefix="notinspec-check-") as root:
                    folder = Path(root)
                    extract_archive(temporary, folder)
                    config = load_config(folder / "notinspec.yaml")
                    plan_ingestion(config, output=folder / ".notinspec-output")
                os.replace(temporary, self.uploads_dir / f"{digest}.tar.gz")
            finally:
                temporary.unlink(missing_ok=True)
            public_id = (
                f"gh-{identity.repository_id}-{identity.github_run_id}"
                f"-{identity.github_run_attempt}"
            )
            run = models.Run(
                public_id=public_id,
                project_id=project.id,
                trigger=identity.event,
                commit_sha=identity.sha,
                ref=identity.ref,
                pr_number=identity.pr_number,
                status="queued",
                tool_version=__version__,
            )
            session.add(run)
            session.flush()
            session.add(
                models.Upload(
                    run_id=run.id,
                    project_id=project.id,
                    repository_id=identity.repository_id,
                    github_run_id=identity.github_run_id,
                    github_run_attempt=identity.github_run_attempt,
                    event_name=identity.event,
                    ref=identity.ref,
                    sha=identity.sha,
                    workflow_ref=identity.workflow_ref,
                    pr_number=identity.pr_number,
                    head_sha=meta["head_sha"],
                    base_sha=meta["base_sha"],
                    archive_sha256=digest,
                    archive_bytes=len(archive),
                    claims=identity.claims,
                )
            )
            return self._accepted(public_id), True

    def _accepted(self, public_id: str) -> dict[str, str]:
        return {
            "run_id": public_id,
            "status_url": f"{self.public_url}/api/runs/{public_id}",
            "web_url": f"{self.public_url}/#/runs/{public_id}",
        }

    def close_pr(self, identity: WorkflowIdentity) -> None:
        if identity.event != "pull_request" or identity.pr_number is None:
            raise ForbiddenUpload("pr-closed requires a pull_request token")
        with Session(self.engine) as session, session.begin():
            project = self._project(session, identity)
            previous = session.scalar(
                select(models.PrClosed.id).where(
                    models.PrClosed.project_id == project.id,
                    models.PrClosed.github_run_id == identity.github_run_id,
                    models.PrClosed.pr_number == identity.pr_number,
                )
            )
            if previous is None:
                session.add(
                    models.PrClosed(
                        project_id=project.id,
                        pr_number=identity.pr_number,
                        github_run_id=identity.github_run_id,
                        claims=identity.claims,
                    )
                )

    def status(self, public_id: str) -> dict[str, Any] | None:
        with Session(self.engine) as session:
            run = session.scalar(select(models.Run).where(models.Run.public_id == public_id))
            if run is None:
                return None
            return {
                "schema_version": 0,
                "run_id": public_id,
                "status": run.status,
                "verdict": run.verdict,
                "comment_md": run.comment_md,
                "error": run.error,
                "error_kind": run.error_kind,
                "web_url": f"{self.public_url}/#/runs/{public_id}",
            }

    def work_one(self, claims_runner: ClaimsRunner | None = None) -> str | None:
        with Session(self.engine) as session:
            candidates = list(
                session.scalars(
                    select(models.Run.id)
                    .where(
                        models.Run.status.in_(("queued", "running")),
                        models.Run.id.in_(select(models.Upload.run_id)),
                    )
                    .order_by(models.Run.id)
                    .limit(100)
                )
            )
        for run_id in candidates:
            # A session lock is released on process death, unlike a permanent running flag.
            with self.engine.connect() as connection:
                key = (0x4E49 << 48) + run_id
                locked = connection.scalar(text("SELECT pg_try_advisory_lock(:key)"), {"key": key})
                connection.commit()
                if not locked:
                    continue
                try:
                    result = self._work(run_id, claims_runner)
                    if result is not None:
                        return result
                finally:
                    connection.execute(text("SELECT pg_advisory_unlock(:key)"), {"key": key})
                    connection.commit()
        return None

    def _work(self, run_id: int, claims_runner: ClaimsRunner | None) -> str | None:
        with Session(self.engine) as session, session.begin():
            run = session.get(models.Run, run_id, with_for_update=True)
            assert run is not None
            if run.status not in ("queued", "running"):
                return None
            upload = session.scalar(select(models.Upload).where(models.Upload.run_id == run.id))
            project = session.get(models.Project, run.project_id)
            assert upload is not None and project is not None
            public_id, sha, slug = run.public_id, run.commit_sha, project.slug
            allowed_models = tuple(project.allowed_models)
            archive = self.uploads_dir / f"{upload.archive_sha256}.tar.gz"
            run.status, run.started_at = "running", datetime.now(UTC)
        self.runs_dir.mkdir(parents=True, exist_ok=True)
        folder = self.runs_dir / public_id
        if not (folder / "run.json").is_file():
            with tempfile.TemporaryDirectory(prefix=".work-", dir=self.runs_dir) as temporary:
                result = process_upload(
                    archive,
                    Path(temporary),
                    public_id,
                    project=slug,
                    commit=sha,
                    web_url=f"{self.public_url}/#/runs/{public_id}",
                    claims_runner=(
                        lambda ingestion, out: claims_runner(
                            ingestion, out, public_id, allowed_models
                        )
                    )
                    if claims_runner is not None
                    else None,
                )
                if result.status == "error":
                    with Session(self.engine) as session, session.begin():
                        run = session.get(models.Run, run_id)
                        assert run is not None
                        run.status, run.error, run.error_kind = (
                            "error",
                            result.error,
                            result.error_kind,
                        )
                        run.comment_md, run.finished_at = result.comment_md, datetime.now(UTC)
                    return public_id
                (Path(temporary) / public_id / "comment.md").write_text(
                    result.comment_md, encoding="utf-8"
                )
                os.replace(Path(temporary) / public_id, folder)
        # A crash between publication and this transaction resumes here without model calls.
        with Session(self.engine) as session, session.begin():
            run = session.get(models.Run, run_id)
            project = session.get(models.Project, run.project_id) if run is not None else None
            assert run is not None and project is not None
            ingestion = json.loads((folder / "ingestion.json").read_bytes())
            stored = save.ingestion(session, project, ingestion)
            run.ingestion_id = stored.id
            snapshot = session.get(models.InputSnapshot, stored.snapshot_id)
            upload = session.scalar(select(models.Upload).where(models.Upload.run_id == run.id))
            assert snapshot is not None and upload is not None
            snapshot.archive_sha256, snapshot.archive_bytes = (
                upload.archive_sha256,
                upload.archive_bytes,
            )
            snapshot.archive_path = str(archive)
            if (folder / "claims.json").is_file():
                save.claims(session, run, json.loads((folder / "claims.json").read_bytes()))
            session.add_all(_artifacts(folder, run.id))
            run.status, run.finished_at = "done", datetime.now(UTC)
            # Evaluation/golden-set integration is still pending. Ingestion never means pass.
            run.verdict = None
            run.comment_md = (folder / "comment.md").read_text(encoding="utf-8")
        return public_id
