# AGENTS.md

Instructions for humans and AI coding agents working in this repo. The product spec is [docs/SPEC.md](docs/SPEC.md); it wins over anything here.

## Layout

```
core/     notinspec package + CLI   (all logic lives here)
api/      FastAPI service           (thin wrapper over core)
worker/   APScheduler worker        (thin wrapper over core)
web/      React + Vite + TS SPA
action/   reusable GitHub Action
deploy/   docker-compose, nginx, env template, fixtures
docs/     SPEC, assignment, DEPLOY (production runbook)
```

Python packages form one **uv workspace** (root `pyproject.toml`). Each lives in `<dir>/src/<module>` with tests in `<dir>/tests`.

## Commands

```sh
uv sync --all-packages              # install everything (Python 3.12+)
uv run ruff check && uv run ruff format --check
uv run mypy                         # strict, core only
uv run pytest --cov=notinspec       # all Python tests, coverage gate on core
uv run notinspec --help             # CLI
uv run uvicorn notinspec_api.main:app --reload    # API on :8000
uv run pre-commit install           # once per clone

cd web && npm ci && npm run dev     # web on :5173, /api proxied to :8000
npm run lint && npm run build

cp deploy/.env.example deploy/.env  # once
docker compose -f deploy/docker-compose.yml up --build            # full stack on :8080
docker compose -f deploy/docker-compose.yml --profile prism up    # + Prism mock on :4010
```

Add a dependency to a package: `uv add --package notinspec-api <dep>` (never pip). Commit `uv.lock` and `web/package-lock.json`.

## Rules that must not be broken

- **All logic in `core/`.** API, worker, CLI and Action only call into it.
- **CI never calls a real LLM.** Every LLM role (models under test, claim extractors, task-text writer, judge) uses the fake provider with recorded responses.
- **Raw LLM responses are append-only**, for every LLM call. Never UPDATE or DELETE them.
- **References are computed by code.** Same input + generator version ⇒ same references. An LLM only writes task text and extracts claims; both are frozen in the golden set.
- **Never average levels** (L0–L4) and never produce a single overall score.
- Secrets only via env (`deploy/.env`, GitHub secrets). Never commit them.

## Git workflow

- `main` is protected and auto-deploys. Work on short-lived branches, open a PR, CI must be green.
- Branch names: `<area>/<short-topic>`, e.g. `core/oasdiff-adapter`, `web/leaderboard`.
- Stay in your own directory. Shared files (`pyproject.toml`, `uv.lock`, `deploy/`, `.github/`) change in small separate PRs.
- Before opening a PR: `git pull --rebase origin main`.
- **Lock file conflict** (`uv.lock` or `web/package-lock.json`): never merge it by hand. Resolve `pyproject.toml` / `package.json` first, then regenerate the lock (it is rebuilt from those, so either side is fine to start from):
  ```sh
  git checkout --ours uv.lock && uv lock && git add uv.lock
  cd web && git checkout --ours package-lock.json && npm install && git add package-lock.json
  ```

### Adding a new service (new top-level directory)

Touch every place below in the same PR, or the service will build but never deploy:

| Where | What |
|---|---|
| `<dir>/pyproject.toml`, `<dir>/src/<module>`, `<dir>/tests` | Python package, same shape as `api/` |
| root `pyproject.toml` | add to `[tool.uv.workspace] members`, `known-first-party`, pytest `testpaths`; then `uv lock` |
| `<dir>/Dockerfile` | copy `api/Dockerfile` or `worker/Dockerfile` |
| `deploy/docker-compose.yml` | new service using `ghcr.io/${IMAGE_OWNER}/notinspec-<name>:${TAG}`; never publish ports except `web` |
| `deploy/nginx.conf` | only if browsers must reach it (route under `/api` or a new prefix) |
| `.github/workflows/ci.yml` | add to the `images` matrix |
| `.github/workflows/deploy.yml` | add to both `pull` and `up` lists |
| `AGENTS.md` layout, `docs/SPEC.md` §12 | one line each |

Non-Python services (like `web/`) skip the workspace row and get their own CI job instead.

### Parallel work with git worktrees

Use a worktree per branch instead of stashing or re-cloning. Useful when several branches (or several AI agents) are in flight at once:

```sh
git worktree add ../notinspec-oasdiff -b core/oasdiff-adapter   # new branch in a sibling folder
cd ../notinspec-oasdiff
uv sync --all-packages && (cd web && npm ci)                     # each worktree has its own .venv / node_modules
# ... work, commit, push, open PR ...
cd - && git worktree remove ../notinspec-oasdiff                 # when merged
git worktree list                                                # see what's open
```

- `deploy/.env` is gitignored, so copy it into the new worktree if you need Compose there.
- Two worktrees running Compose at once collide on project name and ports. Give one its own: `COMPOSE_PROJECT_NAME=notinspec-oasdiff WEB_PORT=8081 docker compose -f deploy/docker-compose.yml up` (Prism's 4010 is fixed, so run it in one worktree only).
