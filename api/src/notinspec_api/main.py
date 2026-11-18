import json
import os
import re
import secrets
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from fastapi import FastAPI, Header, HTTPException, Request

from notinspec import __version__

app = FastAPI(title="NOT-IN-SPEC", version=__version__)

MAX_RESULTS_BYTES = 1_000_000  # nginx caps bodies at 1 MB too (client_max_body_size default)
_REPO_PART = re.compile(r"[A-Za-z0-9_.-]{1,100}")
_COMMIT = re.compile(r"[0-9a-f]{40}")


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/runs", status_code=201)
async def ingest_run(request: Request, authorization: str = Header("")) -> dict[str, str]:
    """Store one results.json pushed by the GitHub Action (action/example-results.json).

    shortcut: one shared INGEST_TOKEN for every repo and files on a volume instead of Postgres;
    move to GitHub OIDC (repo proven by GitHub) and the DB schema once role 5 has it.
    """
    token = os.environ.get("INGEST_TOKEN", "")
    if not token:
        raise HTTPException(503, "ingest is disabled")
    if not secrets.compare_digest(authorization.encode(), f"Bearer {token}".encode()):
        raise HTTPException(401, "bad token")
    body = await request.body()
    if len(body) > MAX_RESULTS_BYTES:
        raise HTTPException(413, "results too large")
    try:
        data = json.loads(body)
    except ValueError as exc:
        raise HTTPException(422, "body is not JSON") from exc
    if not isinstance(data, dict) or data.get("schema_version") != 0:
        raise HTTPException(422, "unsupported schema_version")
    repo, commit = data.get("repo"), data.get("commit")
    parts = repo.split("/") if isinstance(repo, str) else []
    # repo becomes a directory name, so ".." or extra slashes must never get through
    if len(parts) != 2 or not all(_REPO_PART.fullmatch(p) and p not in (".", "..") for p in parts):
        raise HTTPException(422, "repo must be owner/name")
    if not isinstance(commit, str) or not _COMMIT.fullmatch(commit):
        raise HTTPException(422, "commit must be a 40-char sha")

    # random suffix: two runs can arrive within the clock's resolution
    name = f"{datetime.now(UTC):%Y%m%dT%H%M%SZ}-{commit[:12]}-{secrets.token_hex(4)}.json"
    path = Path(os.environ.get("RESULTS_DIR", "/results"), *parts, name)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as f:  # append-only: never overwrite an earlier run
        f.write(body)
    return {"stored": f"{repo}/{path.name}"}


# shortcut: demo runs are folders written by `notinspec demo` (docs/plans/demo-cli-web.md),
# read straight from disk; they move to Postgres once the DB models are settled (SPEC §18).
_SUMMARY_FIELDS = ("id", "project", "created_at", "commit", "counts")


def _runs_dir() -> Path:
    return Path(os.environ.get("NOTINSPEC_RUNS_DIR", "tmp/runs"))


def _read_run(path: Path) -> dict[str, Any]:
    data: dict[str, Any] = json.loads(path.read_bytes())
    return data


@app.get("/demo/runs")
def demo_runs() -> list[dict[str, Any]]:
    root = _runs_dir()
    runs = [
        _read_run(p / "run.json")
        for p in (root.iterdir() if root.is_dir() else [])
        if (p / "run.json").is_file()
    ]
    runs.sort(key=lambda r: (r.get("created_at", ""), r.get("id", "")), reverse=True)
    return [{k: r.get(k) for k in _SUMMARY_FIELDS} for r in runs]


@app.get("/demo/runs/{run_id}")
def demo_run(run_id: str) -> dict[str, Any]:
    # run_id becomes a path part, so ".." or slashes must never get through
    if not _REPO_PART.fullmatch(run_id) or run_id in (".", ".."):
        raise HTTPException(422, "bad run id")
    path = _runs_dir() / run_id / "run.json"
    if not path.is_file():
        raise HTTPException(404, "run not found")
    return _read_run(path)
