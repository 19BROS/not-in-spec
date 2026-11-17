# Plan — session B: Sphinx demo integration (`core/sphinx-demo`)

Temporary working plan. Delete this file in the last commit before the PR is merged; the SPEC
is the lasting record. The other half of the work is on branch `core/sphinx-reader`
(`docs/plans/sphinx-reader.md`). The **Shared** part below is identical in both plans.

---

## Shared (identical in both plans)

### Goal: level-1 demo

```sh
uv run notinspec ci --config core/examples/sphinx/trio/notinspec.yaml --out tmp/trio
```

reads real Sphinx 9 XML (urllib3, trio, hydra-zen) into chunks, and a plain `report.html`
shows them for visual review. No LLM, no tasks, no evaluation.

### Decisions already made (project lead, 2026-11-17)

- **MVP supports Sphinx 9.x only.** The reader reads the first line of `build-env.txt`
  (`sphinx-build 9.1.0`, format from `action/README.md`). Missing file or another major
  version → `SphinxInputError`. Other versions and migration between them are future work.
- **Blocks straight from the doctree (approach "c").** No XML → Markdown → markdown-it round
  trip: it would lose node types, break on text that looks like Markdown, and cannot express
  per-parameter fields. The chunk text is a rendered, Markdown-like, read-only text (inline
  code in backticks), used for display and citations, never parsed again. The Markdown reader
  stays for Markdown inputs (README, llms.txt, changelogs, OpenAPI guides).
- **Real XML is committed** in `core/examples/sphinx/` (4.8 MB, built 2026-11-17; see its
  README). Tiny fixtures for golden tests go to `core/tests/fixtures/sphinx/`.
- **Plain `report.html`** (no JS) for visual review of chunks.
- **Two sessions, two PRs in total.** No PR per step. `core/pyproject.toml` + `uv.lock`
  (defusedxml) go into PR A on purpose, although AGENTS.md asks for small separate PRs for
  shared files: the lead wants few PRs.

### Contract (A implements, B uses)

```python
# notinspec/chunking/blocks.py
type BlockKind = Literal["heading", "text", "code", "table", "list", "quote", "html", "rule",
                         "admonition", "signature", "field"]
@dataclass(frozen=True)
class Block:
    ...                            # existing fields unchanged
    name: str | None = None        # field: "timeout", "RuntimeError"; None for unnamed returns
    field: str | None = None       # field: "param" | "returns" | "raises" | "return-type" | ...
    type: str | None = None        # field: "float | None"

# notinspec/chunking/chunker.py
@dataclass(frozen=True)
class BlockDocument:
    source: str                     # Sphinx: docname, e.g. "reference-core", "generated/hydra_zen.builds"
    text: str                       # rendered text; block line ranges point into it
    blocks: tuple[ParsedBlock, ...]
def chunk_blocks(document: BlockDocument, *, project: str,
                 soft_limit: int = DEFAULT_SOFT_LIMIT, ...) -> tuple[Chunk, ...]
# chunk_document(Document) = parse_blocks + chunk_blocks; Markdown output stays identical.

# notinspec/sphinx/__init__.py
SPHINX_READER_VERSION = 1
SUPPORTED_SPHINX_MAJOR = 9
class SphinxInputError(ValueError): ...
@dataclass(frozen=True)
class SphinxXml:
    sphinx_version: str                    # "9.1.1", from build-env.txt
    files: tuple[tuple[str, str], ...]     # (path relative to the XML folder, sha256 of the
                                           #  normalized bytes), sorted; build-env.txt included
    documents: tuple[BlockDocument, ...]   # sorted by source
    warnings: tuple[str, ...]              # sorted, e.g. "unknown node sd_foo (3x)"
def read_sphinx_xml(root: Path) -> SphinxXml
def read_sphinx_version(root: Path) -> str   # only build-env.txt; cheap, for --dry-run
```

`ingestion.py`: `INGESTION_SCHEMA_VERSION` 2 → 3 (new `Block` fields; B adds Sphinx metadata
under the same v3). **A changes this one line**, B rebases on it.

A contract change after work has started: edit the Shared part in **both** plan files and
tell the other session.

### Ownership (no file is touched by both)

| Session A (`core/sphinx-reader`) | Session B (`core/sphinx-demo`) |
|---|---|
| `core/src/notinspec/chunking/*` | `core/src/notinspec/{config,ingestion,report,cli}.py` (except the schema line) |
| `core/src/notinspec/sphinx/` (new) | `core/tests/test_{config,ingestion_cli,cli,report}*.py` |
| `core/tests/chunking/`, `core/tests/sphinx/` (new) | `core/tests/test_sphinx_demo.py` (new, end to end) |
| `core/tests/fixtures/sphinx/` (new) | `docs/SPEC.md` |
| `core/examples/sphinx/` | `core/README.md`, `action/README.md` |
| `core/pyproject.toml`, `uv.lock`, `.gitattributes` | |
| `docs/plans/sphinx-reader.md` | `docs/plans/sphinx-demo.md` |

### Order

1. Both start now. B does everything that does not import `notinspec.sphinx`.
2. **PR A merges first.** B then `git pull --rebase origin main`, wires ingestion, runs the
   end-to-end tests on the three libraries, and opens PR B. B reviews PR A meanwhile.
3. Before each PR: `git pull --rebase origin main`; `uv run ruff check && uv run ruff format
   --check && uv run mypy && uv run pytest --cov=notinspec` green; delete your plan file.
4. Commit messages follow the repo: `[ADD] …`, `[CHANGE] …`, `[DOCS] …`.

---

## Session B: integration, report, SPEC

Read first: `docs/SPEC.md` §2.3, §6.1, §10, §11, §16; `core/README.md`;
`core/src/notinspec/{config,ingestion,report,cli}.py`; `core/examples/sphinx/README.md`
(on branch `core/sphinx-reader` until PR A merges: `git show origin/core/sphinx-reader:core/examples/sphinx/README.md`).
Plan A (`git show origin/core/sphinx-reader:docs/plans/sphinx-reader.md`) has the census
of the real XML and the reader rules that the SPEC text must describe.

### Steps (one branch, commit as you go, one PR)

**Before PR A merges** (nothing here imports `notinspec.sphinx`):

1. **Plain `report.html` for visual review** (`report.py`). Works with Markdown chunks today
   (`core/examples/cli`), so build and check it now.
   - No JS, no external CSS/fonts; small inline `<style>`; everything HTML-escaped.
   - Header: project, input hash, counts (files, documents, chunks, sections, warnings).
   - Warnings table: message and count; `unknown node …` warnings sorted first.
   - Per document (group chunks by `source`, document order): each chunk as
     `<details>` with summary = breadcrumb, `part/parts`, tokens, block-kind counts
     (`text 4 · code 2 · field 3`), `oversized` marked; body = chunk text in `<pre>`, and a
     small table of `field` blocks (name, type, field) when present.
   - Must stay usable for ~2,000 chunks (trio): no per-chunk scripts, text only.
   - Tests: escaping (`<script>` in chunk text), every chunk id appears, warnings shown.
2. **Config** (`config.py`): accept `docs.sphinx_xml` (a directory inside the config folder,
   containing `build-env.txt` and at least one `*.xml`); remove the "not supported yet"
   error; keep the `docs.sphinx` hint. `--dry-run` lists the folder and its XML file count.
   Update `test_config.py`. (The Sphinx version in dry-run comes in step 5.)
3. **SPEC** (`docs/SPEC.md`), from the decisions above and the rules in plan A:
   - §6.1: MVP reads Sphinx 9.x XML only; blocks straight from the doctree (no Markdown round
     trip) and why; the node table in short; the ordering rule (prose after a `desc` stays
     in the section chunk); `rubric` is not a heading; `source` = docname; hash after
     normalizing `source=` paths; new block kinds `admonition`, `signature`, `field`.
   - §2.3: `build-env.txt` is required; its first line is `sphinx-build 9.x.y`.
   - §11: golden fixture built three ways + the three real example libraries.
   - §16.3 future work: other Sphinx versions and migration between them.
   - §18: update the "Sphinx build environment for the pilot" item (built, see
     `core/examples/sphinx/`).
   Ask session A to review the §6.1 text in PR B.
4. **Docs:** `core/README.md` (Sphinx input, the demo command for the three libraries,
   exit codes unchanged); `action/README.md` (Sphinx 9.x only; `build-env.txt` required).

**After PR A merges:** `git pull --rebase origin main`, then:

5. **Ingestion** (`ingestion.py`, `cli.py` if needed):
   - `plan_ingestion`: a `PlannedInput(kind="sphinx")` for the XML folder.
   - `ingest`: `read_sphinx_xml(folder)`; each `files` entry → `InputFile(source=<sphinx_xml>/<path>,
     kind="sphinx", content_hash=<normalized hash>)`; chunks from `chunk_blocks` per
     document, appended after Markdown chunks; reader warnings prefixed with the folder.
     `SphinxInputError` → `ConfigError`-style exit 2 with its message.
   - `Ingestion` / `ingestion.json` v3: `sphinx: {version, reader_version} | null`, and the
     new `Block` fields serialized.
   - `input_hash` stays the hash over all `files`, so it is the normalized XML hash.
   - `--dry-run` also shows `read_sphinx_version(folder)`; a version other than 9.x is an
     error already in dry-run.
6. **End-to-end tests** (`core/tests/test_sphinx_demo.py`): for each of urllib3, trio,
   hydra-zen run the CLI on `core/examples/sphinx/<lib>/notinspec.yaml` into `tmp_path`:
   exit 0; `ingestion.json` identical across two runs; chunks > 0 for every document that
   has text; no `unknown node` warning; `report.html` written. Keep it fast (no `slow`
   marker unless it is above a few seconds).
7. **Eyeball the three reports** (`uv run notinspec ci --config core/examples/sphinx/<lib>/notinspec.yaml --out tmp/<lib>`)
   and write what looks wrong into the PR description (do not fix reader issues in PR B;
   report them to session A or as follow-up issues).
8. Rebase, checks, delete this plan, open PR B ("Sphinx demo: ingestion, report, SPEC").

### Not in scope

Reader internals, chunker, fixtures, example XML (all session A). Storage for uploaded XML
(separate design item for role 5). LLM tasks and evaluation.
