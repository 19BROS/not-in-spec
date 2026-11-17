# CLI prototype

This branch builds on `core/chunking` (PR #7). It adds real documentation ingestion to the
existing CLI. The parsers and chunker remain owned by role 2; the CLI calls them through
`notinspec.ingestion.ingest`, which the API or worker can also call.

From the repository root:

```sh
uv sync --all-packages
uv run notinspec --help
uv run notinspec ci --config core/examples/cli/notinspec.yaml --out tmp/cli-demo
```

The example processes one Markdown guide into **3 chunks** and extracts **2 OpenAPI
operations**. Open `tmp/cli-demo/report.html` to inspect the summary. `ingest` is an alias
for `ci`; `python -m notinspec.cli` also works. The existing `chunk` command is preserved.

Preview which inputs the configuration selects:

```sh
uv run notinspec ci --config core/examples/cli/notinspec.yaml --out tmp/cli-demo --dry-run
```

`--dry-run` checks configuration, file existence, supported formats and output location, then
lists the selected files. It creates no files and preserves existing output. It does **not**
parse document content or validate OpenAPI schemas; run the normal command for those checks.

## Configuration

Paths are relative to the configuration file, regardless of the current working directory.

```yaml
docs:
  paths: ["docs/**/*.md", "llms.txt"]  # optional; glob patterns, duplicates removed
  openapi: "api/openapi.yaml"         # optional; YAML or JSON, OpenAPI 3.x
  changelog: "CHANGES.md"             # optional; Markdown or plain text
```

At least one input is required. Markdown (`.md`, `.markdown`) and plain text (`.txt`) are
supported. Explicit missing files and unsupported formats fail with an explanation. Patterns
matching nothing produce a warning, or an error if no inputs remain. Sphinx is not supported
yet: `docs.sphinx` produces an error instead of silently skipping that documentation.
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
| `ingestion.json` | deterministic input hashes, source paths, full chunks, normalized OpenAPI operations and warnings; ingestion schema v1 |
| `results.json` | Action/server envelope v0, ingestion counts, `stage: ingestion`, `verdict: not-evaluated`, empty `results` and `findings` |
| `comment.md` | summary beginning with the Action's `<!-- notinspec -->` marker |
| `report.html` | standalone readable summary, linked to `ingestion.json` |

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

The command flags and three report filenames follow `action/mock.py`, but **the current
Action image still runs that mock**. This branch does not change its Dockerfile, workflow,
server, database or deploy anything.

`not-evaluated` is a proposed extension of the v0 envelope. Before replacing the mock, agree
this status with the backend and DevOps: the current Action maps exit 0 to `verdict=pass` and
must distinguish successful ingestion from an evaluated pass. The full detail is a separate
artifact; the current server receives only `results.json`.

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
