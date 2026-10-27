# NOT-IN-SPEC — Specification

**Team project 2026/2027, project no. 8.** Team leader: Ing. William Brach.
Source of requirements: [assignment.md](assignment.md). This document is the agreed interpretation of it.

## 1. What we are building

`notinspec` is a service that measures **how reliably language models answer questions about a specific API**, and how that reliability changes over time.

Given an OpenAPI specification and its version history, the system:

1. normalizes the input into **snippets** and **hard claims**;
2. **deterministically** generates test tasks from the claims (no LLM invents tasks);
3. runs every task against several LLMs in **three modes**: no context, retrieved snippet, full text;
4. **verifies** answers by executing the model's proposed request against a **mock server generated from the spec**;
5. stores every raw response forever, repeats runs on a schedule, diffs against the previous run, and alerts on drops;
6. reports **a list of questions models get wrong, why, and how that changes over time** — never a single score.

It ships as: a **CLI**, a **web service + public web UI / leaderboard**, a **scheduled worker**, and a **reusable GitHub Action** that fails a PR when a documentation change lowers answer accuracy.

### 1.1 What we are *not* building

- **Not** an "upload any document, get an AI-readability score" website. The assignment explicitly asks for "instead of a single score, a list of questions the models answer incorrectly, the cause of the failure, and how it evolves over time", requires a mock server generated from OpenAPI, and values results "verified by running code, not by another model's opinion". A generic score for arbitrary documents can satisfy none of that.
- **No** single aggregated score. Results are reported per API, mode, model and claim type.
- **No** user accounts. The web UI is public and read-only.

## 2. Architecture

```
            ┌─────────────── core (Python package `notinspec`) ───────────────┐
 inputs ──► │ adapters ─► claims ─► generator ─► runner ─► verifiers ─► report │
            └────▲───────────────────▲───────────────▲────────────────▲───────┘
                 │                   │               │                │
               CLI            FastAPI service     worker        GitHub Action
                                    │          (APScheduler)   (CLI + Prism in
                                    ▼                │          the CI runner)
                               React web UI    PostgreSQL ◄─────┘
                                                     │
                                                Slack alerts
```

**Principle:** all logic lives in `core`. CLI, API, worker and GitHub Action are thin wrappers. The Action needs no hosted service.

### 2.1 Input adapters

| Input | Claims | Verification |
|---|---|---|
| OpenAPI 3.x spec + its version history (git) | Hard claims (see §2.2) | Request executed against Prism mock server |

- **Changelog source:** change claims come from **diffing historical OpenAPI versions with `oasdiff`** (old versions taken from the API's public spec git repo). Changelog prose is used only as supporting evidence. This is deterministic and yields exact "removed X" claims. oasdiff reports a rename as a removal plus an addition, so "renamed X → Y" claims come from a deterministic pairing rule (same operation and location, same type, removed and added in the same version).
- Build order: **OpenAPI → oasdiff history**, using only hard claims.

### 2.2 Hard claim types (MVP)

| Type | Model must… |
|---|---|
| `endpoint-exists` | produce the correct method + path for an operation |
| `param-name` | use the correct parameter name and location (path/query/header/body) |
| `required-field` | include required body fields |
| `enum-value` | use a valid enum value |
| `auth-scheme` | authenticate correctly |
| `removed` | **not** use an endpoint/field that no longer exists |
| `renamed` | use the new name, not the old one |

Each type has a fixed prompt template, versioned with the generator.

### 2.3 Task generation

- Deterministic: same input + same generator version ⇒ identical task set (asserted by hash in tests).
- **Stratified sampling** with a fixed seed: even across claim types, **cap ≈100 claims per API per run**, same sample every run so runs are comparable.
- **Coverage** = sampled claims / total claims, reported per run.

### 2.4 Modes

| Mode | Context given to the model |
|---|---|
| `none` | nothing |
| `snippet` | top-k snippets retrieved with **BM25** (`rank_bm25`). Semester 2 experiment: local embeddings (sentence-transformers) in **pgvector**, reported separately |
| `full` / `full-sliced` | whole document if it fits the model's context window; otherwise the deterministic **slice** (tag/resource section) containing the claim. Slice size recorded per task |

### 2.5 Answer format and verification

- **Hard layer:** the model returns a **structured HTTP request** (JSON constrained by a schema: method, path, query, headers, body). The request is sent to **Prism** running the current spec in validation mode. A validation error = fail.

### 2.6 Failure causes (determined by code, not by a model)

A failed hard answer is additionally validated against **older spec versions**.

| Cause | Meaning |
|---|---|
| `stale-knowledge` | request is valid against an older spec version (the headline finding) |
| `hallucinated` | uses something that never existed in any known version |
| `wrong-location` | right name, wrong place (e.g. query vs body) |
| `missing-required` | required field omitted |
| `invalid-value` | wrong type / enum value |
| `wrong-auth` | wrong authentication scheme |
| `malformed-output` | answer does not match the response schema |
| `refusal` | model declined to answer |

### 2.7 Reports and metrics

- Primary table: **accuracy per API × mode × model**, with 95% bootstrap confidence intervals.
- Alongside: coverage, failure-cause distribution, delta vs. previous run, **newly failing / newly passing questions**.
- Never a single overall score.

### 2.8 Repeated runs, diffs and alerts

- Worker runs each target **weekly**, plus on detected input change.
- Each run is diffed against the previous run of the same target.
- **Slack** webhook alert when accuracy (per API × mode × model) drops by more than a threshold (default **5 percentage points**, configurable).
- Runs are **resumable**: if rate limits stop a run, the worker continues it later.

## 3. Models under test

- Accessed via **OpenRouter**, **free (`:free`) models only**, panel of ~4 models. No GPU available, so no local models.
- Client is rate-limit aware (queue, backoff on 429), caches every response by (run ID, model, prompt hash) so a resumed run never re-asks. The cache never crosses runs: each scheduled run asks again, otherwise change over time could not be measured.
- Every call is recorded with exact model ID, temperature (0), and all parameters.
- Free models can disappear: a vanished model is a normal, displayed state on the leaderboard, not an error.

### 3.1 Budget constraint (important)

OpenRouter free models are limited to **20 requests/min** and **50 requests/day per account**, raised to **1,000 requests/day once ≥10 USD of credits have been purchased** ([OpenRouter limits](https://openrouter.ai/docs/limits)). Limits are per account, not per key.

One full run of one API = 100 claims × 3 modes × 4 models = **1,200 requests**.

| Scenario | Feasible scope |
|---|---|
| 0 USD (50/day) | ~1 API run per month with 4 models. Not enough for weekly tracking. |
| **10 USD one-time** (1,000/day) | 3 APIs weekly (~3,600 requests over ~4 days). **Required for the plan as specified.** |

**Action:** request a one-time 10 USD credit from the faculty / team leader. Until then, run with a reduced panel (2 models, 30 claims) to start the dataset.

## 4. Targets (leaderboard)

Initial: **Stripe, GitHub REST, Twilio**. All publish official OpenAPI specs in public git repos (`stripe/openapi`, `github/rest-api-description`, `twilio/twilio-oai`), giving version history for `oasdiff`. More added once the pipeline is stable. Plus a small **demo API repo** we own, used to dogfood the GitHub Action within free limits.

## 5. Stack

| Area | Choice |
|---|---|
| Language | Python 3.12+ (core, API, worker), TypeScript (web) |
| Packaging / tooling | uv, ruff, mypy (core), pytest, pre-commit |
| API | FastAPI; its generated OpenAPI is validated in CI |
| Spec tooling | OpenAPI 3.x + JSON Schema, **Prism** (mock server), **oasdiff** (spec diffs), **Schemathesis** (tests our own API) |
| LLM access | OpenRouter (OpenAI-compatible API) |
| Evaluation | `rank_bm25`, scikit-learn |
| Database | PostgreSQL, SQLAlchemy 2, Alembic; pgvector in semester 2 |
| Scheduler | APScheduler in a dedicated `worker` container, job state in Postgres (no Redis/Celery) |
| Web UI | React + Vite + TypeScript SPA, ECharts or Recharts, served by nginx |
| Alerts | Slack incoming webhook |
| Agent formats | `AGENTS.md` in our repo, our own `llms.txt`; MCP server (stretch, semester 2) |

## 6. Data

- **Raw responses are append-only**: stored as JSONB, never updated or deleted. The dataset cannot be reconstructed retroactively, so this is the most valuable asset.
- Every result row records: input snapshot hash, spec version, generator version, task ID, mode, model ID + params, raw response, verification result, failure cause, timestamps.
- Database backed up regularly from the VM (pg_dump, off-machine copy).
- The dataset is intended to be published. **TBD:** check that the terms of each free model allow publishing its outputs.

## 7. GitHub Action

- Reusable action (Docker / composite) that runs the CLI + Prism inside the CI runner. No dependency on our hosted service.
- Triggers on PRs touching the OpenAPI spec.
- Runs the suite on the base branch and the PR branch, posts a PR comment listing newly failing questions, and **fails the build when hard-layer accuracy drops by more than a configurable threshold**.
- User provides their own `OPENROUTER_API_KEY` as a secret.

## 8. DevOps

- **Monorepo:**
  ```
  core/     package + CLI
  api/      FastAPI service
  worker/   scheduler
  web/      React SPA
  action/   GitHub Action
  deploy/   docker-compose, nginx, env templates
  docs/     SPEC, FAQ, INSPIRATION, assignment
  ```
- **Docker Compose** services: `postgres`, `api`, `worker`, `prism` (as needed), `web` (nginx).
- **CI (GitHub Actions):** lint (ruff, mypy, oxlint), unit tests, Compose integration tests, build images, push to **GHCR**.
- **CD:** the faculty VM is reachable only over VPN, so a **self-hosted GitHub runner on the VM** pulls images from GHCR and runs `docker compose up -d`. The repo is public, so the runner is used **only by the deploy job on pushes to `main`** (dedicated runner label + protected `production` environment), and workflows from fork PRs require maintainer approval. Fork PRs must never run on the VM.
- Public GitHub repository under a team organization, **MIT license**.

## 9. Testing

- **Determinism tests:** same input ⇒ same task-set hash; golden files per adapter.
- **Fake LLM provider** replaying recorded responses. **CI never calls OpenRouter.**
- **Integration:** Compose up → Prism with a small fixture spec → full end-to-end run.
- Our own API: OpenAPI validated in CI + Schemathesis.
- Web: Playwright smoke tests.
- Coverage gate on `core/` only.

## 10. Milestones

Faculty checkpoint dates: **TBD**.

**Semester 1 — MVP (hard layer end-to-end)**
- OpenAPI + oasdiff adapter, hard claim types, deterministic generator with sampling
- 3 modes, OpenRouter runner, Prism verification, failure causes
- CLI, Postgres schema, worker with schedule + Slack alerts
- Basic web UI (per-API results, failing questions, history)
- CI/CD to the faculty VM
- **Weekly runs for Stripe, GitHub, Twilio from mid-semester.** The long-term dataset only starts when the first run happens, so this date matters more than features.

**Semester 2 — breadth and evaluation**
- Public GitHub Action + demo repo
- Leaderboard polish, data visualization
- Embedding retrieval experiment (pgvector)
- MCP server exposing results (stretch)
- Evaluation write-up: accuracy by claim type, stale-knowledge findings, trends over time

## 11. Roles

| # | Role | Owns |
|---|---|---|
| 1 | Lead / architecture | core package, task generator, this spec |
| 2 | Input adapters | OpenAPI, oasdiff history |
| 3 | Runner & verification | OpenRouter client, rate limiting, Prism, failure causes |
| 4 | ML / evaluation | retrieval, sampling, coverage, statistics, stale-knowledge analysis |
| 5 | Backend & data | FastAPI, Postgres schema, migrations, worker |
| 6 | Frontend & viz | web UI, leaderboard, charts |
| 7 | DevOps | CI, Compose, GHCR, self-hosted runner, GitHub Action, monitoring |

## 12. Open items

- [ ] Request a one-time 10 USD OpenRouter credit (§3.1)
- [ ] Faculty checkpoint dates (§10)
- [ ] Free-model terms on publishing outputs (§6)
- [ ] Pick the initial free-model panel from OpenRouter's current `:free` list
- [ ] Confirm alert threshold (default 5 pp)
