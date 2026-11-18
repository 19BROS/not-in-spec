import json
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from notinspec_api.main import app

client = TestClient(app)


def _run(root: Path, run_id: str, created_at: str) -> dict[str, object]:
    run = {"id": run_id, "project": "p", "created_at": created_at, "commit": "c",
           "counts": {"files": 1}, "steps": []}  # fmt: skip
    (root / run_id).mkdir()
    (root / run_id / "run.json").write_text(json.dumps(run), "utf-8")
    return run


@pytest.fixture
def runs(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    monkeypatch.setenv("NOTINSPEC_RUNS_DIR", str(tmp_path))
    return tmp_path


def test_list_newest_first_without_unfinished(runs: Path) -> None:
    _run(runs, "old", "2026-11-17T10:00:00+00:00")
    _run(runs, "new", "2026-11-18T10:00:00+00:00")
    (runs / "unfinished").mkdir()  # no run.json yet
    body = client.get("/demo/runs").json()
    assert [r["id"] for r in body] == ["new", "old"]
    assert set(body[0]) == {"id", "project", "created_at", "commit", "counts"}


def test_broken_run_json_is_skipped(runs: Path) -> None:
    _run(runs, "good", "2026-11-18T10:00:00+00:00")
    (runs / "half").mkdir()
    (runs / "half" / "run.json").write_text('{"id": "ha', "utf-8")  # half-written
    assert [r["id"] for r in client.get("/demo/runs").json()] == ["good"]
    assert client.get("/demo/runs/half").status_code == 404


def test_list_without_folder(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    monkeypatch.setenv("NOTINSPEC_RUNS_DIR", str(tmp_path / "missing"))
    assert client.get("/demo/runs").json() == []


def test_get_run(runs: Path) -> None:
    run = _run(runs, "r1", "2026-11-18T10:00:00+00:00")
    assert client.get("/demo/runs/r1").json() == run


def test_missing_run_is_404(runs: Path) -> None:
    assert client.get("/demo/runs/nope").status_code == 404


@pytest.mark.parametrize("run_id", ["..", "a b", "x" * 101, "%2E%2E"])
def test_bad_run_id(runs: Path, run_id: str) -> None:
    assert client.get(f"/demo/runs/{run_id}").status_code in (404, 422)
    assert client.get(f"/demo/runs/{run_id}").status_code != 200
