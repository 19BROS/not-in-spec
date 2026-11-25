# CLI prototype

This branch builds on `core/chunking` (PR #7). It adds real documentation ingestion to the
existing CLI. The parsers and chunker are owned by role 4 (SPEC §17); the CLI calls them through
`notinspec.ingestion.ingest`, which the API or worker can also call.

From the repository root:

```sh
uv sync --all-packages
uv run notinspec --help
uv run notinspec ci --config core/examples/cli/notinspec.yaml --out tmp/cli-demo
```

The example processes one Markdown guide into **3 chunks** and extracts **2 OpenAPI
operations**. Open `tmp/cli-demo/report.html` to review every chunk. `ingest` is an alias
for `ci`; `python -m notinspec.cli` also works. The existing `chunk` command is preserved.

### Sphinx demo

Real Sphinx 9 XML of three libraries is committed in `core/examples/sphinx/` (see its README:
urllib3 with reST fields, trio with Google docstrings via napoleon, hydra-zen with numpydoc):

```sh
uv run notinspec ci --config core/examples/sphinx/urllib3/notinspec.yaml --out tmp/urllib3
uv run notinspec ci --config core/examples/sphinx/trio/notinspec.yaml --out tmp/trio
uv run notinspec ci --config core/examples/sphinx/hydra-zen/notinspec.yaml --out tmp/hydra-zen
```

Open `tmp/<lib>/report.html`: chunks grouped by document, each with its breadcrumb, size,
block kinds and text, and the reader's warnings first. No LLM is called.

Preview which inputs the configuration selects:

```sh
uv run notinspec ci --config core/examples/cli/notinspec.yaml --out tmp/cli-demo --dry-run
```

`--dry-run` checks configuration, file existence, supported formats and output location, then
lists the selected files (a Sphinx XML folder with its XML file count). It creates no files and preserves existing output. It does **not**
parse document content or validate OpenAPI schemas; run the normal command for those checks.

### Demo

`notinspec demo` runs `ci` and `claims run` into one folder `tmp/runs/<run id>/` and writes
`run.json` (contract: `docs/plans/demo-cli-web.md`) last. The API serves it
(`GET /api/demo/runs`, `GET /api/demo/runs/<id>`) and the web shows it. Shortcut: folders on
disk, no Postgres. Claims need `FIIT_API_KEY` (only for chunks not in the claims store) and the
`nli` extra; `--no-claims` needs neither.

```sh
uv sync --all-packages --extra nli
uv run notinspec demo --config core/examples/sphinx/urllib3/notinspec.yaml \
  --source user-guide --source reference/urllib3.util --source v2-migration-guide \
  --claims-store experiments/nli/runs/009-fiit-urllib3-demo/claims-store.jsonl
uv run notinspec demo --config core/examples/sphinx/trio/notinspec.yaml --no-claims
uv run notinspec demo --config core/examples/sphinx/hydra-zen/notinspec.yaml --no-claims

uv run uvicorn notinspec_api.main:app --reload     # :8000, from the repo root
cd web && npm run dev                              # http://localhost:5173
```

## Configuration

Paths are relative to the configuration file, regardless of the current working directory.

```yaml
project: "items-api"                  # optional; root of every breadcrumb
docs:
  sphinx_xml: "build/xml/"            # optional; folder built by `sphinx-build -b xml`
  paths: ["docs/**/*.md", "llms.txt"]  # optional; glob patterns, duplicates removed
  openapi: "api/openapi.yaml"         # optional; YAML or JSON, OpenAPI 3.x
  changelog: "CHANGES.md"             # optional; Markdown or plain text
```

At least one input is required. Markdown (`.md`, `.markdown`) and plain text (`.txt`) are
supported. Explicit missing files and unsupported formats fail with an explanation. Patterns
matching nothing produce a warning, or an error if no inputs remain.

`docs.sphinx_xml` is a folder below the config with the output of `sphinx-build -b xml`
(SPEC §6.1) and a `build-env.txt` whose first line is `sphinx-build 9.x.y`: **only Sphinx 9.x
is read**. A missing folder, no `*.xml` files, a missing `build-env.txt` or another Sphinx
major version is an error (exit 2), also in `--dry-run`. `docs.paths` patterns never select
files inside that folder. The old `docs.sphinx` (a Sphinx project to build) explains the change:
the CLI never builds Sphinx.
`project` starts every chunk breadcrumb (`items-api > Items API > List items`). Without it, the
repository name from `GITHUB_REPOSITORY` is used, otherwise the config directory's name.
Unknown fields inside `docs` and duplicate YAML keys are errors with an explanation.
`docs.version` is accepted as metadata reserved for later stages. Top-level model, budget and
threshold settings remain unused; this is not validation of the complete future config schema.
YAML merge overrides that repeat a key are also rejected rather than resolved silently.

All configured files are processed, not just changes in a PR. Paths outside the config's
directory are rejected, including symlinks resolving outside it. The output folder is excluded
from discovery so repeated runs do not read their own `comment.md`. Run from the config's
directory to use the defaults: `notinspec ci` reads `notinspec.yaml` and writes `notinspec-out/`.
Explicit relative `--config` and `--out` arguments are resolved from the terminal's directory.

## Artifacts and exit codes

| File | Content |
|---|---|
| `ingestion.json` | deterministic input hashes, source paths, full chunks (blocks with `field` / `name` / `type` for API reference entries), normalized OpenAPI operations, the Sphinx and reader version (`sphinx`, `null` without Sphinx input) and warnings; ingestion schema v3 |
| `results.json` | Action/server envelope v0, ingestion counts, `stage: ingestion`, `verdict: not-evaluated`, empty `results` and `findings` |
| `comment.md` | summary beginning with the Action's `<!-- notinspec -->` marker |
| `report.html` | plain HTML (no scripts, no external files) for reviewing chunks by eye: counts, warnings with counts, every chunk per document |

`ingestion.json` contains the adapter's intermediate normalized data, **not** the complete v3
inventory (`Symbol`, `Signature`, `Constraint`, ...). OpenAPI descriptions are retained in
that data but are not yet turned into prose chunks. `results.json` adds timestamps and GitHub
run metadata, so it is not byte-identical between runs; `ingestion.json` is.

- **0:** ingestion completed, possibly with parser warnings. This is **not** a passing LLM test.
- **2:** bad arguments/configuration, missing or unreadable inputs, fatal parsing/output error,
  or a crash. OpenAPI schema problems that the adapter can recover from are warnings.
- **1:** reserved for a future evaluated regression; this prototype never returns it.

Artifacts are first written into a temporary directory under the output folder. Only after all
four are ready are the previous artifacts replaced. If a normal write/publish error occurs,
the previous files are restored; unrelated files in the output folder are preserved. If the
filesystem also prevents rollback, the CLI returns 2 and reports where it kept recovery backups.
This is not a crash-safe transaction and does not support simultaneous writers to one output
folder. After a failed run, old reports may still exist: use the exit code to distinguish them
from a newly completed run.

There are no LLM calls, generated tasks, golden set, NLI decisions, Prism runs, model scores,
incremental comparisons or statistical pass/fail decisions yet. Model/budget/threshold
settings are unused. Warnings are not labelled as K1-K7 findings.

## GitHub Action integration boundary

The Action is a thin client ([SPEC §11.1](../docs/SPEC.md#111-upload-api)): it runs only
`notinspec pack`, which writes the upload archive with the inputs `ci --dry-run` would select,
so the Action and our service always agree on what the inputs are. The verdict comes from the
service, never from the CLI.

## Verification

```sh
uv run pytest --cov=notinspec
uv run ruff check
uv run ruff format --check
uv run mypy
```

New tests cover real Markdown/OpenAPI ingestion, paths relative to the config, repeatability,
own-output exclusion, input changes, unsupported inputs, error exit codes, honest reports,
dry-run, config typos/duplicates and recovery after interrupted artifact publication.
