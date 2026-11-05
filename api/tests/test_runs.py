import json
from pathlib import Path
from typing import Any

import pytest
from fastapi.testclient import TestClient

from notinspec_api.main import app

client = TestClient(app)
AUTH = {"Authorization": "Bearer secret"}
RESULTS = {"schema_version": 0, "repo": "19BROS/demo", "commit": "a" * 40, "verdict": "pass"}


@pytest.fixture(autouse=True)
def env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> Path:
    monkeypatch.setenv("INGEST_TOKEN", "secret")
    monkeypatch.setenv("RESULTS_DIR", str(tmp_path))
    return tmp_path


def test_stores_results(env: Path) -> None:
    r = client.post("/runs", json=RESULTS, headers=AUTH)
    assert r.status_code == 201
    (stored,) = (env / "19BROS" / "demo").iterdir()
    assert json.loads(stored.read_bytes()) == RESULTS


def test_two_runs_of_same_commit_are_both_kept(env: Path) -> None:
    client.post("/runs", json=RESULTS, headers=AUTH)
    client.post("/runs", json=RESULTS, headers=AUTH)
    assert len(list((env / "19BROS" / "demo").iterdir())) == 2


@pytest.mark.parametrize("headers", [{}, {"Authorization": "Bearer wrong"}])
def test_rejects_bad_token(headers: dict[str, str]) -> None:
    assert client.post("/runs", json=RESULTS, headers=headers).status_code == 401


def test_disabled_without_token(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("INGEST_TOKEN")
    assert client.post("/runs", json=RESULTS, headers=AUTH).status_code == 503


@pytest.mark.parametrize(
    "change",
    [
        {"schema_version": 1},
        {"repo": "../etc"},
        {"repo": "../../x"},
        {"repo": "a/b/c"},
        {"repo": "owner/.."},
        {"commit": "abc"},
        {"commit": None},
    ],
)
def test_rejects_invalid_results(change: dict[str, Any], env: Path) -> None:
    assert client.post("/runs", json=RESULTS | change, headers=AUTH).status_code == 422
    assert list(env.iterdir()) == []


def test_rejects_non_json_and_too_large() -> None:
    assert client.post("/runs", content=b"nope", headers=AUTH).status_code == 422
    big = b"[" + b"0," * 600_000 + b"0]"
    assert client.post("/runs", content=big, headers=AUTH).status_code == 413
