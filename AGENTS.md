# AGENTS.md

Instructions for humans and AI coding agents working in this repo. The product spec is [docs/SPEC.md](docs/SPEC.md); it wins over anything here.

**Current goal: live demo on 2026-12-09.** Our supervisor picks a documentation built with Sphinx 9.x at random, and L0–L3 must run on it live. OpenAPI and L4 are out of the MVP. Plan and risks: [docs/plans/live-demo-2026-12-09.md](docs/plans/live-demo-2026-12-09.md).

## Layout

```
core/     notinspec package + CLI   (all logic lives here)
api/      FastAPI service           (thin wrapper over core)
worker/   APScheduler worker        (thin wrapper over core)
web/      React + Vite + TS SPA
action/   reusable GitHub Action
deploy/   docker-compose, nginx, env template, fixtures
docs/     SPEC, assignment, DEPLOY (production runbook), design (UI screens)
```

The web UI design is in [docs/design/](docs/design/README.md). Follow those screens where they agree with SPEC, and read the README's notes on each screen: screen 1 (upload / connect a repo) is not MVP, because the web UI is read-only and runs start only from the Action (SPEC §1.1, §11.1).

Python packages form one **uv workspace** (root `pyproject.toml`). Each lives in `<dir>/src/<module>` with tests in `<dir>/tests`.

## Commands

```sh
uv sync --all-packages              # install everything (Python 3.12+)
uv sync --all-packages --extra nli  # + torch CPU and transformers for the real NLI model; plain uv sync removes them
uv run ruff check && uv run ruff format --check
uv run mypy                         # strict, core only
uv run pytest --cov=notinspec       # all Python tests, coverage gate on core
uv run notinspec --help             # CLI
uv run notinspec db upgrade        # migrations on DATABASE_URL (notinspec[db])
uv run notinspec db import-runs tmp/runs   # old run folders into the DB
uv run notinspec db add-project NAME --repository O/R --repository-id ID --workflow F.yml   # register for uploads
TEST_DATABASE_URL=postgresql://… uv run pytest core/tests/db   # DB tests; skipped without it
uv run uvicorn notinspec_api.main:app --reload    # API on :8000
uv run pre-commit install           # once per clone

cd web && npm ci && npm run dev     # web on :5173, /api proxied to :8000
npm run lint && npm run build

cp deploy/.env.example deploy/.env  # once
docker compose -f deploy/docker-compose.yml up --build            # full stack on :8080
sh deploy/mock/smoke.sh                                           # mock (Prism) service, on a running stack
docker run --rm -p 4010:4010 -v "$PWD/deploy/fixtures:/s:ro" stoplight/prism:5 mock -h 0.0.0.0 /s/openapi.yaml  # bare Prism on :4010
```

Add a dependency to a package: `uv add --package notinspec-api <dep>` (never pip). Commit `uv.lock` and `web/package-lock.json`.

## Rules that must not be broken

- **All logic in `core/`.** API, worker, CLI and Action only call into it.
- **Our tests and our CI never call a real LLM** (SPEC §13). They replay recorded real responses through the fake provider, for every LLM role in SPEC §8 (models under test, claim extractors, task-text writer, round-trip solvers, judge). NLI uses a fake classifier in unit tests, and the real model runs only in marked slow tests. The product itself calls the real models: the CLI and the worker use the FIIT LiteLLM proxy (claim extractors), Groq (models under test) and the local NLI model on real docs.
- **FIIT proxy: only the free local models** (`qwen3.8-flash-next`, `gemma4-26b-a4b-hpc`). The team shares one key and budget, and the paid models draw from it, so the client refuses every other model (SPEC §8). Don't widen `FIIT.allowed_models` without a team decision.
- **Raw LLM responses are append-only**, for every LLM call. Never UPDATE or DELETE them.
- **References are computed by code.** Same input + generator version ⇒ same references. An LLM only writes task text and extracts claims; both are frozen in the golden set.
- **Never average levels** (L0–L4) and never produce a single overall score.
- Secrets only via env (`deploy/.env`, GitHub secrets). Never commit them.

## Git workflow

- `main` is protected and auto-deploys. Work on short-lived branches, open a PR, CI must be green.
- Branch names: `<area>/<short-topic>`, e.g. `core/oasdiff-adapter`, `web/leaderboard`.
- Work mostly in your role's area (below). Shared files (`pyproject.toml`, `uv.lock`, `deploy/`, `.github/`) change in small separate PRs.
- Before opening a PR: `git pull --rebase origin main`.
- **Lock file conflict** (`uv.lock` or `web/package-lock.json`): never merge it by hand. Resolve `pyproject.toml` / `package.json` first, then regenerate the lock (it is rebuilt from those, so either side is fine to start from):
  ```sh
  git checkout --ours uv.lock && uv lock && git add uv.lock
  cd web && git checkout --ours package-lock.json && npm install && git add package-lock.json
  ```

### Roles and reviews

Seven roles, one person each. What each builds is in [SPEC §17](docs/SPEC.md#17-roles); which paths each reviews is in [`.github/CODEOWNERS`](.github/CODEOWNERS), so GitHub requests the owner's review on its own.

| # | Role | Who |
|---|---|---|
| 1 | DevOps & Action | Damián Parigal (`damianecek`) |
| 2 | Architecture lead | Jakub Mitický (`jmiticky4130`) |
| 3 | Frontend & data | Jana Puchein (`JanaPuchein`) |
| 4 | Inputs: docs & claims | Erik Dusík (`Hinzun`) |
| 5 | L2 & changes | Radoslav Muntág (`RadoslavMuntag`) |
| 6 | Test generation | Samuel Maliarik (`ryzovy-nakyp`) |
| 7 | Runs, evaluation & CI gate | Richard Sič (`figaro112`) |

Roles say who builds and who reviews, not who may touch what. Anyone may open a PR anywhere.

**How many reviews.** The ruleset on `main` requires 1 approval and does not enforce code owners. We aim for **2 reviewers, never more**:

- **One owner** of the area the PR changes most (the code owner GitHub requests). A PR across several areas needs one owner, not all of them; mention the others if their part matters.
- **One more reviewer**, anyone. Best is someone whose code uses the change.
- **1 approval is enough** when only one person is free to review, and for small PRs (docs and typos, tests only, `experiments/`, a fix of a few lines, a revert of a broken `main`).

**When a reviewer must be a specific role:**

- **Contracts between stages** (the files that list the lead in `CODEOWNERS`: inventory, call record, claim, finding and test-item models, the DB schema, the pipeline, CLI and config) and **this file or the SPEC**: the lead (2), and if someone else reviews too, the owner of the code on the other side of the contract.
- **Security boundaries** (uploads and OIDC, archive extraction, `deploy/`, `.github/`, the `mock` service, the self-hosted runner): DevOps (1).
- **Shared files** (`pyproject.toml`, `uv.lock`): DevOps (1) or the lead (2).

**Flexibility.**

- An owner who has not reviewed within 2 working days may be replaced by anyone who knows the area. Say so in the PR; the owner may still comment after the merge, and a fix is a new PR.
- When the author owns the area, the reviewer should be someone who knows the area or uses the change.

### Adding a new service (new top-level directory)

Touch every place below in the same PR, or the service will build but never deploy:

| Where | What |
|---|---|
| `<dir>/pyproject.toml`, `<dir>/src/<module>`, `<dir>/tests` | Python package, same shape as `api/` |
| root `pyproject.toml` | add to `[tool.uv.workspace] members`, `known-first-party`, pytest `testpaths`; then `uv lock` |
| `<dir>/Dockerfile` | copy `api/Dockerfile` or `worker/Dockerfile` |
| `deploy/docker-compose.yml` | new service using `ghcr.io/${IMAGE_OWNER}/notinspec-<name>:${TAG}`; never publish ports except `proxy` (Caddy, TLS). The deploy starts every service without a profile (plus `backup`), so a dev-only service must sit behind its own profile |
| `deploy/nginx.conf` | only if browsers must reach it (route under `/api` or a new prefix) |
| `.github/workflows/ci.yml` | add to the `images` matrix |
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
- Two worktrees running Compose at once collide on project name and ports. Give one its own: `COMPOSE_PROJECT_NAME=notinspec-oasdiff WEB_PORT=8081 HTTPS_PORT=8444 docker compose -f deploy/docker-compose.yml up`.
