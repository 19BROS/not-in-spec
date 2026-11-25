"""Upload → PostgreSQL queue → core processing → public status, plus crash/replay cases."""

import json
from concurrent.futures import ThreadPoolExecutor
from dataclasses import replace
from pathlib import Path
from threading import Event

import pytest
from fastapi.testclient import TestClient
from sqlalchemy import func, select
from sqlalchemy.orm import Session

from notinspec.db import models, save
from notinspec.db.hosted import HostedService, UploadTooLarge, upload_meta
from notinspec.oidc import ForbiddenUpload, WorkflowIdentity
from notinspec.pack import pack_inputs
from notinspec_api import hosted
from notinspec_api.main import app

META = {"schema_version": 0, "head_sha": "b" * 40, "base_sha": None}


@pytest.fixture
def identity():
    return WorkflowIdentity(
        123,
        456,
        1,
        "pull_request",
        "refs/pull/7/merge",
        "a" * 40,
        "team/repo/.github/workflows/check.yml@refs/pull/7/merge",
        7,
        {"repository_visibility": "public"},
    )


@pytest.fixture
def service(engine, tmp_path):
    with Session(engine) as session, session.begin():
        session.add(
            models.Project(
                slug="test",
                name="Test",
                repository="team/repo",
                repository_id=123,
                default_branch="main",
                workflow_path="team/repo/.github/workflows/check.yml",
            )
        )
    return HostedService(engine, tmp_path / "uploads", tmp_path / "runs", "https://example.org")


@pytest.fixture
def archive(tmp_path):
    root = tmp_path / "input"
    root.mkdir()
    (root / "notinspec.yaml").write_text('project: test\ndocs: {paths: ["docs.md"]}\n')
    (root / "docs.md").write_text("# API\n\nThe timeout is 30 seconds.\n", encoding="utf-8")
    target = tmp_path / "input.tar.gz"
    pack_inputs(root / "notinspec.yaml", target)
    return target.read_bytes()


def count(engine, model):
    with Session(engine) as session:
        return session.scalar(select(func.count()).select_from(model))


def test_api_worker_roundtrip(service, identity, archive):
    app.dependency_overrides[hosted.service] = lambda: service
    app.dependency_overrides[hosted.identity] = lambda: identity
    try:
        with TestClient(app) as client:

            def post(data=archive):
                return client.post(
                    "/uploads",
                    files={"archive": ("input.tar.gz", data), "meta": (None, json.dumps(META))},
                )

            accepted = post()
            assert accepted.status_code == 202
            public_id = accepted.json()["run_id"]
            assert client.get(f"/runs/{public_id}").json()["status"] == "queued"
            assert post().status_code == 200
            assert post(archive + b"different").status_code == 409
            assert service.work_one() == public_id
            result = client.get(f"/runs/{public_id}").json()
            assert (result["status"], result["verdict"], result["error"]) == ("done", None, None)
            assert result["comment_md"] and client.get("/runs/missing").status_code == 404
            assert service.work_one() is None
            assert client.post("/pr-closed").status_code == 202
            assert client.post("/pr-closed").status_code == 202
        assert count(service.engine, models.Upload) == count(service.engine, models.Run) == 1
        assert count(service.engine, models.PrClosed) == 1
        assert count(service.engine, models.Chunk) > 0
        assert count(service.engine, models.RunArtifact) >= 5
        with Session(service.engine) as session:
            run = session.scalar(select(models.Run))
            assert run.commit_sha == identity.sha != META["head_sha"]
    finally:
        app.dependency_overrides.clear()


def test_rejected_upload_never_queues(service, identity, archive):
    with pytest.raises(ForbiddenUpload):
        service.accept(replace(identity, repository_id=999), archive, META)
    with pytest.raises(UploadTooLarge):
        with Session(service.engine) as session, session.begin():
            session.scalar(select(models.Project)).max_upload_bytes = 1
        service.accept(identity, archive, META)
    assert count(service.engine, models.Run) == 0


def test_concurrent_replay_is_one_run(service, identity, archive):
    with ThreadPoolExecutor(max_workers=2) as pool:
        results = list(pool.map(lambda _: service.accept(identity, archive, META), range(2)))
    assert sorted(created for _, created in results) == [False, True]
    assert count(service.engine, models.Run) == 1


def test_worker_lock_prevents_duplicate_execution(service, identity, archive):
    service.accept(identity, archive, META)
    entered, release = Event(), Event()

    def failing_claims(*_):
        entered.set()
        assert release.wait(15)
        raise RuntimeError("injected failure")

    with ThreadPoolExecutor(max_workers=1) as pool:
        running = pool.submit(service.work_one, failing_claims)
        try:
            assert entered.wait(15)
            assert service.work_one() is None
        finally:
            release.set()
        public_id = running.result(timeout=15)
    status = service.status(public_id)
    assert (status["status"], status["error_kind"], status["verdict"]) == (
        "error",
        "internal",
        None,
    )


def test_recovery_after_artifact_publication(service, identity, archive, monkeypatch):
    accepted, _ = service.accept(identity, archive, META)
    original = save.ingestion

    def crash(*_):
        raise RuntimeError("crashed before final transaction")

    monkeypatch.setattr(save, "ingestion", crash)
    with pytest.raises(RuntimeError, match="crashed"):
        service.work_one()
    assert service.status(accepted["run_id"])["status"] == "running"
    monkeypatch.setattr(save, "ingestion", original)

    def forbidden(*_):
        raise AssertionError("must not run the model again after publication")

    assert service.work_one(forbidden) == accepted["run_id"]
    assert service.status(accepted["run_id"])["status"] == "done"


def test_recorded_fiit_pipeline_persists_claims_and_raw_calls(service, identity, tmp_path):
    """Real FIIT responses and a fake NLI classifier: test storage, not NLI accuracy."""
    from notinspec.db.hosted_claims import HostedClaims
    from notinspec.nli import NliScores
    from notinspec.runner import FakeProvider, ModelClient

    core = Path(__file__).parents[2]
    fixtures = core / "tests" / "claims" / "fixtures"
    archive = tmp_path / "urllib3.tar.gz"
    pack_inputs(core / "examples" / "sphinx" / "urllib3" / "notinspec.yaml", archive)
    accepted, _ = service.accept(identity, archive.read_bytes(), META)

    class FakeNli:
        model_id = "fake/nli"
        revision = "0" * 40

        def score(self, pairs):
            return [NliScores(0.9, 0.05, 0.05) for _ in pairs]

    runner = HostedClaims(
        service.engine,
        ModelClient(FakeProvider.load(fixtures / "fiit-urllib3-demo.json"), max_attempts=1),
        FakeNli(),
        service.uploads_dir / "calls",
    )
    chunk_ids = {"567cff0c95e2e342", "0f1fe6bd0dcdec3d", "00fb7285ec99b133", "dab80b5788c33002"}

    def recorded_chunks(ingestion, out, run_id, allowed):
        selected = replace(
            ingestion, chunks=tuple(c for c in ingestion.chunks if c.id in chunk_ids)
        )
        assert len(selected.chunks) == 4
        return runner(selected, out, run_id, allowed)

    assert service.work_one(recorded_chunks) == accepted["run_id"]
    status = service.status(accepted["run_id"])
    assert status["status"] == "done", status
    assert count(service.engine, models.Claim) == 153
    assert count(service.engine, models.LlmCall) == 8
    assert count(service.engine, models.ClaimAnswer) == 8
    journal = service.uploads_dir / "calls" / f"{accepted['run_id']}.jsonl"
    assert len(journal.read_text(encoding="utf-8").splitlines()) == 8


def test_raw_journal_survives_database_failure(service, tmp_path, monkeypatch):
    from notinspec.claims.store import LlmCall
    from notinspec.db.hosted_claims import HostedCallLog

    path = tmp_path / "raw.jsonl"
    log = HostedCallLog(service.engine, path)

    def fail(_):
        raise RuntimeError("database unavailable")

    monkeypatch.setattr(log.database, "append", fail)
    call = LlmCall(
        "r",
        "claim-extractor",
        "qwen",
        "chunk",
        "qwen",
        "hash",
        {},
        {"choices": ["raw response"]},
        None,
        "2026-11-23T12:00:00+00:00",
    )
    with pytest.raises(RuntimeError, match="database unavailable"):
        log.append(call)
    assert json.loads(path.read_text())["response"] == call.response


@pytest.mark.parametrize(
    "text",
    [
        "[]",
        "{}",
        '{"schema_version":true,"head_sha":null,"base_sha":null}',
        '{"schema_version":0,"head_sha":"bad","base_sha":null}',
    ],
)
def test_invalid_metadata(text):
    from notinspec.config import ConfigError

    with pytest.raises(ConfigError):
        upload_meta(text)
