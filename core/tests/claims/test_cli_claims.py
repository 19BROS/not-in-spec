"""`notinspec claims extract` with the recorded fake provider; CI never calls Groq."""

import json
from pathlib import Path

import pytest

from notinspec import cli
from notinspec.cli import main
from notinspec.runner import FakeProvider, Provider, ProviderError

GUIDE_RECORDING = Path(__file__).parent / "fixtures" / "groq-fixturelib-guide.json"
OUTPUT = "extracted-claims.json"


def _fake(_: str) -> Provider:
    return FakeProvider.load(GUIDE_RECORDING)


def _no_provider(_: str) -> Provider:
    raise ProviderError("GROQ_API_KEY is not set")


def _extract(config: Path, out: Path, *args: str) -> int:
    return main(
        ["claims", "extract", "--config", str(config), "--out", str(out), "--run-id", "t", *args]
    )


def _lines(path: Path) -> list[str]:
    return path.read_text(encoding="utf-8").splitlines()


def test_extract_writes_claims_and_calls(
    fixture_project: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    out = tmp_path / "out"
    monkeypatch.setattr(cli, "_live_provider", _fake)
    assert _extract(fixture_project, out, "--source", "guide") == 0
    assert not (out / "claims.json").exists()  # the grounded claims come from a later step
    data = json.loads((out / OUTPUT).read_text(encoding="utf-8"))
    assert data["chunks"] == 8 and data["sources"] == ["guide"]
    assert [e["name"] for e in data["extractors"]] == ["qwen/qwen3.8-27b", "openai/gpt-oss-20b"]
    assert len(data["claims"]) == 24 and data["failures"] == []
    calls = [json.loads(line) for line in _lines(out / "llm-calls.jsonl")]
    assert len(calls) == 16
    # every claim points at the call that produced it
    by_call = {(c["run_id"], c["prompt_hash"]) for c in calls}
    assert all((c["run_id"], c["prompt_hash"]) in by_call for c in data["claims"])
    assert {c["model"] for c in data["claims"]} <= {"qwen/qwen3.8-27b", "openai/gpt-oss-20b"}
    assert "qwen/qwen3.8-27b: 6 claims, 8 chunks asked" in capsys.readouterr().out

    # a second run reuses every chunk: no provider, byte-identical output (the original call's
    # run ID stays on the claims), no new calls
    first = (out / OUTPUT).read_bytes()
    monkeypatch.setattr(cli, "_live_provider", _no_provider)
    assert _extract(fixture_project, out, "--source", "guide", "--run-id", "second") == 0
    assert (out / OUTPUT).read_bytes() == first
    assert len(_lines(out / "llm-calls.jsonl")) == 16


def test_no_reuse_asks_again_and_replaces(
    fixture_project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    out = tmp_path / "out"
    monkeypatch.setattr(cli, "_live_provider", _fake)
    args = ("--source", "guide", "--extractor", "qwen/qwen3.8-27b")
    assert _extract(fixture_project, out, *args) == 0
    assert _extract(fixture_project, out, *args, "--no-reuse", "--run-id", "again") == 0
    assert len(_lines(out / "llm-calls.jsonl")) == 16
    assert len(_lines(out / "claims-store.jsonl")) == 16
    # a normal run now reuses the replaced answers
    monkeypatch.setattr(cli, "_live_provider", _no_provider)
    assert _extract(fixture_project, out, *args, "--run-id", "third") == 0
    data = json.loads((out / OUTPUT).read_text(encoding="utf-8"))
    assert {c["run_id"] for c in data["claims"]} == {"again"}


def test_record_saves_a_fixture(
    fixture_project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(cli, "_live_provider", _fake)
    record = tmp_path / "rec.json"
    out = tmp_path / "out"
    args = ("--source", "guide", "--extractor", "qwen/qwen3.8-27b", "--record", str(record))
    assert _extract(fixture_project, out, *args) == 0
    assert len(json.loads(record.read_text(encoding="utf-8"))) == 8


def test_record_survives_a_failure_midway(
    fixture_project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(cli, "_live_provider", _fake)
    record = tmp_path / "rec.json"
    # the second extractor has no recording, so the fake provider fails on its first chunk
    args = ("--source", "guide", "--extractor", "qwen/qwen3.8-27b", "--extractor", "acme/none")
    assert _extract(fixture_project, tmp_path / "out", *args, "--record", str(record)) == 2
    assert len(json.loads(record.read_text(encoding="utf-8"))) == 8


def test_without_key_the_run_stops(
    fixture_project: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    monkeypatch.setattr(cli, "_live_provider", _no_provider)
    out = tmp_path / "out"
    assert _extract(fixture_project, out, "--source", "guide", "--no-reuse") == 2
    assert "GROQ_API_KEY is not set" in capsys.readouterr().err
    assert not (out / OUTPUT).exists()


def test_cut_off_store_line_is_reported(
    fixture_project: Path,
    tmp_path: Path,
    monkeypatch: pytest.MonkeyPatch,
    capsys: pytest.CaptureFixture[str],
) -> None:
    out = tmp_path / "out"
    monkeypatch.setattr(cli, "_live_provider", _fake)
    args = ("--source", "guide", "--extractor", "qwen/qwen3.8-27b")
    assert _extract(fixture_project, out, *args) == 0
    store = out / "claims-store.jsonl"
    store.write_bytes(store.read_bytes()[:-40])  # a crash while writing the last entry
    capsys.readouterr()
    assert _extract(fixture_project, out, *args) == 0
    captured = capsys.readouterr()
    assert "removed a cut-off last line" in captured.err
    assert "1 chunks asked, 7 reused" in captured.out


def test_unknown_source(
    fixture_project: Path, tmp_path: Path, capsys: pytest.CaptureFixture[str]
) -> None:
    assert _extract(fixture_project, tmp_path / "out", "--source", "nothing*") == 2
    assert "no chunk source matches nothing*" in capsys.readouterr().err


def test_extractor_flag_and_several_sources(
    fixture_project: Path, tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    monkeypatch.setattr(cli, "_live_provider", _fake)
    out = tmp_path / "out"
    args = ("--extractor", "qwen/qwen3.8-27b", "--source", "gui*", "--source", "nothing")
    assert _extract(fixture_project, out, *args) == 0
    data = json.loads((out / OUTPUT).read_text(encoding="utf-8"))
    assert [e["name"] for e in data["extractors"]] == ["qwen/qwen3.8-27b"]
    assert data["sources"] == ["gui*", "nothing"] and data["chunks"] == 8


def test_claims_without_subcommand_prints_help() -> None:
    assert main(["claims"]) == 0
