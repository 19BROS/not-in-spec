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
docs/     SPEC, FAQ, INSPIRATION, assignment
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
- **CI never calls OpenRouter.** Tests use the fake provider with recorded responses.
- **Raw LLM responses are append-only.** Never UPDATE or DELETE them.
- **Task generation is deterministic.** Same input + generator version ⇒ same task-set hash. No LLM generates tasks or extracts claims.
- **Never average layers** (hard / medium / soft) and never produce a single overall score.
- Secrets only via env (`deploy/.env`, GitHub secrets). Never commit them.

## Git workflow

- `main` is protected and auto-deploys. Work on short-lived branches, open a PR, CI must be green.
- Branch names: `<area>/<short-topic>`, e.g. `core/oasdiff-adapter`, `web/leaderboard`.

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
