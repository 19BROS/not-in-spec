# Plan: demo, a CLI run whose results show on the web

Goal for today's meeting: run `notinspec demo` on urllib3 from the CLI, then open the web and
show what we have: ingestion, inventory, claims with grounding, and which pipeline steps are
not built yet. Two branches in parallel:

| Branch | Owns | Session |
|---|---|---|
| `core/demo-run` | `core/` (builder + `notinspec demo`), `api/` (2 read endpoints) | A |
| `web/demo-screens` | `web/` (3 screens) | B |

Both work against the **contract below**. B starts on the committed sample
`web/src/fixtures/demo-run.sample.json` (real urllib3 data, trimmed), so B does not wait for A.

**Shortcut, on purpose:** no Postgres. The DB models are still open (SPEC §18), so runs are
folders on disk (`tmp/runs/<id>/run.json`) and the API only reads them. Local only
(`uvicorn` + `vite dev`); no change in `deploy/`, `.github/` or the Action. Mark it in code
with `# shortcut:` like `api/main.py` does.

Not in scope: L0–L4, models under test, scores, Postgres, auth, uploads, deploy. Never
average levels or show one overall score (AGENTS.md); the demo shows counts only.

## Flow

```
notinspec demo --config X.yaml   (core, CLI)
  ├─ ingestion       → tmp/runs/<id>/ingestion.json, results.json, report.html, comment.md
  ├─ claims run      → tmp/runs/<id>/claims.json, claims.html, claims-store.jsonl   (unless --no-claims)
  └─ build_demo_run  → tmp/runs/<id>/run.json      (written last: a folder without it is not listed)

GET /api/demo/runs        (api)  → list of run summaries, newest first
GET /api/demo/runs/{id}   (api)  → that run.json

web  #/                    runs list
     #/runs/<id>           run dashboard
     #/runs/<id>/claims    claims + detail panel
```

## Contract: `run.json` v0

Reference converter: `docs/plans/demo-run-reference.py` (scratch script that made the
sample). A ports it into core and deletes it. Field names below are binding for both sides.

```jsonc
{
  "schema": "notinspec-demo-run", "schema_version": 0,
  "id": "20261118T1030Z-urllib3-ab12",          // also the folder name
  "project": "urllib3",
  "created_at": "2026-11-18T10:30:00+00:00",
  "commit": "8cb1aca…",                          // from results.json, may be ""
  "tool_version": "0.0.0",
  "docs": { "sphinx_version": "9.1.0" | null, "input_hash": "…", "config_hash": "…" },
  "counts": { "files": 22, "chunks": 481, "symbols": 266, "parameters": 464, "changes": 3,
              "warnings": 0, "claims": 446 | null, "claims_kept": 338 | null },
  "steps": [   // always these 7 ids, in this order
    { "id": "read",      "label": "Read & chunk",    "status": "done", "detail": "22 files · 481 chunks" },
    { "id": "inventory", "label": "Build inventory", "status": "done", "detail": "266 symbols · 3 changes" },
    { "id": "claims",    "label": "Extract claims",  "status": "done" | "skipped" | "failed", "detail": "…" },
    { "id": "grounding", "label": "Ground claims (citation, NLI, identifiers)", "status": "…", "detail": "…" },
    { "id": "tests",     "label": "Generate tests (L0-L4)", "status": "not_implemented", "detail": "next iteration" },
    { "id": "models",    "label": "Run models",            "status": "not_implemented", "detail": "next iteration" },
    { "id": "evaluate",  "label": "Evaluate & report",     "status": "not_implemented", "detail": "next iteration" }
  ],
  "documents": [ { "source": "user-guide", "chunks": 40, "tokens": 9000, "symbols": 0,
                   "claims": 120, "claims_kept": 100 } ],      // claims 0 for pages not run
  "symbols":   [ { "path": "urllib3.PoolManager", "kind": "class", "source": "reference/…" | null,
                   "parameters": ["num_pools", "headers"] } ],
  "changes":   [ { "symbol": "…", "kind": "deprecated", "version": "2.0.0",
                   "parameter": null, "replacement": null } ],
  "warnings":  [ /* ingestion warnings, as in ingestion.json */ ],
  "claims": null | {                                            // null with --no-claims
    "sources": ["user-guide", "reference/urllib3.util", "v2-migration-guide"],
    "extractors": ["qwen/qwen3.8-27b", "openai/gpt-oss-20b"],
    "counts": { "<extractor>": { "kept": 338, "citation_not_found": 18, "not_checkable": 79,
                                 "nli_neutral": 6, "nli_contradiction": 1, "id_missing": 4 } },
    "versions": { /* claims.json "versions" as is */ },
    "items": [ {
      "id": "<chunk_id>:<extractor>:<local_id>", "extractor": "…", "source": "user-guide",
      "breadcrumb": "urllib3 > User Guide > …", "chunk_id": "…", "type": "fact",
      "text": "…", "citation": "…",
      "status": "kept" | "citation_not_found" | "not_checkable" | "nli_neutral" | "nli_contradiction" | "id_missing",
      "premise": "…" | null,
      "nli": { "entailment": 0.74, "neutral": 0.04, "contradiction": 0.22, "truncated": false } | null,
      "missing": ["urllib3.util.parse_url"]
    } ]
  }
}
```

`GET /demo/runs` returns `[{ "id", "project", "created_at", "commit", "counts" }]`.

## Session A: `core/demo-run`

1. **`core/src/notinspec/demo.py`**: `build_demo_run(ingestion: dict, results: dict, claims: dict | None, run_id: str) -> dict`.
   Port of the reference converter, typed (mypy strict). Without claims: steps `claims` and
   `grounding` are `skipped`, `counts.claims*` and `claims` are `null`. Claims with failed
   chunks (`claims.json` `failures`) → step `claims` says how many failed, still `done`.
2. **CLI `notinspec demo`** in `cli.py`, calling the existing ingestion and claims-run code
   (no copy of their logic):
   `--config`, `--runs-dir` (default `tmp/runs`), `--source` (repeatable), `--extractor`
   (repeatable), `--no-claims`, `--claims-store PATH` (copied to `<run>/claims-store.jsonl`
   before the claims run, so stored answers are reused). Run ID
   `YYYYmmddTHHMMZ-<project>-<4 hex>`. Writes `run.json` last. Prints the run folder and
   `http://localhost:5173/#/runs/<id>`. Exit 2 on failure, like `ci`.
3. **API** in `api/src/notinspec_api/main.py`: `GET /demo/runs`, `GET /demo/runs/{run_id}`.
   Folder from env `NOTINSPEC_RUNS_DIR`, default `tmp/runs` (relative to the cwd: run
   uvicorn from the repo root). Validate `run_id` with `[A-Za-z0-9_.-]{1,100}` and reject
   `.`/`..`; 404 when missing. Skip folders without `run.json`.
4. **Tests** (no LLM, no NLI model): `build_demo_run` with and without claims (small
   hand-built dicts, or the core claims test fixtures); `notinspec demo --no-claims` on
   `core/tests/fixtures/sphinx`; the API endpoints with `TestClient` and `tmp_path`
   (list order, 404, bad id).
5. **Docs**: a "Demo" section in `core/README.md` with the commands below. Delete
   `docs/plans/demo-run-reference.py`.

Done when: `uv run ruff check && uv run ruff format --check && uv run mypy && uv run pytest`
are green and the demo commands below work.

## Session B: `web/demo-screens`

Style reference: `docs/plans/demo-style.png` (style only, not its data or screens). Light grey
page, white cards with a thin border and small radius, small grey labels, big numbers in
stat tiles, left sidebar with the `not-in-spec` logo and a coral active item, a blue accent
for progress, green/grey step icons, coloured status pills, dark code blocks for citations.
Plain CSS with tokens in `:root`, dark mode not required. **No new npm dependencies**
(tiny hash router in `App.tsx`).

Data: `fetch('/api/demo/runs')` and `fetch('/api/demo/runs/<id>')` (Vite proxies `/api` to
`:8000`). If the API is unreachable or the URL has `?fixture`, use
`src/fixtures/demo-run.sample.json` and show a small "sample data" badge. Types for the
contract in `src/types.ts`.

1. **Runs** (`#/`): table of runs: project, date, commit (7 chars), files, chunks, symbols,
   claims kept / claims (or "–"), link to the run. Empty state tells the CLI command.
2. **Run dashboard** (`#/runs/<id>`): title "urllib3 docs", meta line (date · commit ·
   Sphinx version · input hash short). Stat tiles: Files, Chunks, Symbols, Parameters,
   Changes, Claims kept. **Pipeline** card with the 7 steps (done = green check, skipped /
   not_implemented = grey with its detail). **Claims by status** per extractor (horizontal
   bars, like "Failure categories" in the style image). **Documents** table (source, chunks,
   symbols, claims, kept). **Changes** list (symbol, kind, version, replacement).
3. **Claims** (`#/runs/<id>/claims`), like "Findings" in the style image: filters (status,
   extractor, source) and a table (status pill, source, claim text); clicking a row opens the
   detail panel on the right: claim, citation (code block), premise, NLI as three bars,
   missing identifiers, breadcrumb. Dropped claims are shown with their reason.
4. Optional if time: **Symbols** (`#/runs/<id>/symbols`): searchable table (path, kind,
   parameters, source).

Done when: `cd web && npm run lint && npm run build` pass and all screens work on the fixture
and on a real run from A.

## Demo commands (after both are merged)

Prepare the runs before the meeting: NLI takes ~3 min per extractor on a laptop CPU.
`GROQ_API_KEY` must be in the environment (needed only for chunks not in the store).

```sh
uv sync --all-packages --extra nli
uv run notinspec demo --config core/examples/sphinx/urllib3/notinspec.yaml \
  --source user-guide --source reference/urllib3.util --source v2-migration-guide \
  --claims-store experiments/nli/runs/008-core-pipeline-urllib3-demo/claims-store.jsonl
uv run notinspec demo --config core/examples/sphinx/trio/notinspec.yaml --no-claims
uv run notinspec demo --config core/examples/sphinx/hydra-zen/notinspec.yaml --no-claims

uv run uvicorn notinspec_api.main:app --reload     # :8000
cd web && npm run dev                              # http://localhost:5173
```

Live in the meeting: `notinspec demo … --no-claims` on trio (1 s), refresh the web, then open
the prepared urllib3 run with claims.
