"""Import run folders written before the DB existed (`notinspec demo`, uploads) into the DB.

A folder counts as a run when it has run.json (written last, so the run is complete). Each run
is imported in its own transaction; a run already in the DB (same run ID) is skipped, so the
import can be repeated. Every file of the folder is kept as a `run_artifact`, as written, so
nothing is lost; ingestion.json, claims.json, llm-calls.jsonl and claims-store.jsonl are also
stored as rows.
"""

import hashlib
import json
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any, Literal

from sqlalchemy import Engine, select
from sqlalchemy.orm import Session

from notinspec.db import models, save

_MEDIA_TYPES = {
    ".json": "application/json",
    ".jsonl": "application/jsonl",
    ".md": "text/markdown; charset=utf-8",
    ".html": "text/html; charset=utf-8",
}
_ZERO_COMMIT = "0" * 40


@dataclass(frozen=True)
class Imported:
    folder: str
    status: Literal["imported", "exists", "skipped", "failed"]
    detail: str


def import_runs(engine: Engine, root: Path) -> list[Imported]:
    """Every run folder directly below `root`, in name order."""
    if not root.is_dir():
        raise ValueError(f"not a folder: {root}")
    return [import_run(engine, folder) for folder in sorted(root.iterdir()) if folder.is_dir()]


def import_run(engine: Engine, folder: Path) -> Imported:
    name = folder.name
    run_file = folder / "run.json"
    if not run_file.is_file():
        return Imported(name, "skipped", "no run.json (not a run, or an unfinished one)")
    try:
        doc = _json(run_file)
        with Session(engine) as session, session.begin():
            exists = session.scalar(select(models.Run.id).where(models.Run.public_id == doc["id"]))
            if exists is not None:
                return Imported(name, "exists", f"run {doc['id']} is already in the database")
            detail = _import(session, folder, doc)
    except (OSError, ValueError, KeyError, TypeError) as e:
        return Imported(name, "failed", f"{type(e).__name__}: {e}")
    return Imported(name, "imported", detail)


def _import(session: Session, folder: Path, doc: dict[str, Any]) -> str:
    proj = save.project(session, doc["project"])
    ingestion_file = folder / "ingestion.json"
    ing = save.ingestion(session, proj, _json(ingestion_file)) if ingestion_file.is_file() else None
    results = _json(folder / "results.json") if (folder / "results.json").is_file() else {}

    created = datetime.fromisoformat(doc["created_at"])
    event = results.get("event")
    commit = doc.get("commit") or None
    run = models.Run(
        public_id=doc["id"],
        project_id=proj.id,
        ingestion_id=ing.id if ing is not None else None,
        trigger=event if event in models.UPLOAD_EVENTS else "cli",
        commit_sha=None if commit == _ZERO_COMMIT else commit,
        ref=results.get("ref") or None,
        pr_number=results.get("pr"),
        status="done",  # run.json is written last: the run finished
        comment_md=_text(folder / "comment.md"),
        tool_version=doc.get("tool_version", "unknown"),
        created_at=created,
        finished_at=created,
    )
    session.add(run)
    session.flush()
    session.add_all(
        models.RunStep(
            run_id=run.id,
            position=i,
            step=s["id"],
            label=s["label"],
            status=s["status"],
            detail=s.get("detail"),
        )
        for i, s in enumerate(doc.get("steps", []))
    )

    parts = [f"project {proj.slug}"]
    if ing is not None:
        parts.append("ingestion")
    claims_file = folder / "claims.json"
    if claims_file.is_file():
        parts.append(f"{save.claims(session, run, _json(claims_file))} claims")
    calls_file = folder / "llm-calls.jsonl"
    if calls_file.is_file():
        parts.append(f"{save.llm_calls(session, run, _jsonl(calls_file))} LLM calls")
    store_file = folder / "claims-store.jsonl"
    if store_file.is_file():
        entries = ((e["key"], e["answer"]) for e in _jsonl(store_file))
        parts.append(f"{save.claim_answers(session, entries)} new stored answers")
    artifacts = _artifacts(folder, run.id)
    session.add_all(artifacts)
    parts.append(f"{len(artifacts)} files")
    session.flush()
    return ", ".join(parts)


def _artifacts(folder: Path, run_id: int) -> list[models.RunArtifact]:
    out = []
    for path in sorted(folder.iterdir()):
        if not path.is_file() or path.is_symlink() or path.name.endswith(".tmp"):
            continue
        data = path.read_bytes()
        out.append(
            models.RunArtifact(
                run_id=run_id,
                name=path.name,
                media_type=_MEDIA_TYPES.get(path.suffix, "application/octet-stream"),
                content=data,
                sha256=hashlib.sha256(data).hexdigest(),
            )
        )
    return out


def _json(path: Path) -> Any:
    return json.loads(path.read_bytes())


def _jsonl(path: Path) -> list[Any]:
    """Lines of a JSONL file; a cut-off last line (a crash while appending) is left out."""
    lines = [line for line in path.read_bytes().split(b"\n") if line.strip()]
    out = []
    for number, line in enumerate(lines, 1):
        try:
            out.append(json.loads(line))
        except ValueError:
            if number == len(lines):
                break
            raise ValueError(f"{path.name}:{number}: not JSON") from None
    return out


def _text(path: Path) -> str | None:
    return path.read_text(encoding="utf-8") if path.is_file() else None
