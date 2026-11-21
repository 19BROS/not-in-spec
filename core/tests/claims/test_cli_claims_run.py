"""`notinspec claims run` end to end: recorded Groq answers and recorded NLI scores (SPEC §13)."""

import json
from collections.abc import Callable
from pathlib import Path
from typing import NoReturn

import pytest

from notinspec import cli
from notinspec.chunking import Chunk
from notinspec.claims import GROQ_EXTRACTORS, MemoryCallLog, pipeline, run_claims
from notinspec.config import load_config
from notinspec.ingestion import ingest
from notinspec.nli import MODEL_ID, REVISION, NliModel, NliUnavailable, RecordedNli
from notinspec.runner import FakeProvider, ModelClient, Provider, ProviderError

CORE = Path(__file__).parents[2]
FIXTURES = Path(__file__).parent / "fixtures"
GUIDE_RECORDING = FIXTURES / "groq-fixturelib-guide.json"
# the guide recording is from Groq, so these tests name its provider and extractors
GROQ = (
    "--provider",
    "groq",
    "--extractor",
    "qwen/qwen3.8-27b",
    "--extractor",
    "openai/gpt-oss-20b",
)
URLLIB3_RECORDING = FIXTURES / "groq-urllib3-demo.json"
NLI_RECORDING = FIXTURES / "nli-claims.json"  # see conftest.py
URLLIB3_CHUNKS = ("567cff0c95e2e342", "0f1fe6bd0dcdec3d", "00fb7285ec99b133")


def _fake(_: str) -> Provider:
    return FakeProvider.load(GUIDE_RECORDING)


def _no_provider(_: str) -> Provider:
    raise ProviderError("GROQ_API_KEY is not set")


def _recorded() -> NliModel:
    return RecordedNli.load(NLI_RECORDING)


def _run(config: Path, out: Path, *args: str) -> int:
    return cli.main(
        ["claims", "run", "--config", str(config), "--out", str(out), "--run-id", "t", *args]
    )


def test_run_writes_grounded_claims_and_a_report(
    fixture_project: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    out = tmp_path / "out"
    monkeypatch.setattr(cli, "_live_provider", _fake)
    monkeypatch.setattr(cli, "_nli_model", _recorded)
    assert _run(fixture_project, out, "--source", "guide", *GROQ) == 0
    data = json.loads((out / "claims.json").read_text(encoding="utf-8"))
    assert data["chunks"] == 8 and data["sources"] == ["guide"]
    assert data["versions"]["nli_model"] == MODEL_ID
    assert data["versions"]["nli_revision"] == REVISION
    assert data["versions"]["decision_rule"] == "argmax"
    assert [e["reasoning_effort"] for e in data["extractors"]] == [None, "low"]
    assert data["counts"] == {
        "qwen/qwen3.8-27b": {
            "kept": 6, "citation_not_found": 0, "not_checkable": 0, "nli_neutral": 0,
            "nli_contradiction": 0, "id_missing": 0,
        },
        "openai/gpt-oss-20b": {
            "kept": 13, "citation_not_found": 0, "not_checkable": 5, "nli_neutral": 0,
            "nli_contradiction": 0, "id_missing": 0,
        },
    }  # fmt: skip
    claims = data["claims"]
    assert len(claims) == 24
    kept = [c for c in claims if c["status"] == "kept"]
    assert all(c["premise"] and c["nli"]["entailment"] > 0.5 for c in kept)
    unchecked = [c for c in claims if c["status"] == "not_checkable"]
    assert all(c["premise"] is None and c["nli"] is None for c in unchecked)
    # every grounded claim still points at the call that produced it
    calls = [json.loads(line) for line in (out / "llm-calls.jsonl").read_text("utf-8").splitlines()]
    assert {(c["run_id"], c["prompt_hash"]) for c in calls} >= {
        (c["claim"]["run_id"], c["claim"]["prompt_hash"]) for c in claims
    }
    printed = capsys.readouterr().out
    assert "openai/gpt-oss-20b: 13 kept, 0 citation_not_found, 5 not_checkable" in printed

    page = (out / "claims.html").read_text(encoding="utf-8")
    assert "<script" not in page and "fixturelib: claims" in page
    assert page.count("<td class=kept>kept") == 19

    # a second run reuses every answer and gives the same bytes
    first = (out / "claims.json").read_bytes()
    monkeypatch.setattr(cli, "_live_provider", _no_provider)
    assert _run(fixture_project, out, "--source", "guide", "--run-id", "second", *GROQ) == 0
    assert (out / "claims.json").read_bytes() == first


def test_missing_nli_stops_before_any_llm_call(
    fixture_project: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def unavailable() -> NliModel:
        raise NliUnavailable("NLI needs the optional dependencies: notinspec[nli]")

    asked: list[str] = []
    monkeypatch.setattr(cli, "_live_provider", lambda name: asked.append(name) or _fake(name))
    monkeypatch.setattr(cli, "_nli_model", unavailable)
    assert _run(fixture_project, tmp_path / "out", "--source", "guide") == 2
    assert "notinspec[nli]" in capsys.readouterr().err
    assert asked == [] and not (tmp_path / "out" / "claims.json").exists()


def test_record_nli_saves_the_scores(
    fixture_project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(cli, "_live_provider", _fake)
    monkeypatch.setattr(cli, "_nli_model", _recorded)
    record = tmp_path / "nli.json"
    args = ("--source", "guide", "--extractor", "qwen/qwen3.8-27b", "--record-nli", str(record))
    assert _run(fixture_project, tmp_path / "out", *args) == 0
    entries = json.loads(record.read_text(encoding="utf-8"))
    assert len(entries) == 6 and {e["revision"] for e in entries} == {REVISION}


def test_record_nli_keeps_the_scores_when_a_later_step_fails(
    fixture_project: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    def broken(*_: object) -> NoReturn:
        raise RuntimeError("after NLI")

    monkeypatch.setattr(cli, "_live_provider", _fake)
    monkeypatch.setattr(cli, "_nli_model", _recorded)
    monkeypatch.setattr(pipeline, "_decide", broken)
    record = tmp_path / "nli.json"
    args = ("--source", "guide", "--extractor", "qwen/qwen3.8-27b", "--record-nli", str(record))
    assert _run(fixture_project, tmp_path / "out", *args) == 2
    assert "after NLI" in capsys.readouterr().err
    assert len(json.loads(record.read_text(encoding="utf-8"))) == 6


def test_run_claims_on_urllib3_demo_chunks(
    tmp_path: Path, golden: Callable[[str, object], None]
) -> None:
    """Docstrings and a guide section of urllib3: real answers, real NLI scores (replayed)."""
    ingestion = ingest(
        load_config(CORE / "examples" / "sphinx" / "urllib3" / "notinspec.yaml"),
        output=tmp_path / "out",
    )
    by_id: dict[str, Chunk] = {c.id: c for c in ingestion.chunks}
    result = run_claims(
        [by_id[i] for i in URLLIB3_CHUNKS],
        GROQ_EXTRACTORS,
        ModelClient(FakeProvider.load(URLLIB3_RECORDING), max_attempts=1),
        RecordedNli.load(NLI_RECORDING),
        "r",
        MemoryCallLog(),
        sections=ingestion.chunks,
        inventory=ingestion.inventory,
        project=ingestion.project,
    )
    statuses = [c.status for c in result.claims]
    assert statuses.count("kept") == 33 and statuses.count("not_checkable") == 7
    golden("urllib3-demo-grounded", result.claims)
