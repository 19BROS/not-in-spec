"""Import of run folders and the DB stores, against a real Postgres (TEST_DATABASE_URL)."""

import json
from pathlib import Path
from typing import Any

import pytest
from sqlalchemy import Engine, func, select
from sqlalchemy.orm import Session

from notinspec.claims.model import RawClaim
from notinspec.claims.store import LlmCall, ReuseKey, StoredAnswer
from notinspec.cli import main
from notinspec.db import models, save
from notinspec.db.importer import import_runs
from notinspec.db.stores import DbCallLog, DbClaimStore

TRIO = Path(__file__).parents[2] / "examples" / "sphinx" / "trio" / "notinspec.yaml"


@pytest.fixture(scope="module")
def demo_runs(tmp_path_factory: pytest.TempPathFactory) -> Path:
    """One real `notinspec demo --no-claims` run, plus claims files like `claims run` writes."""
    runs = tmp_path_factory.mktemp("runs")
    assert main(["demo", "--config", str(TRIO), "--runs-dir", str(runs), "--no-claims"]) == 0
    (folder,) = runs.iterdir()
    chunk = json.loads((folder / "ingestion.json").read_bytes())["chunks"][0]
    claim = {"chunk_id": chunk["id"], "extractor": "qwen", "local_id": "c1", "text": "t",
             "citation": "c", "type": "fact", "run_id": folder.name, "prompt_hash": "ph",
             "model": "qwen"}  # fmt: skip
    grounded = {"claim": claim, "prompt_version": 1, "status": "kept", "citation_span": [0, 1],
                "citation_matches": 1, "premise_candidates": 1, "premise": "p",
                "premise_span": [0, 1], "nli": {"entailment": 0.9}, "missing": []}  # fmt: skip
    claims: dict[str, Any] = {
        "claims": [grounded],
        "versions": {"grounding": 1},
        "failures": [{"chunk_id": chunk["id"], "extractor": "gemma", "cause": "timed-out",
                      "detail": "no answer"}],
        "problems": [],
    }  # fmt: skip
    (folder / "claims.json").write_text(json.dumps(claims), encoding="utf-8")
    call = {"run_id": folder.name, "role": "claim-extractor", "extractor": "qwen",
            "chunk_id": chunk["id"], "model": "qwen", "prompt_hash": "ph", "request": {},
            "response": {"model": "qwen"}, "error": None,
            "time": "2026-11-21T10:00:00+00:00"}  # fmt: skip
    (folder / "llm-calls.jsonl").write_text(json.dumps(call) + "\n" + '{"cut', encoding="utf-8")
    entry = {"key": {"content_hash": chunk["content_hash"], "breadcrumb": chunk["breadcrumb"],
                     "extractor": "qwen", "model": "qwen", "prompt_version": 1},
             "answer": {"claims": [], "problems": [], "run_id": folder.name,
                        "prompt_hash": "ph", "model": "qwen"}}  # fmt: skip
    (folder / "claims-store.jsonl").write_text(json.dumps(entry) + "\n", encoding="utf-8")
    (runs / "unfinished").mkdir()  # no run.json
    return runs


def _count(engine: Engine, table: type[models.Base]) -> int:
    with Session(engine) as session:
        return session.scalar(select(func.count()).select_from(table)) or 0


def test_import_stores_the_run_its_docs_and_every_file(engine: Engine, demo_runs: Path) -> None:
    outcomes = {o.folder: o for o in import_runs(engine, demo_runs)}
    assert outcomes["unfinished"].status == "skipped"
    (run_out,) = (o for name, o in outcomes.items() if name != "unfinished")
    assert run_out.status == "imported", run_out.detail

    folder = next(p for p in demo_runs.iterdir() if (p / "run.json").is_file())
    run_json = json.loads((folder / "run.json").read_bytes())
    ingestion = json.loads((folder / "ingestion.json").read_bytes())
    with Session(engine) as session:
        run = session.scalars(select(models.Run)).one()
        assert (run.public_id, run.trigger, run.status) == (run_json["id"], "cli", "done")
        assert session.scalars(select(models.Project.slug)).all() == [run_json["project"]]
        steps = session.scalars(select(models.RunStep.step).order_by(models.RunStep.position))
        assert list(steps) == [s["id"] for s in run_json["steps"]]
        names = set(session.scalars(select(models.RunArtifact.name)))
        assert {"run.json", "ingestion.json", "results.json", "claims.json"} <= names
        stored = session.scalar(
            select(models.RunArtifact.content).where(models.RunArtifact.name == "run.json")
        )
        assert stored == (folder / "run.json").read_bytes()
    assert _count(engine, models.Chunk) == len(ingestion["chunks"])
    assert _count(engine, models.Symbol) == len(ingestion["inventory"]["symbols"])
    parameters = sum(
        len(sig["parameters"]) for s in ingestion["inventory"]["symbols"] for sig in s["signatures"]
    )
    assert _count(engine, models.Parameter) == parameters
    assert _count(engine, models.Change) == len(ingestion["inventory"]["changes"])
    assert _count(engine, models.Claim) == 1
    assert _count(engine, models.ExtractionIssue) == 1
    assert _count(engine, models.LlmCall) == 1  # the cut-off last line is left out
    assert _count(engine, models.ClaimAnswer) == 1


def test_import_again_skips_runs_already_in_the_database(engine: Engine, demo_runs: Path) -> None:
    import_runs(engine, demo_runs)
    again = [o.status for o in import_runs(engine, demo_runs) if o.folder != "unfinished"]
    assert again == ["exists"]
    assert _count(engine, models.Run) == 1


def test_cli_import_and_upgrade(
    engine: Engine, demo_runs: Path, db_url: str, schema: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    sep = "&" if "?" in db_url else "?"
    monkeypatch.setenv("DATABASE_URL", f"{db_url}{sep}options=-csearch_path%3D{schema}")
    assert main(["db", "upgrade"]) == 0  # already at head: nothing to do
    assert main(["db", "import-runs", str(demo_runs)]) == 0
    assert _count(engine, models.Run) == 1


def test_db_stores_behave_like_the_jsonl_ones(engine: Engine) -> None:
    store = DbClaimStore(engine)
    key = ReuseKey("h", "lib > A", "qwen", "m", 1, None, 2, None)
    assert store.get(key) is None
    first = StoredAnswer((RawClaim("c1", "t", "c", "fact"),), (), "r1", "ph", "m")
    second = StoredAnswer((), ("skipped",), "r2", "ph2", "m")
    store.put(key, first)
    store.put(key, second)
    assert store.get(key) == second  # a later answer wins
    assert store.get(ReuseKey("h", "lib > A", "qwen", "m", 1, None, 2, False)) is None

    DbCallLog(engine).append(
        LlmCall(
            "no-such-run",
            "claim-extractor",
            "qwen",
            "k1",
            "m",
            "ph",
            {},
            None,
            "x",
            "2026-11-21T10:00:00+00:00",
        )  # fmt: skip
    )
    with Session(engine) as session:
        call = session.scalars(select(models.LlmCall)).one()
        assert (call.run_id, call.run_ref, call.error) == (None, "no-such-run", "x")


def test_register_a_project_and_update_it(
    engine: Engine, db_url: str, schema: str, monkeypatch: pytest.MonkeyPatch
) -> None:
    with Session(engine) as session, session.begin():
        save.project(session, "trio")  # as a demo import creates it, without a repository
    sep = "&" if "?" in db_url else "?"
    monkeypatch.setenv("DATABASE_URL", f"{db_url}{sep}options=-csearch_path%3D{schema}")
    args = ["db", "add-project", "trio", "--repository", "python-trio/trio",
            "--repository-id", "37415591", "--workflow", "notinspec.yml"]  # fmt: skip
    assert main(args) == 0
    assert main([*args, "--allowed-model", "qwen/qwen3.8-27b", "--budget-per-run", "0.5"]) == 0
    with Session(engine) as session:
        project = session.scalars(select(models.Project)).one()  # the demo project, registered
        assert (project.repository_id, project.default_branch) == (37415591, "main")
        assert project.workflow_path == "python-trio/trio/.github/workflows/notinspec.yml"
        assert (project.allowed_models, str(project.budget_per_run_usd)) == (
            ["qwen/qwen3.8-27b"],
            "0.5000",
        )
    with Session(engine) as session, session.begin(), pytest.raises(ValueError, match="trio"):
        registration = save.Registration(
            "other", "x/y", 37415591, "main", "notinspec.yml"
        )  # the same repository ID under another project
        save.register_project(session, registration)
