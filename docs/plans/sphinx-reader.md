# Plan — session A: Sphinx 9 reader (`core/sphinx-reader`)

Temporary working plan. Delete this file in the last commit before the PR is merged; the SPEC
is the lasting record. The other half of the work is on branch `core/sphinx-demo`
(`docs/plans/sphinx-demo.md`). The **Shared** part below is identical in both plans.

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

## Session A: the reader

Read first: `docs/SPEC.md` §6.1 (reading and chunking, API reference, field shapes,
determinism), `core/src/notinspec/chunking/` (chunker, blocks, windows), and
`core/examples/sphinx/README.md`.

### What the real XML contains (census, 2026-11-17)

Run `uv run python core/examples/sphinx/census.py core/examples/sphinx/<lib>/xml` to see it.

| | urllib3 | trio | hydra-zen |
|---|---|---|---|
| documents | 21 | 13 | 49 |
| Sphinx | 9.1.0 | 9.1.1 | 9.1.0 |
| `desc` objtypes (all `py`) | method 82, attribute 74, exception 38, class 26, function 24, property 22 | method 180, function 95, class 58, attribute 40, property 20, exception 11, **interface 1**, data 1, decorator 1 | method 22, function 19, class 6 |
| field `name:shape` | Return(type):B 115, Parameters:A 78, Parameters:B 18, Returns:B 13, Raises:B 3 | Returns:B 42, Raises:B 37, Parameters:B 37, Parameters:A 34, Raises:A 22, Return(type):B 16, Type:B 10 | Parameters:C 32, Returns:C 22, Raises:C 6, Attributes:C 3 |
| `rubric` | — | `Example` 6 | Examples 34, Notes 15, References 12, Methods 7, + 8 tab labels |
| `container` | — | — | `literal-block-wrapper` 119 (code with caption), `sd-tab-set` 7, `sd-tab-item` 17, `sd-tab-content` 17 |
| sections with prose after a `desc` | 0 | 6 | 0 |
| absolute `source=` paths | `document` 21 | `document` 13, `literal_block` 23 | `document` 49 |

Other nodes seen: `compact_paragraph`, `inline`, `abbreviation`, `title_reference`,
`literal_strong`, `literal_emphasis`, `doctest_block` (222 in hydra-zen), `classifier`,
`citation` 40, `footnote`, `footnote_reference`, `label`, `seealso`, `glossary`, `caution`,
`attention`, `tip`, `admonition`, `math`, `math_block`, `meta`, `comment`, `index`, `target`,
`compound`, `autosummary_table`, `autosummary_toc`, `tabular_col_spec`, `problematic` (2,
broken refs), `image`, `substitution_definition`, `versionmodified`, `desc_returns`,
`desc_sig_*`.

Verified: two builds from different checkout paths are byte-identical except the absolute
`source=` paths. `defusedxml.ElementTree.parse` (0.7.1, defaults) reads all files (they have a
DOCTYPE with a public DTD id but no internal subset) and rejects an external entity with
`EntitiesForbidden`. The 8 `at 0x…` addresses are static doctest output, not autodoc values.

### Rules (put the final version in code docstrings; B mirrors them in SPEC §6.1)

**Document.** `source` = docname = XML path relative to the XML folder, without `.xml`, POSIX.
`srcdir` = `<document source=…>` minus `<docname>.<suffix>`.

**Hash normalization.** Before hashing, rewrite every `source="…"` attribute value: strip the
`srcdir` prefix; a path outside `srcdir` keeps only its file name and gives a warning. Do it
on the text (regex on the attribute) and hash the result, so the hash never depends on
re-serialization. `build-env.txt` is hashed as is.

**Order inside a section or `desc_content`.** First all own body content in document order,
then nested `desc`s, then subsections. (Docutils already puts subsections last; this only
moves prose that follows a `desc` into the section's own chunk: the 6 trio cases.)

**Structure → blocks**

| Node | Block | Rendering / notes |
|---|---|---|
| `section` + `title` | `heading`, level = depth | `#`×level (max 6) + title text |
| `desc` | `heading`, one level below its parent | title = `desc_name` text (from the first signature), `()` added for function, method, classmethod, staticmethod, decorator. Any domain/objtype is accepted (trio `interface`) |
| `desc_signature` | `signature` (not prose) | whole signature text on one line in backticks; one block per signature |
| `desc_content` | transparent | |
| `paragraph`, `compact_paragraph` | `text` | |
| `bullet_list`, `enumerated_list`, `definition_list`, `glossary` | `list` (one block, never cut) | `- ` items, nested indented |
| `literal_block`, `doctest_block` | `code`, `lang` = `language` attr (`pycon` for doctest) | fenced; text kept exactly (`xml:space="preserve"`) |
| `container.literal-block-wrapper` | one `code` block | `caption` rendered above the fence, not prose |
| other `container` (`sd-tab-*`, …) | transparent | |
| `rubric` | `text` (never a heading, never splits) | `**Examples**`; tab labels are rubrics too |
| `note`, `warning`, `caution`, `attention`, `tip`, `important`, `hint`, `danger`, `error`, `seealso`, `admonition` | `admonition` (prose) | `Note: …`; generic `admonition` uses its `title` |
| `versionmodified` | `text` | |
| `block_quote` | `quote` | |
| `table`, `autosummary_table` | `table` (never cut) | pipe table, cell text via inline rules |
| `math_block` | `code`, `lang="math"` | |
| `footnote`, `citation` | `text` | `[label] text` |
| `field_list` in a `desc` | one `field` block per entry (below) | |
| `index`, `target`, `comment`, `meta`, `substitution_definition`, `compound` (toctree), `autosummary_toc`, `tabular_col_spec`, `image`, `raw` | ignored | |
| `problematic` | its text | warning `unresolved markup in <source>` |
| anything else | children if it has elements, else text | warning `unknown node <tag> (Nx)`, counted per tag |

**Inline.** `literal`, `literal_strong`, `literal_emphasis`, inline `math` → text in backticks
(a reference wrapping a literal stays one backticked span). `reference`, `pending_xref`,
`emphasis`, `strong`, `inline`, `abbreviation`, `title_reference` → their text, never the
link target (SPEC: intersphinx must not change chunk text). `footnote_reference` → `[label]`.
Whitespace in prose collapses to single spaces.

**Fields** (SPEC §6.1 shapes, confirmed in the census):

| Field name | `Block.field` | kind |
|---|---|---|
| Parameters, Keyword Arguments, Other Parameters, Attributes | `param` | `field` (prose) |
| Returns, Yields | `returns` | `field` (prose) |
| Raises, Warns | `raises` | `field` (prose) |
| Return type, Type | `return-type` / `type` | `signature` (not prose) |
| other | lower-case name | `field` + warning |

- A: `field_body > bullet_list > list_item`: one block per item.
- B: `field_body > paragraph`: one block.
- In A and B: first `literal_strong` = name (Raises: the exception, possibly inside a
  `reference`), `literal_emphasis` and references in the parentheses = type, text after the
  separator = text. The separator is an en dash ` – ` (U+2013; 151× in urllib3 + trio).
  Returns has no name.
- C (numpydoc): `definition_list_item`: `term` = name, `classifier` = type, `definition` =
  text. For Returns/Yields without a classifier, the term is the type and name is `None`.
- Nested paragraphs are joined with a blank line. Rendered as ``- `name` (type) – text``.
- Google style **without** napoleon stays a `definition_list` → plain `list` (SPEC).

### Steps (one branch, commit as you go, one PR)

0. **Done already** (commit on this branch): `core/examples/sphinx/` with XML, `build.sh`,
   `census.py`, licences, `notinspec.yaml`, README.
1. **Contract commit, push early.** Split `chunk_document` into `parse_blocks` +
   `chunk_blocks(BlockDocument)`; new kinds and `Block` fields; `field` and `admonition` in
   `_PROSE_KINDS` (`windows.py`); schema 2 → 3. Existing Markdown tests stay green and chunk
   IDs do not change (`CHUNKER_VERSION` stays 3).
2. **Dependencies:** `uv add --package notinspec defusedxml` and `types-defusedxml` as a dev
   dependency (mypy strict). Commit `uv.lock`.
3. **Reader** in `core/src/notinspec/sphinx/` (e.g. `reader.py` for files, version and hash;
   `render.py` for nodes → lines and blocks; `fields.py` for A/B/C). Pure functions,
   deterministic, no absolute paths in output.
4. **Mini fixture** `core/tests/fixtures/sphinx/project/`, our own code (safe to build
   locally with `uv run --no-project --with sphinx==9.1.1 …`; `build.sh` committed): a tiny
   module documented in reST `:param:`, Google and NumPy style; a guide page with a rubric,
   admonitions, `versionadded`, a table, a code block with a caption, `literalinclude`, a
   section with prose after a `.. function::`, a nested class with methods; one MyST `.md`
   page. Built three times: napoleon / numpydoc / neither → `xml-napoleon/`, `xml-numpydoc/`,
   `xml-plain/`, each with `build-env.txt`.
5. **Tests** (`core/tests/sphinx/`):
   - golden: each fixture build → expected chunks JSON (breadcrumb, kinds, field
     name/type/text); regenerate with an env flag, review the diff
   - XXE file → `SphinxInputError`; `build-env.txt` with 8.x or missing → `SphinxInputError`
   - normalization: copy of a folder with another checkout path → same `files` hashes
   - real examples: all three read without error; **no `unknown node` warnings**; hydra-zen
     gives 63 C-shape field entries with name and type (Returns may have no name); trio's
     6 prose-after-desc paragraphs are in their section's chunk; no chunk text contains
     `/src/`; reading twice gives equal output
6. `.gitattributes`: `core/examples/sphinx/*/xml/** linguist-generated=true -diff` so the
   PR diff stays readable (keep `eol=lf`).
7. Rebase, checks, delete this plan, open PR A ("Sphinx 9 XML reader + example XML").

### Not in scope

Config, ingestion wiring, report, SPEC text (all session B). The parameter name in the NLI
breadcrumb (role 4 builds it from `Block.name` later). `objects.inv`. Any Sphinx other than 9.x.
