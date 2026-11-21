# NOT-IN-SPEC — Specification

**Team project 2026/2027, project no. 8.** Team leader: Ing. William Brach.
Source of requirements: [assignment.md](assignment.md). Design source: team proposal v3 (discussion 2026-10-29 to 10-31). This document is the agreed interpretation of both. Tools, thresholds and numbers marked *candidate* still need to be verified. Undecided points are collected in [§18](#18-open-items).

## 1. What we are building

`notinspec` measures **how well language models can use a piece of software based on its documentation**, and shows **which parts of the documentation cause the failures**.

We test **usage, not just comprehension**. Studies show a large gap between the two: models score >90 % on comprehension questions about a library, yet none reaches 50 % on tasks that use it in code ([arXiv:2605.31478](https://arxiv.org/html/2605.31478)); models know about an API change ~75 % of the time but produce working code only ~43 % of the time ([arXiv:2604.09515](https://arxiv.org/html/2604.09515)); code examples matter most (67 % success with examples only vs. 3 % with descriptions only, [arXiv:2606.03657](https://arxiv.org/html/2606.03657)). So:

- the **target metric is usage** (level L3, for OpenAPI also L4, see [§5](#5-test-levels));
- comprehension levels (L0–L2) are **diagnostics** that explain *why* usage fails;
- a validation track ([§14](#14-validation-outside-ci)) checks that the levels really relate to usage.

Given software documentation (a Sphinx project, Markdown docs, a formal spec such as OpenAPI, a changelog, llms.txt; other documentation generators come in later phases, see [§6.1](#61-reading-and-chunking)), the system:

1. splits it into **chunks** (whole documentation sections) and detects the **components** in each chunk (spec, API reference, examples, prose);
2. builds an **inventory** of what exists in the API (symbols, signatures, parameters, constraints, changes), each fact with its source and confidence;
3. runs **cross-checks** between sources and reports contradictions as **findings**;
4. derives **test items** whose correct answer (**reference**) is computed by a program, never by an LLM; an LLM only writes the natural-language task text;
5. freezes the approved test items as a **golden set**, versioned in our database;
6. runs the golden set against several models in **three modes** (no context, retrieved context, gold context);
7. evaluates answers by code: parses the model's code/request into a normalized **call record** and compares it with the reference; for OpenAPI operations also **sends the request to a Prism mock** generated from the spec;
8. reports results **per level, model and mode**, failing documentation sections, failure categories and findings, and how all of it changes over time. It does not recommend fixes: the docs author fixes the docs. **Never a single score.**

It ships as:

- a **web service + web UI**: in the MVP **every run happens on our service** and all data is stored there ([§3](#3-architecture));
- a **GitHub Action** (the CI tool), a thin client of the service: it uploads the inputs, comments on PRs and fails the build when a documentation change significantly lowers usage success ([§11](#11-github-action));
- a **scheduled worker** that runs the queued and the nightly / pre-release runs;
- a **CLI** for development and local runs.

### 1.1 What we are *not* building

- **No code execution** except L4 for OpenAPI operations via the Prism mock. SDK sandboxes, CLI execution and stateful mocks are [future development](#163-future-development).
- **We never build the user's Sphinx docs next to secrets.** `sphinx-build` runs the project's code (`conf.py`, autodoc imports the library, `pip install` runs build hooks). So we only read the **built XML** ([§6.1](#61-reading-and-chunking)):
  - **Action:** the user builds the XML in a separate job with no secrets and passes it on as an artifact. Our upload job, which can request the repo's OIDC token for our service, only sends it to us ([§11](#11-github-action)).
  - **Our VM** (worker, API, self-hosted runner): no Sphinx builds at all. The pilot XML is built once in a pinned environment and stored. Uploads accept built inputs only (Sphinx XML, Markdown, OpenAPI), never a Sphinx project. The worker only parses them and never executes anything from them. Prism, which serves an uploaded OpenAPI spec, runs in its own container without secrets or network access ([§12](#12-devops)).
  - If automatic builds of connected projects are ever needed, they run on GitHub-hosted runners, never on the VM.
  - The XML is **untrusted input**: parsed with `defusedxml` (or lxml with `resolve_entities=False`, no network) against XXE and entity bombs.
- **Docs vs. reality is out of scope.** The truth is what the documentation says. Prism validates against the spec, not against a real backend.
- **No single overall score.** Levels L0–L4 are never averaged together.
- **No LLM decides the correct answer.** References are computed deterministically from the inventory and examples.
- **No user accounts** in the MVP. The web UI is read-only. Golden-set review in the MVP is done by our team with the CLI ([§2.5](#25-golden-set-review)), not in the web UI.
- **Public repos only** in the MVP. The web UI is public and has no accounts, so the docs, answers and results of a private repo would be world-readable ([§11](#11-github-action)). Private repos are [future development](#163-future-development).

## 2. Users

The tool is for a team that **owns a software product's documentation** (library, SDK, REST API, CLI) and wants LLM agents and coding assistants to use it correctly.

### 2.1 Personas

| Persona | Who | Wants | Meets the tool in | Gets |
|---|---|---|---|---|
| **P1 · Maintainer** | developer / maintainer, owns the repo and CI | a change must not make the software harder for LLMs to use; fast, cheap runs | CI status check, PR comment | pass / fail, L3 (L4) drop vs. `main`, new findings in changed sections |
| **P2 · Docs author** | technical writer, DevRel, developer writing docs | to know **which section fails and why** | PR comment, HTML report / web UI, golden-set review ([future](#25-golden-set-review)) | worst sections first, findings, sample wrong model answers, diagnosis |
| **P3 · Team lead / product** | tech lead, product owner, platform team | quality over time and before releases; which models the docs are good enough for | nightly / release report, web UI | results per level and model, trend across versions, model comparison |

Both entry points are built: the **GitHub Action** (P1, P2 in PRs) and the **web UI** with results (P2, P3).

### 2.2 Use cases

| Use case | Persona | When | Scope |
|---|---|---|---|
| **UC1 · First audit** | P2, P3 | once, when adopting the tool | whole documentation, generates the golden set, larger review |
| **UC2 · PR check** | P1, P2 | every PR changing code or docs | only changed chunks and their test items, small models, fast and cheap |
| **UC3 · Nightly / pre-release** | P1, P3 | nightly or before a release | full golden set, also large models, full report |
| **UC4 · Model selection** | P3 | occasionally | same golden set on several models, comparison |

### 2.3 What the tool needs from the user

1. A **config file in the repo** (`notinspec.yaml`, shape is a candidate):
   ```yaml
   project: "urllib3"                 # root of every breadcrumb; default: the repo name
   docs:
     sphinx_xml: "build/xml/"         # output of `sphinx-build -b xml`, built by the user (§1.1)
     paths: ["README.md", "guides/**/*.md"]   # plain Markdown outside the Sphinx project, optional
     openapi: "api/openapi.yaml"      # optional
     changelog: "CHANGELOG.md"        # optional
     version: "2.0"
   formats: [python, curl]            # answer formats for L3
   models:
     pr: [small-model]                # UC2
     nightly: [small-model, large-model]   # UC3
   budget:
     max_cost_per_pr_eur: 0.5
   thresholds:
     fail_on_l3_drop: significant     # statistically significant drop
     fail_on_new_findings: [K1, K4, K7]
     candidates_min_success: 0.6      # absolute floor for PR candidates (§7); warn-only in the MVP
   ```
   The config is uploaded with the inputs. In the MVP our service caps `models` and `budget` by the project's limits ([§11](#11-github-action)).
2. For Sphinx docs: a **CI job that builds the XML** without secrets (`sphinx-build -b xml`) with **Sphinx 9.x** (the only version the MVP reads), and records its build environment in **`build-env.txt`** in the XML folder. The file is **required**: its first line is the output of `sphinx-build --version` (`sphinx-build 9.1.0`), followed by `python --version` and `pip freeze`. A missing file or another Sphinx major version is an error (exit 2). `action/README.md` has the example workflow.
3. The repo is **public** and **registered as a project** on our service ([§11](#11-github-action)). No model API key: in the MVP every LLM call runs on our service ([§8](#8-models)).
4. Nothing to review in the MVP: our team reviews the golden set ([§2.5](#25-golden-set-review)).

### 2.4 What the tool returns

| Output | For | Format |
|---|---|---|
| CI status check | P1 | pass / fail + reason |
| PR comment | P1, P2 | short summary: score change, new findings, links to sections |
| HTML report / web UI | P2, P3 | worst sections first, symbol profile, sample answers, diagnosis, trend |
| JSON results | integrations | machine-readable results and findings, from our API |
| golden set | P2 | in our database, shown in the web UI, exportable as files ([§10](#10-data)) |

Example PR comment (UC2):
```text
NOT-IN-SPEC · 3 changed sections · 2 models · 0.18 €
✗ L3 docs/client.md > Connecting > connect()   91 % → 64 % (p = 0.01)
  most common error: wrong arguments – timeout given in ms
✗ new finding K4: example in docs/retry.md uses removed parameter retries
✓ L3 docs/orders.md, L4 POST /orders unchanged
```

### 2.5 Golden-set review

Review is the biggest adoption risk. To keep it small:

- auto-approve items whose reference comes deterministically from high-confidence objects (spec, signature);
- send for review only low-confidence items (from claims, from changelog changes, variations without a signature) plus a random sample of the rest;
- in UC2 show only items for changed sections;
- in UC1 split the review into batches by section.

**Who reviews.** In the MVP **our team** reviews, to check that the pipeline produces correct items; nobody outside the team does. The review uses the CLI on our service (*candidate:* export the pending items to a file, import the decisions), so the web UI stays read-only and needs no accounts ([§1.1](#11-what-we-are-not-building)). Every decision is stored with the reviewer and the time ([§10](#10-data)).

**Future (not decided):** the docs owners review their own project's items in the web UI, signed in with their GitHub account, with the right to review taken from the repo's permissions (e.g. push access). See [§16.3](#163-future-development).

## 3. Architecture

```
               ┌───────────────────────── core (Python package `notinspec`) ─────────────────────────┐
 docs, spec, ─►│ chunking ─► components A–D ─► inventory ─► cross-checks ─► symbol profiles          │
 changelog     │                                    │            │                │                 │
               │                                    ▼            ▼                ▼                 │
               │                               findings ◄────────────── test items (golden set)     │
               │                                                                  │                 │
               │                        runner (models × modes) ─► evaluation (+ Prism) ─► report    │
               └────▲──────────────────▲─────────────────────▲─────────────────────────────────────┘
                    │                  │                     │
                  CLI          FastAPI service             worker
              (dev, tests)     ▲    │       │          (APScheduler)
                               │    ▼       ▼                │
 GitHub Action ────────────────┘ web UI PostgreSQL ◄─────────┘
 (uploads inputs with OIDC,     (read-only)  (everything)
  waits for the result)
```

- **All logic lives in `core`.** CLI, API, worker and Action are thin wrappers.
- **Hosted-only MVP:** every run (UC1–UC4) happens on our service. The API accepts the inputs and queues a run, the worker runs `core` on it, and **PostgreSQL on our VM holds everything**: inputs, chunks, inventory, golden set, raw LLM responses, results ([§10](#10-data)). The GitHub Action computes nothing; it uploads the inputs and waits for the result ([§11](#11-github-action)).
- The **CLI** runs the same pipeline locally with files in and JSON out, for development and tests. In the MVP it is not a supported way to run the CI check.
- A self-contained Action that runs `core` in the caller's CI with the caller's own key and no dependency on our service is [future development](#163-future-development).

## 4. Glossary

These exact terms are used in code, diagrams and text.

| Term | DB model | Meaning |
|---|---|---|
| **Chunk** | `Chunk` | one whole documentation section split by headings, or one API description (`desc` node) in API reference (no small token limit, code blocks and tables intact, oversized sections split at a soft limit). Identity = source + heading path; a content hash tells whether it changed. Has a breadcrumb. Unit for component detection, inventory, `Source`, gold context, IDs and CI diffs. |
| **NLI premise** | – | the text a claim is checked against: the chunk's breadcrumb plus the cited sentence(s) ±1 sentence within the cited prose block (for a list item, plus the sentence that introduces the list). Computed from the chunk and the citation, not stored. |
| **Recall window** | – | `<breadcrumb>:` + consecutive prose sentences of a chunk, up to a token limit, with overlap. Used only where a missed entailment is the worse error: the unsupported check of the perturbation operator ([§6.7](#67-tasks-and-operators)). Computed from the chunk, not stored. |
| **Component** | – | kind of content in a chunk: **A** formal spec, **B** API reference, **C** examples, **D** prose and changelog. One chunk can contain several. |
| **Symbol** | `Symbol` | anything callable: function, method, class, endpoint, CLI command |
| **Signature** | `Signature` | header of a symbol: parameters and return type, no body. A symbol can have several (overloads, versions). |
| **Parameter** | `Parameter` | one input of a signature: name, type, required / optional, default |
| **Constraint** | `Constraint` | rule for a parameter value: enum, range, unit, format |
| **Return type** | `ReturnType` | what a symbol returns; used by the composition operator |
| **Change** | `Change` | addition, deprecation or removal of a symbol or parameter in a version, optionally with its replacement (a rename is a deprecation or removal with a replacement). A deprecated symbol still exists and works. |
| **Source** | `Source` | where a fact comes from (chunk, source type) and with what confidence; attached to every inventory object |
| **Inventory** | – | composition of `Symbol`, `Signature`, `Parameter`, `Constraint`, `ReturnType`, `Change`, `Source` = what exists in the API |
| **API reference** | – | the part of the docs describing signatures (parameter tables, docstrings, JSDoc); component B |
| **Example** | `Example` | a code block from the docs. Identity = chunk ID + its position among the chunk's code blocks, so an edit inside the code keeps the ID, as for chunks; a content hash tells that it changed. |
| **Adapter** | – | parser + normalization for one language or format (Python, tree-sitter languages, curl, CLI) |
| **Call record** | `CallRecord` | normalized call: symbol + named arguments. Built from examples and from model answers, in the same shape. |
| **Claim** | `Claim` | atomic fact from prose or changelog with a citation, verified by NLI grounding. Type *fact* or *change*. |
| **Grounding** | – | NLI check that a claim follows from its chunk (premise = the NLI premise around the claim's citation, hypothesis = claim) |
| **Cross-check** | – | comparison of two sources (K1–K7); a contradiction is a finding |
| **Operator** | – | rule that turns a call record or signature into a new reference: copy, adaptation, variation, composition, migration |
| **Reference** | `Reference` | the correct answer of a test item, computed by a program, not by an LLM |
| **Task text** | – | natural-language wording of a task, written by an LLM for an existing reference |
| **Test item** | `TestItem` | question or task at level L0–L4 + reference + metadata. Identity key: [§10](#10-data). |
| **Golden set** | – | approved and frozen set of test items, versioned in our database ([§10](#10-data)) |
| **Symbol profile** | – | which levels L0–L4 can be tested for a symbol, and the results |
| **Finding** | `Finding` | a problem in the documentation, reported to the author |

## 5. Test levels

| Level | Tests | Source | Format | Evaluation |
|---|---|---|---|---|
| **L0 Recognition** | does this symbol / parameter exist (in version X)? | `Symbol`, `Parameter`, `Change` | yes/no, 4 options | exact match |
| **L1 Recall** | path, required parameters, defaults | `Signature`, `Parameter` | open answer | path correctness + Jaccard of parameters |
| **L2 Comprehension** | behaviour, constraints, "not in the documentation" | `Claim`; "not in the documentation" from claims changed by the perturbation operator ([§6.7](#67-tasks-and-operators)) | questions | normalization → NLI → LLM judge |
| **L3 Usage** | can it write the call / code that reaches the goal? | `CallRecord`, `Signature`, `Parameter`, `Constraint`, `ReturnType`, `Change` | task → code / request | call-record comparison + error category |
| **L4 Execution** *(OpenAPI only)* | the request is valid per the spec | L3 tasks for OpenAPI operations | task → HTTP request | Prism mock validates the request |

The level framework is inspired by [arXiv:2605.31478](https://arxiv.org/html/2605.31478). **The CI gate is L3 (and L4 for OpenAPI).**

## 6. Pipeline

### 6.1 Reading and chunking

**Readers.** Documentation generators are supported in phases. Every reader produces the same `Chunk`s, so everything after this step does not care where the docs came from.

| Phase | Input | How it is read |
|---|---|---|
| MVP | **Sphinx 9.x** project | from Sphinx's **structured output** built by the user (`sphinx-build -b xml`, i.e. the docutils doctree; never built by us, [§1.1](#11-what-we-are-not-building)), not from rendered HTML and not with our own reST/MyST parser. Sections, code blocks (`literal_block`), tables and API descriptions (`desc` nodes, input for component B) come already typed from the tree. Only Sphinx 9.x, read from the first line of `build-env.txt` ([§2.3](#23-what-the-tool-needs-from-the-user)); other versions are [future work](#163-future-development). `objects.inv` as the list of documented symbols is a *candidate*. |
| MVP | plain Markdown, llms.txt, changelog | Markdown parser |
| MVP | formal spec (OpenAPI) | its own parser (component A); `description` texts become chunks for component D |
| next iteration | other generators (*candidates:* MkDocs, Docusaurus, TypeDoc) | their structured output where they have one |
| future | docs websites without a supported generator | rendered HTML → Markdown (*candidates:* `trafilatura`, `markitdown`) |

**Chunks = sections.**

- A `Chunk` is **one whole section**: split **by headings**, a section runs from its heading to the next heading. **No small token limit.**
- Code blocks and tables are **never split**.
- **Soft-limit fallback:** a section over a soft limit (*candidate:* ~2,000 tokens) is split at paragraph boundaries, never inside a code block or table. The parts keep the section's breadcrumb.
- **Breadcrumb** = `project` from the config + the heading path, e.g. `urllib3 > User Guide > Using Timeouts`. The file path is not part of it; it goes to `Source`. The breadcrumb helps NLI ([§6.4](#64-prose-and-changelog--claim)).
- **Identity** = hash of source + heading path (+ part, + occurrence for repeated headings), so fixing a typo keeps the chunk and everything derived from it. A separate **content hash** tells that the chunk changed (CI diff, regenerating its test items).
- A parent section's **intro** (text between its heading and the first sub-heading) is the parent's own chunk. It is not copied into the subsections; they get their context from the breadcrumb. A heading with no text of its own gives no chunk.
- **Split sections:** the parts exist only for size. Gold context, retrieval results and `Source` always use the **whole section** (all its parts).
- Sections are the unit for **component detection, the inventory `Source`, gold context, IDs and CI diffs**.
- Output: `Chunk`.

**Sphinx XML → blocks.** The Sphinx reader turns the doctree **straight into typed blocks**; it never converts XML to Markdown and parses that again. A round trip would lose node types (a `desc_signature` would become plain text), break on prose that looks like Markdown (`*args`, a line starting with `#`), and could not express one block per parameter. The Markdown reader stays for Markdown inputs (README, llms.txt, changelogs, guides next to an OpenAPI spec).

- `source` of a Sphinx chunk is the **docname**: the XML path relative to the XML folder, without `.xml` (`reference-core`, `generated/hydra_zen.builds`).
- The chunk **text** is rendered, Markdown-like and **read-only**: `#` headings, inline code in backticks, `- ` list items, fenced code, pipe tables. It exists for display and citations, and block line ranges point into it; it is never parsed again.
- Block kinds: the Markdown ones (`heading`, `text`, `code`, `table`, `list`, `quote`) plus **`admonition`** (prose), **`signature`** (not prose) and **`field`** (prose; carries `name`, `field` and `type`, see below).
- Nodes in short:

  | Node | Block |
  |---|---|
  | `section` + `title` | `heading` (level = depth) |
  | `desc` | `heading` one level below its parent; title = `desc_name`, `()` added for functions, methods and decorators; any domain and object type |
  | `desc_signature` | `signature`, one per signature |
  | `paragraph`, `footnote`, `citation` | `text` |
  | `versionmodified` (`deprecated`, `versionadded`, `versionchanged`, `versionremoved` directives) | `text`, which also keeps the directive's `type` and `version` as input for `Change` ([§6.3](#63-inventory)). Inside a parameter entry the `field` block keeps them. |
  | `bullet_list`, `enumerated_list`, `definition_list`, `glossary` | `list` (never cut) |
  | `literal_block`, `doctest_block`, `math_block`, `container.literal-block-wrapper` (caption above the code) | `code` (never cut) |
  | `table`, `autosummary_table` | `table` (never cut) |
  | `block_quote` | `quote` |
  | `note`, `warning`, `seealso`, generic `admonition`, … | `admonition` |
  | `rubric` (`Examples`, `Notes`, tab labels) | `text` in bold, **never a heading**: it does not start a section |
  | `field_list` in a `desc` | one `field` or `signature` block per entry (below) |
  | `index`, `target`, `comment`, `meta`, `substitution_definition`, toctree `compound`, `autosummary_toc`, `image`, `raw` | ignored |
  | other `container`s, `desc_content` | transparent |
  | anything else | its children or text are kept, with a warning `unknown node <tag> (Nx)` |

- Inline: `literal` and inline `math` → backticks; links and cross-references → their text, never their target; `footnote_reference` → `[label]`. Whitespace in prose collapses.
- **Order inside a section or `desc_content`:** first all its own body content in document order, then nested `desc`s, then subsections. Prose that follows a `desc` in the source therefore stays in the section's own chunk instead of being attached to the last API description.

**API reference (Sphinx `desc` nodes).** A page like `automodule :members:` is one heading for a whole module, so heading-based chunks would be huge and the soft limit would cut them at random paragraphs. Instead:

- **Each `desc` node** (function, class, method, attribute) is its own chunk, with the symbol in the breadcrumb: `urllib3 > API Reference > Retry > sleep()`. A nested `desc` (method in a class) is a chunk of its own; the class chunk keeps only the class's own text.
- Node rules inside a `desc` (the same for reST `:param:`, Google and NumPy docstrings, because Sphinx produces the same node types; we never parse docstring styles ourselves):

  | Node | Rule |
  |---|---|
  | `desc_signature` | not prose → component B |
  | `desc_content` → `paragraph`, `note` / `warning`, `versionmodified` | prose, as in a normal section |
  | `desc_content` → `literal_block`, `doctest_block` | code → component C |
  | `field_list` → one parameter / `Raises` / `Returns` entry | **its own prose block** (`field`); its NLI premise adds the parameter name to the breadcrumb (`urllib3 > API Reference > Retry > total`) |
  | `field_list` → `Return type`, types in parentheses | not prose → component B |

- The reader normalizes the three XML shapes of a field entry into one block (kind, name, type, text):

  | Shape | From | XML |
  |---|---|---|
  | A | reST or napoleon, several params | `field_body > bullet_list > list_item > paragraph`: `literal_strong` name, `literal_emphasis` type, ` – ` (en dash), text |
  | B | reST or napoleon, one param | `field_body > paragraph`, no `bullet_list` |
  | C | numpydoc | `field_body > definition_list > item`: `term` = name, `classifier` = type, `definition` = text |

  All text after the dash (A, B) or in the `definition` (C) is one block; nested paragraphs are joined with a blank line. A `Returns` entry has no name (in C, a term without a classifier is the type). The entry is rendered as ``- `name` (type) – text``. Each group of entries starts with a **label line** (`**Parameters:**`, `**Raises:**`): a `text` block that the chunker keeps in the same part as the first entry after it, so a split never leaves a label alone at the end of a part.
- Field names map to the block's `field`: Parameters, Keyword Arguments, Other Parameters, Attributes → `param`; Returns, Yields → `returns`; Raises, Warns → `raises` (all `field` blocks, prose); Return type → `return-type` and Type → `type` (`signature` blocks, not prose). Any other field name is a `field` block with the lower-case name and a warning.
- **Google style without napoleon** stays a `definition_list` (`Args:` term, all parameters in one paragraph) and is read as plain prose: the text is kept, only the per-parameter split is lost. We do not inject napoleon into the user's `conf.py`: it changes the docs vs. what the project publishes.

**Determinism of Sphinx input.** Autodoc output depends on the Sphinx version, its extensions and the installed library, so the same docs commit can build to different XML.

- The reader's input is the **built XML**: its hash (every `*.xml` in the folder and `build-env.txt`, sorted by path) is the input snapshot hash ([§10](#10-data)). Other build output (`_static/` scripts and CSS) is not documentation and is neither read nor hashed. Same XML + reader version ⇒ same chunks and IDs; the Sphinx version and the reader version are stored with every run (`ingestion.json`: `sphinx`).
- The XML contains the absolute path of the build's checkout in `source="…"` attributes (on `document`, and on `literal_block` from `literalinclude`), so the same docs built in another folder would hash differently. Before hashing, the reader strips the source-folder prefix from every `source=` value (a path outside the source folder keeps only its file name, with a warning). This is done on the file text, so the hash never depends on XML re-serialization. Verified on the three example libraries: two builds from different checkout paths differ only in these paths.
- The **build environment** (`build-env.txt`, [§2.3](#23-what-the-tool-needs-from-the-user)) is stored with every run, so a change in chunks can be traced to a change in the environment.
- The reader takes the text of links, never their targets, so intersphinx (which fetches `objects.inv` from the network at build time) does not change the chunk text.

**Prose and NLI premises.** NLI never sees a whole section: the model accepts only a few hundred tokens, and a long premise dilutes negations and numbers.

- **Prose** = paragraphs, list items and admonitions (notes, warnings), including those inside API descriptions (`desc_content`, parameter entries; see the table above). Inline code inside them counts as prose text. Code blocks, tables, signatures and types are not prose.
- The **NLI premise** for a claim is `<breadcrumb>:` followed by the cited sentence(s) ±1 sentence, **within the cited prose block**. For a list item, the sentence that introduces the list (the last sentence of the paragraph before it, ending with ":") is put in front.
- The premise is computed deterministically from the chunk and the citation, so it needs no storage of its own. Use in grounding: [§6.4](#64-prose-and-changelog--claim).
- Evidence: `experiments/nli/FINDINGS.md` (runs 004–007, human-labelled sample). On a human-labelled sample, a 400-token window instead of this premise kept nearly twice as many wrong claims (22 vs 12 of 88) and claims from other sections (38 vs 23 of 259).

### 6.2 Components and techniques

A component detector finds **all** components present in each chunk (file extension, code-block language, Sphinx node types, Markdown structure). Each goes its own way in parallel; there is no either/or.

| Component | What | Technique | Output |
|---|---|---|---|
| **A · Formal spec** | OpenAPI, GraphQL schema, `.proto`, JSON Schema | spec parser (YAML/JSON, `graphql-core`, protobuf), deterministic. `description` texts go to D. For OpenAPI a Prism mock is also started. | `Symbol`, `Signature`, `Parameter`, `Constraint`, `ReturnType`, `Change` (`deprecated`) |
| **B · API reference** | signatures, parameter tables, docstrings, JSDoc, Sphinx API descriptions (`py:function`, autodoc) | Sphinx `desc` nodes, signature parser (`ast` / tree-sitter) and table parser, deterministic | `Symbol`, `Signature`, `Parameter`, `Constraint`, `ReturnType`; `Change` from Sphinx version directives ([§6.3](#63-inventory)) |
| **C · Examples** | code blocks in any language or format | `Example` → language adapter → normalization using the inventory (variable → class, positional argument → `Parameter`). Invalid code is dropped (`Finding`). | `Example`, `CallRecord`; into the inventory only missing `Symbol` and `Parameter` |
| **D · Prose and changelog** | guides, concepts, changelog, spec `description` | claim extractor (LLM) → grounding (NLI) → K5a, K5b (NLI) | `Claim`; a *change* claim yields a `Change` |

Nothing is extracted from prose directly by an LLM without NLI grounding: everything from prose goes through `Claim`.

Adapters for component C:

| Language / format | Parser | Note |
|---|---|---|
| Python | `ast` | variable type by heuristics from assignments and imports |
| JS, TS, PHP, Ruby | tree-sitter | JS: options object = named arguments |
| Java, C#, Go | tree-sitter | type from declaration, overloads by argument count and types, builder, functional options |
| curl / HTTP | `shlex` + `json` | path → template `/orders/{id}`, query vs. body vs. headers |
| CLI | `shlex` | flag alias mapping |
| YAML / JSON config | `yaml` / `json` | keys and values |

MVP adapters: **Python `ast` + curl**.

### 6.3 Inventory

```
Symbol
 ├─ 1:n  Signature
 │        ├─ 1:n  Parameter
 │        │        └─ 1:n  Constraint
 │        └─ 1:1  ReturnType
 └─ 1:n  Change
Source  – attached to every object above
```

| Written by | Objects | `Source` |
|---|---|---|
| A · spec parser | `Symbol`, `Signature`, `Parameter`, `Constraint`, `ReturnType`, `Change` | spec, high confidence |
| B · signature and table parser | `Symbol`, `Signature`, `Parameter`, `Constraint`, `ReturnType`; `Change` from version directives (below) | signature, high confidence |
| C · example normalization | `Symbol`, `Parameter`, only if not yet in the inventory | example, medium confidence |
| D · *change* claim | `Change` | changelog, low confidence → review by our team ([§2.5](#25-golden-set-review)) |

- **Merge:** objects of the same symbol from several sources are merged with priority **spec > signature > example > changelog**. A disagreement between sources is a `Finding`.

**`Change`:**

- **Kind = the status of the name** the `Change` is about: `added`, `deprecated` or `removed`. A `deprecated` symbol or parameter still exists and works. For example, `format_header_param()` in urllib3 2.x is deprecated, so the L0 question "does it exist in 2.0?" has the answer yes.
- **Attributes** (optional): `replacement` (the symbol or parameter to use instead) and `removal_planned` (a version).
- **A rename is not a kind.** It is a `Change` of the **old name** with the new name as `replacement`:
  - if the old name keeps working (an alias), the kind is `deprecated`;
  - otherwise it is `removed`.
  
  Code decides between the two, not the extractor: `deprecated` if the old name is still in the inventory of that version, otherwise `removed` (what the docs do not describe does not exist for us, [§1.1](#11-what-we-are-not-building)). "Renamed from A and B" on the new symbol therefore gives one `Change` per old name, keyed by the old name.
- **Key:** symbol + parameter (if any) + kind + version, where the symbol and parameter are always the old name. The version is taken from the directive, or from the changelog heading it is under (`2.0.0 (2023-04-26)` → `2.0.0`), and compared as a PEP 440 `Version` (`2.0 == 2.0.0`).
- **Merge:** objects with the same key from several sources merge into one `Change` with several `Source`s. In urllib3 2.0.0, `format_header_param` is mentioned three times: its `deprecated` directive ("Renamed to `format_multipart_header_param()`"), the `versionchanged` on the new name ("Renamed from `format_header_param_html5` and `format_header_param`") and the changelog ("Deprecated … in favor of …"). All three have the key (`format_header_param`, `deprecated`, 2.0.0) and become one `Change`.
- **Review of a *change* claim** (D, [§2.5](#25-golden-set-review)):
  - If its key matches a `Change` from a version directive, the **key** needs no review: the directive confirms that the change exists. It does not confirm the attributes the LLM extracted.
  - `replacement` is accepted without review only if code finds it in the inventory **and** in the claim's citation. Otherwise it goes to review, because it feeds the references of the migration operator ([§6.7](#67-tasks-and-operators)).
  - Other attributes (`removal_planned`) and claims that match no directive go to review.
- Under the same key, attributes that disagree are a `Finding`. A real case is urllib3 2.x: its API reference says `RequestField`'s `header_formatter` "will be removed in urllib3 v3.0", while the changelog says "in urllib3 v2.1.0". Both sides are claims: on the class this deprecation is a `versionchanged`, which gives no `Change` by itself (below).
- **From Sphinx version directives** (component B, deterministic). For `deprecated`, `versionadded` and `versionremoved`, code reads:
  - the kind (`deprecated` / `added` / `removed`) and the version;
  - the symbol: the enclosing `desc`;
  - the parameter: the parameter entry the directive sits in. numpydoc puts it there (e.g. hydra-zen's `builds(frozen=…)`). Otherwise there is no parameter.
- **What a version directive does not give:**
  - Anything said only in the directive's text: the replacement or rename target ("Renamed to `format_multipart_header_param()`"), a parameter named only in prose (urllib3's `header_formatter` sits on the class) and the planned removal version. These come only through a *change* claim (D).
  - **`versionchanged` gives no `Change`.** It is free text about any kind of change: of its three uses in urllib3, one is a deprecation, one a rename and one a change in behaviour. Its text goes to claims (D) like any prose.
- Verified on the three example libraries: urllib3 has 3 `deprecated` and 3 `versionchanged`, hydra-zen has 6 `deprecated` (5 on parameters), trio has none. The big urllib3 changes (`Retry(method_whitelist=…)` → `allowed_methods`, removed in 2.0) are only in the changelog, so D is needed anyway.
- **Outside the inventory:** `Chunk`, `Example`, `CallRecord`, `Claim`, `Finding`, `TestItem`, `Reference`. The composition graph is built from `ReturnType` and the data flow in call records.

### 6.4 Prose and changelog → `Claim`

1. **Claim extractor** (LLM; 2 extractors with different models or prompts, [§8](#8-models)): reads the **whole chunk** (section) and returns atomic, self-contained claims, each with a **citation** (exact quoted span from the chunk). Type *fact* or *change*. A chunk without prose is not sent. The claims of a chunk are reused while its text, breadcrumb, extractor model, prompt version and reasoning effort stay the same (`notinspec.claims`). Deterministic citation check on normalized text (whitespace collapsed, Markdown markup and backticks removed, typographic quotes → plain quotes, en and em dashes → `-`):
   - citation not found in the chunk → drop the claim;
   - citation found only outside prose (code block, table, signature or type) → `not_checkable`, dropped. Facts in code and signatures are covered by components B and C.
2. **Grounding via NLI:** premise = the **NLI premise** around the citation ([§6.1](#61-reading-and-chunking)), hypothesis = claim, decision by argmax. `entailment` → keep. `neutral` / `contradiction` → drop. A citation found more than once in the prose (a docstring repeats sentences across parameter entries) has one premise per match: the entries of a parameter the claim names come first, and among the rest a premise that entails the claim wins over one that does not, then the highest entailment. Then the **identifier check** ([§18](#18-open-items)): a claim NLI keeps is still dropped (`id_missing`) if its section never names one of its identifiers, numbers or versions. It runs on every claim with a premise, so both checks can be measured on their own. Dropped claims are recorded but **not reused as test material automatically**: NLI also drops some true claims. "Not in the documentation" questions come from the perturbation operator instead ([§6.7](#67-tasks-and-operators)).
3. **K5a · claim vs. claim within a chunk:** extractor A ⇄ B, NLI in both directions. A whole section can yield many claims, so K5a uses the same prefilter as K5b.
4. **K5b · claim vs. claim across chunks:** embedding prefilter so not all pairs are compared, then NLI in both directions.

| A ⇒ B | B ⇒ A | Relation | Action |
|---|---|---|---|
| entailment | entailment | duplicate | merge into one claim |
| neutral | entailment | B is more specific | keep B |
| neutral | neutral | different claims | keep both |
| contradiction | – | contradiction | `Finding`, no tasks from these claims |

5. A *change* claim yields a `Change` (low confidence → review by our team, [§2.5](#25-golden-set-review)). If it matches a `Change` from a version directive, only its key skips the review; its attributes are checked as described in [§6.3](#63-inventory).

NLI = local cross-encoder classifying (premise, hypothesis) → entailment / contradiction / neutral; deterministic, CPU only.

- **Model:** `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` (~0.3–0.6 s per claim on CPU, measured on two PCs; ~1.1 s on our VM: 0.88 pairs/s in the worker limited to 3 CPU, 1.1 pairs/s on all 4 vCPU, batch 8, peak ~3.1 GB RAM in the worker). It was chosen in `experiments/nli`. `notinspec.nli` runs it at a **pinned revision**, always in fp32 (the checkpoint is fp16, ~9× slower on CPU with the same decisions), in batches sorted by length. An input over 512 tokens is cut from the premise, never the claim, and the cut is recorded with the decision. The earlier candidate `cross-encoder/nli-deberta-v3-base` with 400-token windows kept only 60 % of correct claims, failing on list-heavy sections. A multilingual XNLI model for non-English docs remains a *candidate*.
- **Premise:** for grounding it is the NLI premise; for K5 it is a claim. It is never a whole chunk.
- **Recorded with every decision:** the NLI model and its revision, the premise rule, the decision rule (argmax), whether the premise was cut, and the versions of the grounding rules, the sentence splitter and the chunker, so a decision can be reproduced.
- **In code:** `notinspec.claims.run_claims`, and `notinspec claims run` in the CLI. Every claim gets a status: `kept`, `citation_not_found`, `not_checkable`, `nli_neutral`, `nli_contradiction` or `id_missing`. The CLI writes `claims.json` (every claim, dropped ones too, with premise, scores and missing identifiers), `claims.html` for reading by eye, and appends every LLM call to `llm-calls.jsonl`.
- **Watch:** NLI does not reliably check exact identifiers, numbers, versions or tense.

### 6.5 Cross-checks K1–K7

| Check | Between | Question | Technique |
|---|---|---|---|
| **K1** | `CallRecord` ↔ `Signature` | does the call in the example match the signature (existing parameters, argument count, types)? | deterministic |
| **K2** | `Claim` ↔ `Signature` / `Constraint` | does a claim contradict the signature (other default, range)? | NLI |
| **K3** | SDK `CallRecord` ↔ REST `CallRecord` | does the SDK example match the same OpenAPI operation? | deterministic |
| **K4** | `CallRecord` ↔ `Change` | does the example use a removed or replaced symbol / parameter? | deterministic |
| **K5** | `Claim` ↔ `Claim` | duplicates and contradictions within a chunk (K5a) and across chunks (K5b) | NLI both directions |
| **K6** | format ↔ format | does the model manage the task in one format (REST) but not another (SDK)? | comparing model results |
| **K7** | curl `Example` ↔ OpenAPI | is the request from the example valid per the spec? | Prism validation |

Every contradiction is a `Finding`.

### 6.6 Per-symbol decisions

Decisions are made per symbol, never for the whole documentation:

| Question | Yes | No |
|---|---|---|
| Has a `Signature` with source spec or signature? | L0 · L1 deterministic; adaptation, variation, composition automatic | L0 · L1 only from call records; variation and composition only after review |
| Has a verified `Example` with a `CallRecord`? | L3: copy, adaptation + leave-one-out | with a signature: L3 from the signature only. With nothing: L3 unavailable → `Finding` |
| Has a `Claim`? | L2 questions, plus "not in the documentation" questions via perturbation | – |
| Has a `Change`? | L0 distractors only from names **removed** in or before the version asked about (a deprecated name still exists, so it would be a second correct answer); L3 migration | – |
| Is it an OpenAPI operation? | **L4 via Prism mock** | L3 by call-record comparison only |

The result is the **symbol profile**, from which test items and references are created.

### 6.7 Tasks and operators

An operator takes a call record or signature and a program computes a new reference:

| Operator | Does | Needs |
|---|---|---|
| **copy** | reference = call record from the example | `CallRecord` |
| **adaptation** | other value, boundary value, other unit, back to default | `Parameter`, `Constraint` |
| **variation** | adds a parameter no example uses | `Parameter`, `Constraint` |
| **composition** | joins 2–3 symbols via the graph; the combination must not appear in any example | `ReturnType`, data flow in call records |
| **migration** | old code → new version | `Change` |
| **perturbation** *(L2 only)* | changes one identifier or number in a grounded claim so that the docs no longer support it; reference = "not in the documentation" | `Claim`, `Symbol`, `Parameter` |

Example reference:
```json
{"task": "t_31", "level": "L3", "operator": "adaptation",
 "calls": [{"call": "Client.connect", "args": {"timeout": [120]}}]}
```
Task text (written by an LLM): "Give up connecting after 2 minutes."

- **Leave-one-out:** in gold-context mode, the example the task was derived from is removed, to test whether the rest of the docs is enough.
- **Perturbation ("not in the documentation", L2):** tests whether a model admits that the docs don't say something, instead of inventing an answer.
  1. Code takes a grounded `Claim` and replaces **exactly one** slot: an identifier with another one of the same kind from the inventory (a parameter of the same signature, a method of the same class), or a number / unit with one that does not appear in the claim's chunk. Example: "`total` set to `0` fails on the first retry" → "`backoff_factor` set to `0` fails on the first retry".
  2. **Unsupported check:** NLI with the changed claim as the hypothesis, decision by argmax. Any `entailment` or `contradiction` → the docs say something about it, discard. All `neutral` → keep. Premises:
     - the **NLI premise of the original claim's citation** ([§6.1](#61-reading-and-chunking)): the changed claim keeps the original citation, so this premise is defined;
     - **recall windows** over the whole claim's chunk and over the top *k* chunks most similar to the changed claim (embedding prefilter, as in K5b). A recall window is `<breadcrumb>:` + consecutive prose sentences of one chunk, cut at sentence boundaries, at most 400 tokens (*candidate*) with a 1/5 overlap, so every prose sentence of the chunk is in at least one window. Windows are computed deterministically from the chunk (chunk ID + offset);
     - all grounded claims of the project.

     Here the risk is the opposite of grounding: a missed entailment (false `neutral`) leaves an answerable question, while a false entailment only discards a candidate. So the premise favours **recall**: in `experiments/nli/FINDINGS.md` the 400-token window found support for 90 of 92 correct claims vs. 86 of 92 for the NLI premise. Every decision records the premise rule and window size, as for grounding ([§6.4](#64-prose-and-changelog--claim)).

     The cheap identifier check ([§18](#18-open-items)) also runs: the new identifier or number must not appear in the claim's citation.
  3. The task-text writer (LLM) turns the changed claim into a question ("What happens when `backoff_factor` is set to `0`?"). The reference, "not in the documentation", comes from step 2, not from the LLM.
  4. **Always reviewed** ([§2.5](#25-golden-set-review)): NLI can miss support for a claim (a false `neutral`), and then the question would be answerable.
  - Evaluation: the answer must say that the documentation does not cover it. A concrete answer is an error (`invented`), even if it happens to be true for the real software, because the truth is what the documentation says ([§1.1](#11-what-we-are-not-building)).
- **Difficulty:** explicit (task names the symbol) / semantic (goal only) × single-step / multi-step.
- **Formats:** a task is asked in every format the docs cover (curl, Python SDK, JS SDK…). Comparing formats is K6.
- **`TestItem` metadata:** symbol, chunk, level, operator (distance from the docs), source, 2–3 paraphrases.
- **Determinism:** references are computed by code, so the same input + generator version ⇒ the same references. The LLM-written task text and paraphrases are frozen in the golden set; when docs change, only the affected part is regenerated.

### 6.8 Quality control

Common to all tasks:

1. structure (schema);
2. leakage: a semantic task text contains no symbol or parameter name;
3. every value of the reference appears in the task text (possibly in another unit);
4. the reference satisfies `Parameter` and `Constraint` (types, ranges, enums);
5. the task is not a copy of an example (except the copy operator);
6. **round-trip:** two strong models with gold context (for leave-one-out without the source example) must solve the task, evaluated by the same evaluator;
7. triviality (closed-book success): do not remove, only flag `parametric_known`;
8. deduplication and symbol coverage;
9. review ([§2.5](#25-golden-set-review)) and manual check of a sample (pipeline precision, Cohen's kappa).

If a well-grounded task fails even with gold context, the problem is probably in the documentation text (`Finding`), not in the task.

### 6.9 Modes

| Mode | Context given to the model |
|---|---|
| `none` | nothing (what the model knows from its weights) |
| `retrieved` | chunks found by retrieval (*candidates:* BM25, embeddings, hybrid). Retrieval may embed smaller sub-parts of a section (paragraphs, code blocks), but always returns the **whole section**. |
| `gold` | the chunks (whole sections) the test item was derived from. For leave-one-out only the source example's code block is removed; the rest of the section stays, including the sentence that introduces the example. |

The three modes separate the effect of model weights, text quality and findability.

### 6.10 Evaluation

Every test item × model × mode. **All raw responses are stored.**

- **L0:** exact match, shuffled option order.
- **L1:** path correctness + Jaccard of required parameters (+ defaults).
- **L2:** normalization → NLI (coverage and precision) → **LLM judge** only for borderline cases. For "not in the documentation" items the answer must say the docs don't cover it ([§6.7](#67-tasks-and-operators)).
- **L3:** model answer → the same adapter as for examples → `CallRecord` → comparison with the reference. Error categories:

  | Category | Meaning |
  |---|---|
  | `success` | matches the reference |
  | `wrong-symbol` | calls a different symbol |
  | `wrong-arguments` | right symbol, wrong arguments |
  | `hallucinated-api` | symbol / parameter not in the inventory |
  | `deprecated-api` | symbol / parameter is removed or deprecated per `Change`. The result records which kind. Whether a deprecated one (which still works) can fail the CI gate is open ([§18](#18-open-items)). |
  | `api-bypass` | reaches the goal without the documented API |
  | `invalid-format` | answer cannot be parsed |

- **L4 (OpenAPI only):** the model's HTTP request is sent to a Prism mock started from the spec, which validates path, method, parameters, body, headers and auth. Prism is stateless: multi-step tasks using an `id` from a previous response are checked structurally only.

**Limits without execution:** L3 cannot check semantics (correct call with a wrongly computed value) or stateful procedures. Conceptual documentation without code or signatures yields only L0–L2.

### 6.11 Diagnosis

The report says what a result pattern means. It does not recommend a fix: findings and failures differ too much for a reliable rule, so the docs author decides how to fix them.

| Situation (gold context) | Interpretation |
|---|---|
| L3 OK | docs enable usage |
| L3 bad, L1 bad | unclear signature |
| L3 bad, L1 and L2 OK | missing example or guide ("knows what, not how") |
| L3 bad, category `deprecated-api` | weights override the context |
| copy OK, variation bad | docs work only via copy-paste of examples |
| with example OK, leave-one-out bad | symbol relies on a single example |
| wrong arguments due to a unit | missing unit |
| bad without context, OK with gold | model doesn't know it from weights, docs work |
| OK with gold, bad with retrieved | text is good but hard to find |
| K1 / K4 / K7 finding | example does not match signature or spec |
| K5 contradiction | sections contradict each other |

## 7. CI behaviour and repeated runs

- Non-determinism is handled by paraphrases and repeated runs.
- **Paired comparison with the `main` baseline** (bootstrap or McNemar); the build fails only on a **statistically significant drop**.
- **Main runs:** the workflow also runs on every push to the default branch ([§11](#11-github-action)) with the PR (small) models. These *main runs* are the baseline for PRs and the source of truth for the golden set ([§10](#10-data)).
- **Baseline of a PR** = the main run of the **first parent of the PR's merge commit**. The merge commit is what is tested (the OIDC `sha`), and its first parent is exactly what the PR was merged onto, so the difference between them is only the PR. `pull_request.base.sha` from the event does not guarantee this: GitHub recomputes the merge ref outside of events, so the two can drift apart. The client sends the first parent for lookup only, never as proof ([§11](#11-github-action)).
  - Pairs need the same golden-set version, model and mode. The worker fills in missing (item, model) pairs from the stored inputs of that main run.
  - No main run for that commit → the nearest main run with the same golden-set version, and the PR comment says so.
  - No baseline at all → "no baseline", and only absolute floors apply. When a project is registered, its first main run is started with `workflow_dispatch`.
  - Nightly runs with large models are a separate series and never a PR baseline.
- **Items in changed chunks:** the worker recomputes the reference of every existing item against the PR's inventory (by code, no LLM):
  - reference unchanged → **stable**: paired with the baseline, can fail the build;
  - reference changed, or the symbol is gone → **superseded** in this PR: left out of the paired comparison, and its candidate replacement is evaluated instead. Example: a PR renames `retries` to `retry_policy` in code and docs; the old reference would turn correct answers into a false drop.
- **Candidates** ([§10](#10-data)) have no paired baseline, so they are checked against an absolute floor (`thresholds.candidates_min_success`). In the MVP the floor only **warns** and never fails the build: low-confidence candidates are not reviewed yet and can be wrong.
- Fail conditions (configurable): L3 (and L4) drop on stable items in changed sections; a new finding from selected cross-checks.
- Thresholds live in the config file in the repo.
- **Cost:** small models on every PR, large models nightly or before a release, only items affected by the diff, reuse of frozen items ([§10](#10-data)), response cache.
- **Repeated runs:** the worker runs the full golden set of every registered project **nightly**, on the inputs of its latest main run, stores every raw response, diffs against the previous nightly run and sends a **Slack alert** on a significant drop.
- Runs are **resumable**: if rate limits stop a run, the worker continues it later.

## 8. Models

- **LLM access:** the **claim extractors** run on the **FIIT LiteLLM proxy** (since 2026-11-21, from our supervisor; [docs](https://fiit-ba.github.io/docs/litellm-quickstart/)) at `https://litellm.blockfinlab.xyz/v1`, key `FIIT_API_KEY`. **Models under test** still run on [Groq](https://console.groq.com/docs/openai) (free tier) at `https://api.groq.com/openai/v1`, key `GROQ_API_KEY`; they move to the proxy later, with as many models as we can get, the weak ones above all. Keys only in env / secrets. The client in `core` (`notinspec.runner`) speaks any OpenAI-compatible API: a provider is a config entry (base URL, key variable, limits, timeout, allowed models), and OpenRouter is kept as a third one.
- **FIIT proxy: only the free local models.** The whole team shares one key with a budget (100, of which 31.27 was spent on 2026-11-21), and the paid models (the Claude, GPT and OpenRouter aliases) draw from it; `openrouter-free` costs nothing but may log prompts. The local models `qwen3.8-flash-next` (vLLM, `nvidia/Qwen3.8-Flash-Next-NVFP4`) and `gemma4-26b-a4b-hpc` (llama.cpp, Gemma 4 26B-A4B, 4-bit) did not change the spend. So the provider allows only these two (`FIIT.allowed_models`), and a request for any other model fails before it is sent, with a message that says why. Allowing a paid model is a team decision ([§18](#18-open-items)).
- **FIIT proxy, measured 2026-11-21:** both local models are reasoning models, and both run with **thinking off** (`chat_template_kwargs` `{"enable_thinking": false}`, which the proxy passes to vLLM and llama.cpp) and a completion limit of 16384. On `urllib3 > Utilities > Retry`, the chunk Groq cut off at 2048 tokens, qwen gave 54–62 claims (~190 tokens/s) and gemma 57 (~80 tokens/s, about a minute). With thinking on, qwen needed 7.4k tokens for 61 claims, and gemma never finished: it thought 5.5k tokens for one claim on a trivial chunk and ran into 16k with effort `low`. The proxy publishes no rate limits and sends no `x-ratelimit-*` headers; the client-side limiter (20/min, 5 000/day per model) is a guess. The servers are shared: a request waited 1–85 s in the queue, so the timeout is 15 minutes. A timed-out request (no answer within the client's timeout, or HTTP 408/504/524 from the proxy or a gateway) is retried only once, because the server may still be generating the answer its client gave up on. If it times out again, the extractor stops like on a spent budget: its remaining chunks are not asked (cause `timed-out`), so a stuck server does not get one abandoned generation per chunk, and a later run continues from the claims store. A spent key budget (LiteLLM `budget_exceeded`) blocks every model of the key, the free ones too, so it pauses the run; an alias the proxy doesn't serve ("Invalid model name") makes the model unavailable. Structured output (`json_schema`) worked on both.
- **Model under test for now: `qwen/qwen3.8-27b`** (a Groq preview model), the client's default. At least a second model comes later ([§18](#18-open-items)).
- **Limits** count per Groq organization and **per model**. Measured on our free-tier organization from the `x-ratelimit-*` headers (2026-11-17): **1 000 requests/day and 8 000 tokens/min**, the same for `qwen/qwen3.8-27b` and `openai/gpt-oss-20b`. Groq's docs add 30 requests/min and 200 000 tokens/day. Groq also limits **output tokens per minute** (`qwen/qwen3.8-27b`: 1 000, from a 429 body on 2026-11-17); a long answer can block the next request for about a minute. With task prompts of a few thousand tokens, tokens per minute are the real limit, not requests. Each model gets its own client-side limiter, and a `429` whose `retry-after` is long pauses the run instead of waiting.
- **Structured output:** the answer schema is sent as `response_format` `json_schema` in best-effort mode, not `strict` (strict needs every property required, and the answer has optional ones). Groq's docs list it for `openai/gpt-oss-20b`, `openai/gpt-oss-120b`, `openai/gpt-oss-safeguard-20b`, and the previews `qwen/qwen3.8-27b` and `meta-models/muse-spark-open` (Enterprise only, not offered to our organization). **Checked live on `qwen/qwen3.8-27b`:** it accepts our answer schema as it is and kept to it even when the prompt told it not to. Without `response_format` it put the JSON in a Markdown fence and sent no `<think>` block, although qwen3 is a reasoning model. All three answers are recorded in `core/tests/runner/fixtures/groq-qwen.json`. Other chat models (e.g. `allam-2-7b`) get the schema in the prompt only. If a best-effort answer fails the schema, Groq returns HTTP 400 `json_validate_failed`. The client treats that as the model's `malformed-output` (parsed from `failed_generation`), not a provider error. `notinspec models --probe` checks the other models live.
- Groq runs temperature 0 as `1e-8`; we record the 0 we sent.
- In the MVP the key exists **only on our VM**: users do not bring a key, and every LLM call of every project runs in our worker within the project's limits ([§11](#11-github-action)). Users bringing their own key belongs to the self-contained Action ([§16.3](#163-future-development)).
- Roles of LLM calls: models under test (small for PRs, large for nightly), 2 claim extractors (`qwen3.8-flash-next` and `gemma4-26b-a4b-hpc` on the FIIT proxy, see above; until 2026-11-21 `qwen/qwen3.8-27b` and `openai/gpt-oss-20b` on Groq, still available as `GROQ_EXTRACTORS` with `--provider groq`. Groq's free tier allows qwen 1 000 output tokens per minute and rejects a request it expects to answer with more, so qwen there runs at Groq's default limit of 2048 and long chunks are cut off. gpt-oss is a reasoning model and needs a completion limit of 8192, otherwise Groq often rejected its answer with `json_validate_failed`, recorded in `core/tests/claims/fixtures/`. It runs at reasoning effort `low`: at the default it used ~3.5k tokens per chunk instead of ~1.7k, see `experiments/nli/runs/008-core-pipeline-urllib3-demo`), task-text writer, 2 strong round-trip solvers, LLM judge for borderline L2 answers.
- **Local CPU models:** NLI cross-encoder and embeddings run locally (no GPU on the VM). Models under test are not run locally.
- Every call is recorded with exact model ID, temperature (0) and all parameters, plus token usage and cost.
- The client is rate-limit aware (queue, backoff on 429) and caches responses by (run ID, model, prompt hash) so a resumed run never re-asks. The cache never crosses runs, otherwise change over time could not be measured. This applies to **models under test**. Generation reuses frozen test items by their identity key ([§10](#10-data)); that is not a response cache.
- A model that disappears is a normal, displayed state, not an error.

## 9. Stack

| Area | Choice |
|---|---|
| Language | Python 3.12+ (core, API, worker), TypeScript (web) |
| Packaging / tooling | uv, ruff, mypy (core), pytest, pre-commit |
| API | FastAPI; its generated OpenAPI is validated in CI |
| Reading docs | Sphinx XML (`xml` builder / docutils doctree, built by the user) parsed with `defusedxml`, `objects.inv` (*candidate*) in the MVP; `markitdown`, `trafilatura` later (*candidates*) |
| Parsers | Python `ast`, tree-sitter, `shlex`, `json`, `yaml`, `graphql-core`, protobuf |
| Spec tooling | OpenAPI 3.x + JSON Schema, **Prism** (mock server, L4 and K7), **Schemathesis** (tests our own API) |
| NLI / embeddings | `transformers` sequence classification with `DeBERTa-v3-large-mnli-fever-anli-ling-wanli` (grounding, K5), fp32, pinned revision; optional extra `notinspec[nli]` (torch CPU wheels), in-process in the worker, not installed in CI; mDeBERTa XNLI, `all-MiniLM-L6-v2` (*candidates*); CPU only |
| LLM access | FIIT LiteLLM proxy (claim extractors) and Groq free tier (models under test) through their OpenAI-compatible APIs, our own client on `httpx2` (no vendor SDK); recorded fake provider in tests and CI |
| Evaluation / statistics | scikit-learn, bootstrap, McNemar test |
| Database | PostgreSQL, SQLAlchemy 2, Alembic |
| Scheduler | APScheduler in a dedicated `worker` container, job state and the run queue in Postgres (no Redis/Celery) |
| Auth | GitHub Actions OIDC tokens checked against GitHub's JWKS (PyJWT, *candidate*); no user accounts in the MVP |
| Web UI | React + Vite + TypeScript SPA, ECharts or Recharts, served by nginx |
| Alerts | Slack incoming webhook |
| Agent formats | `AGENTS.md` in our repo, our own `llms.txt`; MCP server (stretch) |

## 10. Data

- **Raw LLM responses are append-only** (models under test, extractors, task-text writer, judge): stored as JSONB, never updated or deleted. They cannot be reconstructed retroactively. The same holds for test items and review decisions; the application's DB role has no `UPDATE` / `DELETE` on these tables.
- **Everything lives in PostgreSQL on our VM** ([§3](#3-architecture)): projects and their limits, runs (with the OIDC claims of the upload, [§11](#11-github-action)), uploaded inputs (hash and metadata; the files themselves on a volume, addressed by hash), the inventory and the out-of-inventory models (`Chunk`, `Example`, `CallRecord`, `Claim`, `Finding`, `TestItem`, `Reference`), the golden set and its reviews, raw LLM calls and results. Model attributes: TBD.
- Every result row records: input snapshot hash, commit, docs version, generator version, test item ID, golden-set version, mode, model ID + params, raw response, evaluation result, error category, cost, timestamps.
- The **golden set** lives in our database and is as frozen as files in git would be:
  - a `TestItem` is **never updated or deleted**; a change is a new item.
  - **Identity key** of an item, from deterministic parts only: project + chunk ID + level + operator + **operator version** + format + difficulty + source example ID + the reference in **canonical serialization**. The LLM-written task text is not part of it.
    - Chunk ID and example ID are stable across text edits ([§6.1](#61-reading-and-chunking), [§4](#4-glossary)). Whether an item changed is decided by its reference: a typo fix keeps the reference, so the item is reused; a change in meaning changes the reference and yields a new item ([§7](#7-ci-behaviour-and-repeated-runs)).
    - The operator version is bumped whenever the operator's behaviour changes, so an item is never silently reused under old logic when its reference happens to stay the same.
    - The generator version is not in the key; it is stored with the item as metadata. A new generator therefore regenerates only the items whose reference it really changes.
  - **Reuse:** if an item with the same identity key already exists (in the golden set or as a candidate), it is reused together with its review decisions: no task-text writer, no round-trip solvers, no new item.
  - a **golden-set version** is identified by project + input snapshot hash + generator version, and has a parent version and the set of its item IDs. Unchanged items are referenced, not copied. The commits that produced it are stored with it as metadata, because a commit that changes only code yields the same inputs and must not create a new version (and runs we start with the CLI have no OIDC `sha`). `docs.version` is only a display label. Every run and every result keeps its own commit, so it can be traced.
  - **review decisions are append-only** (item, decision, reviewer, time); an item's state is its latest decision;
  - every result references the item and the golden-set version it ran against.
- **Candidates and main runs:**
  - Items generated in a PR are **candidates**. They are evaluated and listed in the PR comment ([§7](#7-ci-behaviour-and-repeated-runs)), but they never enter the golden set directly.
  - **Main runs are the source of truth.** On every push to the default branch the worker generates items for the changed chunks itself. A candidate with the same identity key is reused there, together with its review decisions. An item enters a golden-set version once it is approved (automatically or by review); items still waiting for review join a later version.
  - A PR closed without merging sends a `closed` event ([§11](#11-github-action)), and its candidates are marked rejected (append-only, never deleted). For a merged PR the event changes nothing, because the main run picks the candidates up.
  - A candidate that no main run picked up and that got no `closed` event shows as **stale** (derived, not stored).
- **Export:** the golden set and the results can be exported as files (*candidate:* JSONL per golden-set version) for the published dataset, backups and determinism tests.
- Database backed up daily from the VM (pg_dump, off-machine copy), see [DEPLOY.md](DEPLOY.md).
- The dataset is intended to be published. **TBD:** check that the model terms allow publishing outputs.

## 11. GitHub Action

In the MVP the Action is a **thin client of our hosted service** ([§3](#3-architecture)): it computes nothing and holds no model key.

- **Triggers** of the caller's workflow (example in `action/README.md`): `pull_request` (including `closed`), `push` to the default branch (main runs, [§7](#7-ci-behaviour-and-repeated-runs)) and `workflow_dispatch` (the first main run of a new project).
- **Two jobs:**
  1. **build** (no secrets, no `id-token`): `sphinx-build -b xml` (Sphinx 9.x) with `build-env.txt` next to the XML ([§2.3](#23-what-the-tool-needs-from-the-user)). An OpenAPI spec is bundled into one file without external `$ref`s (e.g. `redocly bundle`). The output is uploaded as a workflow artifact. **Never built by us** ([§1.1](#11-what-we-are-not-building)). A separate job is a separate VM, so this is a real boundary.
  2. **upload** (`permissions: id-token: write`, checkout with `fetch-depth: 2`): downloads the artifact, packs the XML, the other inputs named in `notinspec.yaml` and the config itself, and sends them to our API with a GitHub OIDC token. On a PR it also sends `head.sha` (for display) and the merge commit's first parent (`git rev-parse HEAD^1`, for the baseline lookup, [§7](#7-ci-behaviour-and-repeated-runs)). It then polls the run, posts the **PR comment** and sets the **status check** with its own `GITHUB_TOKEN`. Our service never gets write access to the caller's repo. On `closed` the job sends only a small "closed" event, with no inputs and no build job.
- **Authentication (GitHub OIDC)**, checked on every upload. There is no shared upload token.
  - signature against GitHub's JWKS, `iss`, `exp` and `aud` (`notinspec`, [§11.1](#111-upload-api));
  - the numeric `repository_id` belongs to a registered project (an ID, not the name, which can be renamed and taken again);
  - `repository_visibility` is `public` ([§1.1](#11-what-we-are-not-building)), so a repo that turns private later is rejected too;
  - `event_name` is `pull_request`, `push` or `workflow_dispatch`. Everything else is rejected: `pull_request_target` and `workflow_run` can run for fork PRs with the base repo's identity. A fork PR with `pull_request` gets no OIDC token;
  - the **path part** of `workflow_ref` (`owner/repo/.github/workflows/<file>`) matches the workflow registered with the project. The `@<ref>` part is ignored, because on a PR it is `refs/pull/N/merge`;
  - for `push` and `workflow_dispatch`, `ref` is `refs/heads/<default branch>` (stored with the project).
- **Trust boundary:**
  - The run's commit is the token's `sha` claim (on a PR, the merge commit); the client does not send it.
  - Values sent by the client (`head.sha`, the first parent) are used only for display and lookup, never as proof.
  - The token proves that the registered workflow of that repo ran, not that the archive matches the commit. Without access to the repo we cannot prove more. That is enough for the MVP: forging inputs needs write access to the repo, and someone with write access can also edit the workflow.
  - Replay protection: one run per (`run_id`, `run_attempt`), and the archive hash is stored with the run. `event_name`, `ref`, `run_id`, `run_attempt` and `workflow_ref` are stored too.
- **Polling needs no token.** Results are public ([§1.1](#11-what-we-are-not-building)), so a run's status can be read without authentication, and a long run never outlives a short-lived OIDC token.
- **Projects** are registered by our team (CLI on the VM), public repos only, with: repository ID, default branch, workflow path, and limits (allowed models, budget; *candidate:* per run and per month).
- **Uploads are untrusted** ([§1.1](#11-what-we-are-not-building)):
  - a compressed archive up to a size limit (*candidate:* 25 MB), extracted with limits on total size and file count; absolute paths, `..` and links are rejected;
  - an OpenAPI spec with a non-local `$ref` (anything other than `#/…`) is rejected, so Prism never fetches a URL or a local file named in the spec. The `core` OpenAPI parser already rejects such refs.
- UC2: evaluates only changed chunks and their test items, compares with the baseline, fails on the conditions in [§7](#7-ci-behaviour-and-repeated-runs).
- The PR comment links to the run in the web UI, where the full results and the report are. Golden-set candidates from the PR ([§10](#10-data)) are listed in the comment; our team reviews them ([§2.5](#25-golden-set-review)).
- Dogfooded on a small demo repo we own.

### 11.1 Upload API

*Proposal: role 7 (the Action) to role 5 (the API). Binding once role 5 approves it.* Paths are public URLs (nginx strips `/api` before the API). Errors use FastAPI's `{"detail": "<message>"}`. The Action shows `detail` to the repo owner in the PR comment, so it must make sense to them.

**`POST /api/uploads`**: one upload starts one run.
- `Authorization: Bearer <GitHub OIDC token>`. The token's `aud` is the fixed string `notinspec`, not our URL. A token minted for another service still fails the check. The site's address can change (today `147-175-151-17.sslip.io`, which has the VM's IP in its name) without breaking the workflows of registered projects.
- `multipart/form-data` with two parts:
  - `archive`: `inputs.tar.gz`, written by `notinspec pack` in the Action, so the client and the server select inputs with the same `core` code. The archive root is the config's folder: the config is stored as `notinspec.yaml`, and each input keeps its path relative to the config. The Sphinx folder holds only `*.xml` and `build-env.txt`. The archive holds regular files only, sorted, with mtime 0 and owner 0, so the same inputs always give the same bytes and the same archive hash.
  - `meta`: JSON `{"schema_version": 0, "head_sha": "<40 hex>" | null, "base_sha": "<40 hex>" | null}`. On a PR, `head_sha` is the PR head (display only) and `base_sha` is `git rev-parse HEAD^1` of the merge commit (baseline lookup, [§7](#7-ci-behaviour-and-repeated-runs)). Both are `null` on `push` and `workflow_dispatch`.
- Everything else comes from the token: repository, event, `ref`, the run's commit (`sha`), `run_id`, `run_attempt`, and the PR number (from `ref` = `refs/pull/<N>/merge`).
- `202` → `{"run_id": "…", "status_url": "https://…/api/runs/<run_id>", "web_url": "https://…/#/runs/<run_id>"}`.
- A second upload with the same (`run_id`, `run_attempt`) and the same archive hash returns `200` with the same body (a retried step). With another archive hash it returns `409`.
- Errors:
  - `401`: bad signature, expired token, or wrong `aud`;
  - `403`: project not registered, private repo, forbidden event, another workflow path, or `push` from another branch;
  - `409`: replay with another archive;
  - `413`: archive over the size limit;
  - `422`: bad archive or config (the `ConfigError` message);
  - `429`: our rate limit (not the caller's setup);
  - `503`: uploads switched off.

**`GET /api/runs/{run_id}`**: no token, because results are public.
```jsonc
{ "schema_version": 0, "run_id": "…",
  "status": "queued" | "running" | "done" | "error",
  "verdict": "pass" | "fail" | null,   // set when status = done
  "comment_md": "…" | null,            // the whole PR comment without our marker; set when done or error
  "error": "…" | null,                 // set when status = error
  "error_kind": "input" | "internal" | null, // set when status = error: the caller's inputs, or our failure
  "web_url": "https://…/#/runs/<run_id>" }
```
`404` for an unknown run.

**`POST /api/pr-closed`**: a PR closed without merging ([§10](#10-data)). The token checks are the same, with `event_name` = `pull_request`. The PR number comes from `ref`. No body, `202`. The token does not say whether the PR was merged, so the Action skips this call for merged PRs. Forging the call needs write access to the repo, which is the same trust boundary as uploads.

**The Action's side** (*proposal* for the open item in [§18](#18-open-items)):
- It polls `status_url` every 15 s, for at most `timeout-minutes` (default 60).
- A problem on our side does not fail the caller's job, so our outage never blocks their merges. This covers our service being unreachable, a `5xx`, and a timeout. The Action posts a warning and a "no result" comment instead.
- A `4xx` on upload except `429` means the caller's setup is wrong, so the job fails and shows `detail`. A `429` is our limit, so it is "no result".
- `verdict: fail` and `status: error` with `error_kind: input` fail the job, and that failure is the status check. `error_kind: internal` (an LLM provider down, the worker out of memory) and `done` with `verdict: null` (a run without an evaluation, e.g. ingestion only) are "no result".

## 12. DevOps

- **Monorepo:**
  ```
  core/     package + CLI
  api/      FastAPI service
  worker/   scheduler
  web/      React SPA
  action/   GitHub Action
  deploy/   docker-compose, nginx, env templates, fixtures
  docs/     SPEC, assignment, DEPLOY
  ```
- **Docker Compose** services: `postgres`, `api`, `worker`, `mock` (Prism), `web` (nginx), `proxy` (Caddy, HTTPS), `backup`.
- The **NLI model** is not in the worker image: its weights live on a named volume (`hf-models`, `HF_HOME`), fetched once by the deploy (`python -m notinspec.nli fetch`). The worker runs with `HF_HUB_OFFLINE=1`, so a run never downloads anything. CI never downloads the model.
- The worker has the LLM key, the DB password and the Slack webhook, so it **never builds Sphinx** ([§1.1](#11-what-we-are-not-building)) and never gets the Docker socket (that would make any code in the worker root on the VM).
- **Prism never runs in the worker.** An uploaded spec is untrusted: even with non-local `$ref`s rejected ([§11](#11-github-action)), Prism must not run where the worker's secrets and the internal network are within reach (SSRF, local file reads). It runs in the `mock` service: no secret env vars, a network with `internal: true` (no egress), the spec on a read-only shared volume. The worker calls it over HTTP and asks it to serve a given spec through a small control endpoint in `mock` (`deploy/mock/control.js`, *proposal* for role 3):
  - the worker writes the spec to the shared `specs` volume as `<sha256>.yaml` (or `.json`);
  - `POST $NOTINSPEC_MOCK_URL/serve` with `{"spec": "<sha256>.yaml"}` → `200 {"base_url": "http://mock:<port>"}` once Prism listens, `422 {"detail": …}` when Prism rejects the spec (the user's problem, the detail has Prism's log), or `503 {"detail": …}` when Prism could not run (ours: spawn error, killed, not listening in 30 s);
  - one Prism at a time: a new spec replaces the old one, and `/serve` calls are handled one after another. Each Prism gets a new port, so a run whose spec was replaced gets "connection refused" and never answers checked against another spec. The worker then calls `/serve` again. So the worker checks **one spec at a time** (all L4 tasks of a run in a row, runs with different specs one after another): two specs at once would keep replacing each other's Prism.
  - Prism validates every request against the spec, and the status alone does not say whether it passed. When the operation defines a `4xx` response, Prism answers with it and lists the violations in the `sl-violations` header (JSON, e.g. `[{"location": ["request", "path", "petId"], "code": "type", …}]`). Otherwise it generates `422` `application/problem+json` with the violations in `validation`. So a request is forbidden when either list is non-empty.
  - The container also runs as a non-root user with a read-only filesystem, no capabilities and 512 MB of memory, so a hostile spec cannot take the worker's memory.
- The **worker** takes queued runs from Postgres (PR runs and main runs uploaded by the Action, UC1 audits) and starts the nightly runs (UC3).
- **CI (GitHub Actions):** lint (ruff, mypy, oxlint), unit tests, Compose integration tests, build images, push to **GHCR**.
- **CD:** SSH to the faculty VM is open only from the STU network / VPN (ports 80 and 443 are public, see [DEPLOY.md](DEPLOY.md)), so a **self-hosted GitHub runner on the VM** pulls images from GHCR and runs `docker compose up -d`. The repo is public, so the runner is used **only by the deploy job on pushes to `main`** (dedicated runner label + protected `production` environment). Fork PRs never run on the VM. PR checks of other repos never use the runner either: their inputs reach the worker only as uploads ([§11](#11-github-action)).
- Public GitHub repository under a team organization, **MIT license**.

## 13. Testing

- **Fake LLM provider** replaying recorded responses for every LLM role. **CI never calls a real LLM.**
- **Determinism tests:** same input + generator version ⇒ same references (hash); golden files per adapter and per reader (a small fixture Sphinx project → expected chunks and NLI premises).
- **Sphinx reader golden test:** a small fixture project of our own with reST `:param:`, Google and NumPy docstrings, built three ways (napoleon, numpydoc, neither) with Sphinx 9 → expected blocks (all three field shapes, [§6.1](#61-reading-and-chunking)). The built XML is committed, so CI never runs `sphinx-build`. Plus tests that XML with external entities and a missing or non-9.x `build-env.txt` are rejected, and that a copy built in another checkout folder hashes the same.
- **Real Sphinx examples:** the built XML of three libraries is committed in `core/examples/sphinx/` (urllib3: reST fields; trio: Google via napoleon; hydra-zen: numpydoc). An end-to-end test runs the CLI on each: exit 0, `ingestion.json` byte-identical across two runs, no `unknown node` warning, `report.html` written.
- **`Change` from version directives:** hydra-zen's `builds(frozen=…)` gives a parameter-level `deprecated`; a `versionchanged` gives no `Change`.
- **`Change` merging** (claims from the fake extractor):
  - urllib3's `format_header_param` from its directive, the "Renamed from …" claim on `format_multipart_header_param` and the changelog claim merge into one `Change` with `replacement`;
  - a `replacement` that is not in the inventory or not in the citation goes to review;
  - `header_formatter` (removal in v3.0 vs. v2.1.0, both claims) gives a `Finding`;
  - L0 never uses a deprecated name as a distractor.
- NLI: fake classifier in unit tests, the real local model only in marked slow tests.
- **Integration:** Compose up → fixture Sphinx docs + spec uploaded through the API → worker → chunking → inventory → cross-checks → L3 / L4 via Prism → report.
- **Auth:** OIDC checks are tested with tokens signed by a test key and a fake JWKS: wrong `aud`, expired, unknown `repository_id`, a private repo, a forbidden event (`pull_request_target`, `workflow_run`), a foreign `workflow_ref` path, a `push` from another branch, and a replayed (`run_id`, `run_attempt`). CI never talks to GitHub's OIDC.
- **Uploads:** an archive with `..`, an absolute path, a link or over the limits is rejected; an OpenAPI spec with a non-local `$ref` is rejected.
- **Reuse and baselines:** a typo fix in a chunk or an example reuses its items (no call to the fake provider); a changed reference yields a superseded item and a candidate; an operator version bump yields new items; a PR is paired with the main run of its merge commit's first parent.
- **Append-only:** tests that the application's DB role cannot update or delete raw LLM responses, test items or review decisions.
- Our own API: OpenAPI validated in CI + Schemathesis.
- Web: Playwright smoke tests.
- Coverage gate on `core/` only.

## 14. Validation (outside CI)

- **H1:** L3 success predicts L4 success (OpenAPI only, via Prism).
- **H2:** lower levels (mainly L1) relate to L3 **per symbol**, not only across models.
- **H3:** tool scores relate to success on tasks of existing benchmarks (those tasks are already evaluated, no need to run them in our tool).
- **H4 (intervention):** fixing sections the tool flagged raises success more than fixing random sections.
- Reliability: manual annotation of tasks and evaluator verdicts.

Candidate data: [NovelAPIBench](https://arxiv.org/html/2606.03657), [CodeUpdateArena](https://arxiv.org/abs/2407.06249v3), tasks from the [RAG study over documentation](https://arxiv.org/pdf/2503.15231), and our own pilot.

## 15. Example across levels

> `connect()` accepts an optional `timeout` parameter in seconds, default 30. Since 2.0, `retries` is replaced by the new `retry_policy`.
> ```python
> conn = client.connect(timeout=10, retry_policy=RetryPolicy(max_attempts=3))
> ```

- **L0:** "Which parameter of `connect()` exists in 2.0? a) `retries` b) `retry_policy` c) `max_retry` d) `backoff`" (`retries` comes from `Change`: `removed` in 2.0 with `replacement` `retry_policy`, so it is a valid distractor).
- **L1:** "List the optional parameters of `connect()` and their defaults."
- **L2:** "In what unit is `timeout`?" (from the claim "timeout is in seconds").
- **L2 (not in the documentation):** "What is the default of `retry_policy`?" (perturbation of the claim "`timeout` defaults to 30": `timeout` → `retry_policy`, another parameter of `connect()`; no chunk states its default). Expected answer: the documentation doesn't say.
- **L3 (adaptation, semantic):** "Give up connecting after 2 minutes and try at most three times." Answer `client.connect(timeout=120, retries=3)` → `timeout` correct, `retries` = `deprecated-api`, `retry_policy` missing.
- **L4:** unavailable, `connect()` is not an OpenAPI operation. For `POST /orders` the model's request would go to Prism.

## 16. Milestones

Faculty checkpoint dates: **TBD**.

### 16.1 MVP

**Order: Sphinx first.** Everything for the Python library is built first, on **urllib3**, then extended to trio (Google via napoleon) and hydra-zen (numpydoc) if that is not time-consuming. The OpenAPI parts come after the Sphinx part works: OpenAPI pilot, curl adapter, K7, L4 via Prism and H1.

1. One OpenAPI spec with guides + one Python library with **Sphinx-based documentation**, examples and a changelog (pilot: urllib3, see [§18](#18-open-items)).
2. Sphinx and Markdown readers, section chunking, component detector, inventory (`Symbol`, `Signature`, `Parameter`, `Constraint`, `Change`, `Source`), `Example` and `CallRecord`.
3. Adapters Python `ast` and curl; cross-checks K1, K4, K7.
4. L1 and L3 tasks (copy, adaptation, variation), L0 from `Change`, L4 via Prism for OpenAPI.
5. 2 small models + 1 large model, 3 modes.
6. Output: PR comment and status check (UC2) with findings and diagnosis through the thin Action; web UI with results.
7. Check hypothesis H1 on the OpenAPI part.
8. CI/CD to the faculty VM, nightly runs of the pilot.
9. Hosted-only: every run on our service, everything in Postgres, the golden set versioned there and reviewed by our team ([§2.5](#25-golden-set-review), [§10](#10-data)).

### 16.2 Next iteration

`Claim` and L2 (with NLI grounding), cross-checks K2, K3, K5, K6, composition, statistics in CI, HTML report, readers for other documentation generators (*candidates:* MkDocs, Docusaurus, TypeDoc).

### 16.3 Future development

- Execution beyond OpenAPI: sandbox for SDKs and libraries (L4 for code), running CLI commands.
- Docs vs. reality: `inspect.signature` of the installed library vs. `Signature`, OpenAPI vs. the real backend.
- Stateful checking of multi-step tasks (stateful mock or a test backend).
- Mocks for GraphQL and gRPC (today call-record comparison only).
- Agentic tasks: the model searches the docs itself via a tool (e.g. MCP).
- Docs websites without a supported generator (rendered HTML → Markdown).
- Sphinx versions other than 9.x (the doctree's node types and attributes change between major versions), and migrating chunks and their IDs when a project moves to another Sphinx version.
- **Self-contained Action:** runs `core` + Prism in the caller's CI with the caller's own model key and no dependency on our service; the golden set as files in the caller's repo, reviewed in PRs, and results as JSON + HTML artifacts.
- **Golden-set review by the docs owners** in the web UI, with GitHub sign-in and the right to review taken from the repo's permissions ([§2.5](#25-golden-set-review)). Not decided yet.
- **Private repos:** the same GitHub sign-in, with a project's results visible only to those who can read its repo.

## 17. Roles

Mapping of roles to the v3 pipeline is a proposal until the team confirms it.

| # | Role | Owns |
|---|---|---|
| 1 | Lead / architecture | core package, golden-set format, this spec |
| 2 | Inputs & inventory | Sphinx and Markdown readers, chunking, prose blocks (input for NLI premises), component detector, spec / signature parsers, adapters, inventory |
| 3 | Runner & evaluation | LLM client, rate limiting, Prism, L0–L4 evaluation, error categories |
| 4 | ML / NLP | claim extraction, NLI grounding, cross-checks, retrieval, statistics, validation track |
| 5 | Backend & data | FastAPI, Postgres schema, migrations, worker, run queue, uploads and OIDC auth, golden-set storage |
| 6 | Frontend & viz | web UI, reports, charts |
| 7 | DevOps | CI, Compose, GHCR, self-hosted runner, GitHub Action packaging, monitoring |

## 18. Open items

- [x] LLM provider: **Groq** free tier ([§8](#8-models)), key `GROQ_API_KEY`, only on our VM. Since 2026-11-21 the claim extractors run on the **FIIT LiteLLM proxy** (`FIIT_API_KEY`); models under test follow later
- [ ] FIIT proxy: a response names the alias (`qwen3.8-flash-next`), not the checkpoint behind it, and the faculty may swap that checkpoint (its docs say so for `decision-local`). Stored claims are reused by alias, so a swap would mix answers of two models unnoticed. The raw response keeps `system_fingerprint`, but that is the server build (vLLM / llama.cpp), not the checkpoint, and the proxy's backend name for qwen is just `Qwen`. So nothing in a response identifies the checkpoint. For now: after the faculty changes a model, extract again with `--no-reuse`. Matters more once models under test run on the proxy (leaderboard)
- [ ] FIIT proxy: its rate limits, concurrency and request timeout are not published (the limiter guesses 20/min, 5 000/day per model). Paid models are blocked in code because they share the team's budget: when, and which, may we allow? ([§8](#8-models))
- [x] Groq limits of our organization: 1 000 requests/day and 8 000 tokens/min per model, from the response headers ([§8](#8-models))
- [ ] Is 8 000 tokens/min and 200 000 tokens/day per model enough for a nightly run of the pilot? The client-side limiter counts requests only. A token budget per model (from `usage` or the `x-ratelimit-remaining-tokens` header), output tokens per minute included, would avoid running into 429s
- [x] Groq structured output: confirmed live on `qwen/qwen3.8-27b` and `openai/gpt-oss-20b` (the claim extractors, [§8](#8-models)). The `json_validate_failed` error with `failed_generation` is not in Groq's docs. gpt-oss-20b without a completion limit produced real ones (`core/tests/claims/fixtures/groq-fixturelib-guide.json`), and the claim parser is tested on them. Before adding another model, run `notinspec models --probe`
- [ ] Faculty checkpoint dates
- [x] Pilot Python library: **urllib3 v2**, first; trio and hydra-zen after it if that is not time-consuming ([§16.1](#161-mvp)). Reasons: Sphinx + autodoc API reference, example-heavy user guide, parameters with units and ranges (`Timeout`, `Retry`), a v1 → v2 migration guide, and a changelog with renames and removals (e.g. `Retry(method_whitelist=…)`, deprecated in 1.26 in favour of `allowed_methods` and removed in 2.0) that exercise `Change`, migration, K4 and `deprecated-api`. Its docs are built with Sphinx 9.1 and stored in `core/examples/sphinx/urllib3/`
- [ ] Pilot OpenAPI spec (after the Sphinx part, [§16.1](#161-mvp))
- [x] Sphinx build environment for the pilot: built for urllib3, trio and hydra-zen with each release's pinned docs dependencies (Sphinx 9.1), in a container without secrets, stored with `build-env.txt` in `core/examples/sphinx/` (see its README). `build-env.txt` stays plain text; its first line is `sphinx-build 9.x.y` ([§2.3](#23-what-the-tool-needs-from-the-user))
- [ ] **Main risk of section chunks:** evidence for a claim may be spread across a section (e.g. a parameter named in one paragraph, its unit in another), so grounding on the text around the citation can drop good claims. Measured in `experiments/nli`: with the breadcrumb, the NLI premise keeps 86 of 92 correct claims in a human-labelled sample. A 400-token window keeps 90, but nearly twice as many wrong ones. Check again on the pilot docs
- [ ] Soft limit for oversized sections
- [ ] **NLI model:** the default is DeBERTa-v3-large wanli. `MoritzLaurer/deberta-v3-large-zeroshot-v2.0` keeps far fewer claims from other sections (7 vs 23 of 259) and is about equal on the rest, but it has no contradiction label. Should we switch, or add it as a second "belongs to this section" check? Needs a larger human-labelled sample
- [ ] **NLI thresholds:** argmax for now. A three-zone rule (keep at p ≥ 0.9, drop below 0.05, human review in between) sends ~8 % of claims to review, but it doesn't catch confident errors (9 of 12 wrong claims kept have p ≥ 0.9). Decide whether the review is worth it
- [ ] A cheap code check that a claim's identifiers, numbers and versions appear in the prose of its section, breadcrumb included; a dotted name may also match without a leading project name (`urllib3.Timeout` → `Timeout`). NLI misses these; see `experiments/nli/FINDINGS.md`, run 006. Prototype `experiments/nli/id_check.py`: on the human labels it drops 3/12 false keeps (2 of them hand-made negatives; 1/9 on model-written claims) and 6/23 wrong cross keeps of NLI, and no correct claim. Checking only the cited sentence drops 5/92 correct claims. The rules were tuned on the same sample, so check again on new docs. Also used by the perturbation operator ([§6.7](#67-tasks-and-operators)), but there the reference stays the claim's **citation**: a sibling identifier from the same section is exactly the distractor we want. In `core/` as `notinspec.grounding` (`missing_identifiers` on `section_reference`) with the fixes from #26: `1` = `1.0` (other numbers as written), units glued to numbers, `TLSv1.2` = TLS 1.2, a leading dot, acronym plurals, capitalized inventory names as identifiers, inventory names in the reference of API descriptions. Still open: check again on new docs (#26)
- [ ] Grounding on docstring prose is not measured yet: `experiments/nli` covered only guide and changelog sections, and parameter blocks are short and lean on the breadcrumb. Run 008 (`experiments/nli/runs/008-core-pipeline-urllib3-demo`) ran `notinspec claims run` on 3 urllib3 pages, docstrings included. It is not human-labelled yet; labels of its blind sample (`experiments/nli/labeling/build_008.py`) would also answer "check again on new docs" for the identifier check (#26). One finding already: 3 of its 6 identifier drops name the full path (`urllib3.util.parse_url`) where the section has only the short name
- [ ] **Claim extraction for whole docs:** one call per chunk. On Groq, the demo pages took ~1.3k tokens per chunk for qwen and ~1.7k for gpt-oss-20b (run 008), so the whole of urllib3 (430 prose chunks) needed 3–4 days of Groq's 200k tokens per day. The FIIT proxy has no known token budget, so the limit there is time (gemma: about a minute for a long chunk). Run all of urllib3 on the proxy; batch several small chunks of one page into one call only if that turns out too slow
- [x] NLI speed on our VM: 0.88 pairs/s under the worker limit of 3 CPU, 1.1 pairs/s on all 4 vCPU (`python -m notinspec.nli bench --pairs 64`, 2026-11-18), in [§6.4](#64-prose-and-changelog--claim)
- [ ] Perturbation: share of "not in the documentation" items in L2, *k* (how many prefilter chunks the unsupported check uses), the recall window size, and how to detect "the docs don't say" in an answer (phrase list, NLI or the judge). Measure the rate of answerable questions that pass the check (false `neutral`) on the reviewed items
- [ ] Models under test: `qwen/qwen3.8-27b` alone for now; at least one more later (small vs. large), and the per-run budget. Qwen is a preview model, which Groq may withdraw at short notice
- [ ] Attributes of the DB models
- [ ] Golden-set review: which items are auto-approved, how much our team can review for the pilot in UC1, and whether and how docs owners review later (GitHub accounts, [§2.5](#25-golden-set-review))
- [ ] Project limits: allowed models, budget per run / per month, upload size
- [x] Where the DB models live in code: in `core` as `notinspec.db`, installed with the extra `notinspec[db]` (API and worker), so the CLI does not need SQLAlchemy. Logic around the DB (item reuse by identity key, baselines, superseded items) is logic too, so it stays in `core`. Pipeline code never imports `notinspec.db`: it works on dataclasses, and only `db` maps them to tables. A separate workspace package was rejected: one more package, and logic would drift into it
- [ ] `deprecated-api` for a **deprecated** symbol or parameter (it still works, but the docs say to use the new one): may it fail the CI gate, or only warn ([§6.10](#610-evaluation))?
- [ ] Backup of the uploaded-inputs volume (today `pg_dump` only)
- [ ] Action when our service is down or the run times out: fail the check or skip it. Proposal in [§11.1](#111-upload-api): a warning and a "no result" comment, and the job passes
- [ ] Export format of the golden set and results for the published dataset
- [ ] Candidates' absolute floor: its default value, and whether it may fail the build after the MVP ([§7](#7-ci-behaviour-and-repeated-runs))
- [ ] Canonical serialization of a reference for the identity key (key order, numbers, units)
- [ ] Definition of "gold context" for multi-step tasks
- [ ] NLI for non-English docs
- [ ] Retrieval for the `retrieved` mode (BM25, embeddings, hybrid)
- [ ] Shape of the report and the web UI
- [ ] Model terms on publishing outputs ([§10](#10-data))
