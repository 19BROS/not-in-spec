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
5. freezes the approved test items as a **golden set**, versioned in the repo;
6. runs the golden set against several models in **three modes** (no context, retrieved context, gold context);
7. evaluates answers by code: parses the model's code/request into a normalized **call record** and compares it with the reference; for OpenAPI operations also **sends the request to a Prism mock** generated from the spec;
8. reports results **per level, model and mode**, failing documentation sections, failure categories, findings and a **recommended fix type**, and how all of it changes over time. **Never a single score.**

It ships as:

- a **CLI**;
- a **GitHub Action** (the CI tool) that comments on PRs and fails the build when a documentation change significantly lowers usage success;
- a **web service + web UI** with results, history and reports;
- a **scheduled worker** for nightly / pre-release runs.

### 1.1 What we are *not* building

- **No code execution** except L4 for OpenAPI operations via the Prism mock. SDK sandboxes, CLI execution and stateful mocks are [future development](#163-future-development).
- **Docs vs. reality is out of scope.** The truth is what the documentation says. Prism validates against the spec, not against a real backend.
- **No single overall score.** Levels L0–L4 are never averaged together.
- **No LLM decides the correct answer.** References are computed deterministically from the inventory and examples.
- **No user accounts** in the MVP. The web UI is read-only.

## 2. Users

The tool is for a team that **owns a software product's documentation** (library, SDK, REST API, CLI) and wants LLM agents and coding assistants to use it correctly.

### 2.1 Personas

| Persona | Who | Wants | Meets the tool in | Gets |
|---|---|---|---|---|
| **P1 · Maintainer** | developer / maintainer, owns the repo and CI | a change must not make the software harder for LLMs to use; fast, cheap runs | CI status check, PR comment | pass / fail, L3 (L4) drop vs. `main`, new findings in changed sections |
| **P2 · Docs author** | technical writer, DevRel, developer writing docs | to know **which section to fix and how** | PR comment, HTML report / web UI, golden-set review | worst sections first, findings, sample wrong model answers, **recommended fix type** |
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
   docs:
     sphinx: "docs/"                  # Sphinx project (folder with conf.py)
     paths: ["docs/**/*.md"]          # plain Markdown outside Sphinx, optional
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
   ```
2. **API key** for the models as a CI secret.
3. **Review of the golden set** in a PR.

### 2.4 What the tool returns

| Output | For | Format |
|---|---|---|
| CI status check | P1 | pass / fail + reason |
| PR comment | P1, P2 | short summary: score change, new findings, links to sections |
| HTML report / web UI | P2, P3 | worst sections first, symbol profile, sample answers, recommended fixes, trend |
| JSON results | integrations | machine-readable results and findings |
| golden set | P2 | files in the repo, reviewable in a PR |

Example PR comment (UC2):
```text
NOT-IN-SPEC · 3 changed sections · 2 models · 0.18 €
✗ L3 docs/client.md > Connecting > connect()   91 % → 64 % (p = 0.01)
  most common error: wrong arguments – timeout given in ms
  recommendation: state the unit of the timeout parameter
✗ new finding K4: example in docs/retry.md uses removed parameter retries
✓ L3 docs/orders.md, L4 POST /orders unchanged
```

### 2.5 Keeping golden-set review small

Review is the biggest adoption risk. To keep it small:

- auto-approve items whose reference comes deterministically from high-confidence objects (spec, signature);
- send for review only low-confidence items (from claims, from changelog changes, variations without a signature) plus a random sample of the rest;
- in UC2 show only items for changed sections;
- in UC1 split the review into several PRs by section.

## 3. Architecture

```
               ┌───────────────────────── core (Python package `notinspec`) ─────────────────────────┐
 docs, spec, ─►│ chunking ─► components A–D ─► inventory ─► cross-checks ─► symbol profiles          │
 changelog     │                                    │            │                │                 │
               │                                    ▼            ▼                ▼                 │
               │                               findings ◄────────────── test items (golden set)     │
               │                                                                  │                 │
               │                        runner (models × modes) ─► evaluation (+ Prism) ─► report    │
               └────▲──────────────────▲─────────────────────▲──────────────────────▲─────────────┘
                    │                  │                     │                      │
                  CLI          FastAPI service             worker              GitHub Action
                                  │      │              (APScheduler)        (CLI + Prism in
                                  ▼      ▼                   │                 the CI runner)
                            React web UI  PostgreSQL ◄───────┘
```

- **All logic lives in `core`.** CLI, API, worker and Action are thin wrappers.
- **Storage split:** `core` reads the docs and the golden set from files and writes results as JSON. The hosted service (API + worker) persists everything in **PostgreSQL** and serves it to the web UI. The **Action does not need the hosted service**: the golden set lives in the user's repo, results are JSON + HTML artifacts.

## 4. Glossary

These exact terms are used in code, diagrams and text.

| Term | DB model | Meaning |
|---|---|---|
| **Chunk** | `Chunk` | one whole documentation section split by headings (no small token limit, code blocks and tables intact, oversized sections split at a soft limit), with a stable ID (hash of heading path + content) and a breadcrumb. Unit for component detection, inventory, `Source`, gold context, IDs and CI diffs. |
| **NLI window** | – | short prose-only excerpt of a chunk, sized to fit the NLI model; the premise for NLI. Computed from the chunk, not stored. |
| **Component** | – | kind of content in a chunk: **A** formal spec, **B** API reference, **C** examples, **D** prose and changelog. One chunk can contain several. |
| **Symbol** | `Symbol` | anything callable: function, method, class, endpoint, CLI command |
| **Signature** | `Signature` | header of a symbol: parameters and return type, no body. A symbol can have several (overloads, versions). |
| **Parameter** | `Parameter` | one input of a signature: name, type, required / optional, default |
| **Constraint** | `Constraint` | rule for a parameter value: enum, range, unit, format |
| **Return type** | `ReturnType` | what a symbol returns; used by the composition operator |
| **Change** | `Change` | rename, removal or addition of a symbol or parameter in a version |
| **Source** | `Source` | where a fact comes from (chunk, source type) and with what confidence; attached to every inventory object |
| **Inventory** | – | composition of `Symbol`, `Signature`, `Parameter`, `Constraint`, `ReturnType`, `Change`, `Source` = what exists in the API |
| **API reference** | – | the part of the docs describing signatures (parameter tables, docstrings, JSDoc); component B |
| **Example** | `Example` | a code block from the docs |
| **Adapter** | – | parser + normalization for one language or format (Python, tree-sitter languages, curl, CLI) |
| **Call record** | `CallRecord` | normalized call: symbol + named arguments. Built from examples and from model answers, in the same shape. |
| **Claim** | `Claim` | atomic fact from prose or changelog with a citation, verified by NLI grounding. Type *fact* or *change*. |
| **Grounding** | – | NLI check that a claim follows from its chunk (premise = NLI window(s) around the claim's citation, hypothesis = claim) |
| **Cross-check** | – | comparison of two sources (K1–K7); a contradiction is a finding |
| **Operator** | – | rule that turns a call record or signature into a new reference: copy, adaptation, variation, composition, migration |
| **Reference** | `Reference` | the correct answer of a test item, computed by a program, not by an LLM |
| **Task text** | – | natural-language wording of a task, written by an LLM for an existing reference |
| **Test item** | `TestItem` | question or task at level L0–L4 + reference + metadata |
| **Golden set** | – | approved and frozen set of test items, versioned in the repo |
| **Symbol profile** | – | which levels L0–L4 can be tested for a symbol, and the results |
| **Finding** | `Finding` | a problem in the documentation, reported to the author |

## 5. Test levels

| Level | Tests | Source | Format | Evaluation |
|---|---|---|---|---|
| **L0 Recognition** | does this symbol / parameter exist (in version X)? | `Symbol`, `Parameter`, `Change`; rejected claims as fake names | yes/no, 4 options | exact match |
| **L1 Recall** | path, required parameters, defaults | `Signature`, `Parameter` | open answer | path correctness + Jaccard of parameters |
| **L2 Comprehension** | behaviour, constraints, "not in the documentation" | `Claim` | questions | normalization → NLI → LLM judge |
| **L3 Usage** | can it write the call / code that reaches the goal? | `CallRecord`, `Signature`, `Parameter`, `Constraint`, `ReturnType`, `Change` | task → code / request | call-record comparison + error category |
| **L4 Execution** *(OpenAPI only)* | the request is valid per the spec | L3 tasks for OpenAPI operations | task → HTTP request | Prism mock validates the request |

The level framework is inspired by [arXiv:2605.31478](https://arxiv.org/html/2605.31478). **The CI gate is L3 (and L4 for OpenAPI).**

## 6. Pipeline

### 6.1 Reading and chunking

**Readers.** Documentation generators are supported in phases. Every reader produces the same `Chunk`s, so everything after this step does not care where the docs came from.

| Phase | Input | How it is read |
|---|---|---|
| MVP | **Sphinx** project | from Sphinx's **structured output**, not from rendered HTML and not with our own reST/MyST parser (*candidate:* `sphinx-build -b xml`, i.e. the docutils doctree; `objects.inv` as the list of documented symbols). Sections, code blocks (`literal_block`), tables and API descriptions (`desc` nodes, input for component B) come already typed from the tree. |
| MVP | plain Markdown, llms.txt, changelog | Markdown parser |
| MVP | formal spec (OpenAPI) | its own parser (component A); `description` texts become chunks for component D |
| next iteration | other generators (*candidates:* MkDocs, Docusaurus, TypeDoc) | their structured output where they have one |
| future | docs websites without a supported generator | rendered HTML → Markdown (*candidates:* `trafilatura`, `markitdown`) |

**Chunks = sections.**

- A `Chunk` is **one whole section**: split **by headings**, a section runs from its heading to the next heading. **No small token limit.**
- Code blocks and tables are **never split**.
- **Soft-limit fallback:** a section over a soft limit (*candidate:* ~2,000 tokens) is split at paragraph boundaries, never inside a code block or table. The parts keep the section's breadcrumb.
- Breadcrumb, **stable ID** = hash of heading path + content.
- Sections are the unit for **component detection, the inventory `Source`, gold context, IDs and CI diffs**.
- Output: `Chunk`.

**NLI windows.** The NLI model accepts only a few hundred tokens, so NLI never sees a whole section. An **NLI window** is a short, **prose-only** excerpt of a chunk (code blocks and tables left out), cut at sentence boundaries and sized to fit the NLI model (*candidate:* ≤ 400 tokens, with overlap). Windows are computed deterministically from the chunk (chunk ID + offset), so they need no storage of their own. Use in grounding: [§6.4](#64-prose-and-changelog--claim).

### 6.2 Components and techniques

A component detector finds **all** components present in each chunk (file extension, code-block language, Sphinx node types, Markdown structure). Each goes its own way in parallel; there is no either/or.

| Component | What | Technique | Output |
|---|---|---|---|
| **A · Formal spec** | OpenAPI, GraphQL schema, `.proto`, JSON Schema | spec parser (YAML/JSON, `graphql-core`, protobuf), deterministic. `description` texts go to D. For OpenAPI a Prism mock is also started. | `Symbol`, `Signature`, `Parameter`, `Constraint`, `ReturnType`, `Change` (`deprecated`) |
| **B · API reference** | signatures, parameter tables, docstrings, JSDoc, Sphinx API descriptions (`py:function`, autodoc) | Sphinx `desc` nodes, signature parser (`ast` / tree-sitter) and table parser, deterministic | `Symbol`, `Signature`, `Parameter`, `Constraint`, `ReturnType` |
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
| B · signature and table parser | `Symbol`, `Signature`, `Parameter`, `Constraint`, `ReturnType` | signature, high confidence |
| C · example normalization | `Symbol`, `Parameter`, only if not yet in the inventory | example, medium confidence |
| D · *change* claim | `Change` | changelog, low confidence → PR review |

- **Merge:** objects of the same symbol from several sources are merged with priority **spec > signature > example > changelog**. A disagreement between sources is a `Finding`.
- **Outside the inventory:** `Chunk`, `Example`, `CallRecord`, `Claim`, `Finding`, `TestItem`, `Reference`. The composition graph is built from `ReturnType` and the data flow in call records.

### 6.4 Prose and changelog → `Claim`

1. **Claim extractor** (LLM; 2 extractors with different models or prompts): reads the **whole chunk** (section) and returns atomic, self-contained claims, each with a **citation** (exact quoted span from the chunk). Type *fact* or *change*. A citation not found verbatim in the chunk → drop the claim (deterministic check).
2. **Grounding via NLI:** premise = the **NLI window(s) around the citation** (the window containing it, plus the neighbouring window when the citation crosses a window boundary), hypothesis = claim. `entailment` → keep. `neutral` / `contradiction` → drop (may still serve as an unanswerable L2 question or a fake name for L0).
3. **K5a · claim vs. claim within a chunk:** extractor A ⇄ B, NLI in both directions.
4. **K5b · claim vs. claim across chunks:** embedding prefilter so not all pairs are compared, then NLI in both directions.

| A ⇒ B | B ⇒ A | Relation | Action |
|---|---|---|---|
| entailment | entailment | duplicate | merge into one claim |
| neutral | entailment | B is more specific | keep B |
| neutral | neutral | different claims | keep both |
| contradiction | – | contradiction | `Finding`, no tasks from these claims |

5. A *change* claim yields a `Change` (low confidence → PR review).

NLI = small local cross-encoder classifying (premise, hypothesis) → entailment / contradiction / neutral; cheap and deterministic (*candidates:* `cross-encoder/nli-deberta-v3-base`, a multilingual XNLI model for non-English docs). The premise is always an NLI window or a claim, never a whole chunk. Watch numbers, negation and language. Thresholds are calibrated on our own annotated sample.

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
| Has a `Claim`? | L2 questions | – |
| Has a `Change`? | L0 distractors from old names, L3 migration | – |
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

Example reference:
```json
{"task": "t_31", "level": "L3", "operator": "adaptation",
 "calls": [{"call": "Client.connect", "args": {"timeout": [120]}}]}
```
Task text (written by an LLM): "Give up connecting after 2 minutes."

- **Leave-one-out:** in gold-context mode, the example the task was derived from is removed, to test whether the rest of the docs is enough.
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
9. PR review and manual check of a sample (pipeline precision, Cohen's kappa).

If a well-grounded task fails even with gold context, the problem is probably in the documentation text (`Finding`), not in the task.

### 6.9 Modes

| Mode | Context given to the model |
|---|---|
| `none` | nothing (what the model knows from its weights) |
| `retrieved` | chunks found by retrieval (*candidates:* BM25, embeddings, hybrid). Retrieval may embed smaller sub-parts of a section (paragraphs, code blocks), but always returns the **whole section**. |
| `gold` | the chunks (whole sections) the test item was derived from (minus the source example for leave-one-out) |

The three modes separate the effect of model weights, text quality and findability.

### 6.10 Evaluation

Every test item × model × mode. **All raw responses are stored.**

- **L0:** exact match, shuffled option order.
- **L1:** path correctness + Jaccard of required parameters (+ defaults).
- **L2:** normalization → NLI (coverage and precision) → **LLM judge** only for borderline cases.
- **L3:** model answer → the same adapter as for examples → `CallRecord` → comparison with the reference. Error categories:

  | Category | Meaning |
  |---|---|
  | `success` | matches the reference |
  | `wrong-symbol` | calls a different symbol |
  | `wrong-arguments` | right symbol, wrong arguments |
  | `hallucinated-api` | symbol / parameter not in the inventory |
  | `deprecated-api` | symbol / parameter is in `Change` (removed or replaced) |
  | `api-bypass` | reaches the goal without the documented API |
  | `invalid-format` | answer cannot be parsed |

- **L4 (OpenAPI only):** the model's HTTP request is sent to a Prism mock started from the spec, which validates path, method, parameters, body, headers and auth. Prism is stateless: multi-step tasks using an `id` from a previous response are checked structurally only.

**Limits without execution:** L3 cannot check semantics (correct call with a wrongly computed value) or stateful procedures. Conceptual documentation without code or signatures yields only L0–L2.

### 6.11 Diagnosis and recommended fix

| Situation (gold context) | Interpretation | Recommended fix (P2) |
|---|---|---|
| L3 OK | docs enable usage | – |
| L3 bad, L1 bad | unclear signature | describe parameters clearly |
| L3 bad, L1 and L2 OK | missing example or guide ("knows what, not how") | add a usage example |
| L3 bad, category `deprecated-api` | weights override the context | highlight the change, add a migration example |
| copy OK, variation bad | docs work only via copy-paste of examples | describe parameters, not only examples |
| with example OK, leave-one-out bad | symbol relies on a single example | add parameter descriptions |
| wrong arguments due to a unit | missing unit | state the unit at the parameter |
| bad without context, OK with gold | model doesn't know it from weights, docs work | – |
| OK with gold, bad with retrieved | text is good but hard to find | improve headings and structure |
| K1 / K4 / K7 finding | example does not match signature or spec | fix the example |
| K5 contradiction | sections contradict each other | unify them |

## 7. CI behaviour and repeated runs

- Non-determinism is handled by paraphrases and repeated runs.
- **Paired comparison with the `main` baseline** (bootstrap or McNemar); the build fails only on a **statistically significant drop**.
- Fail conditions (configurable): L3 (and L4) drop in changed sections; a new finding from selected cross-checks.
- Thresholds live in the config file in the repo.
- **Cost:** small models on every PR, large models nightly or before a release, only items affected by the diff, response cache.
- **Repeated runs:** the worker runs the full golden set of every hosted target **nightly**, stores every raw response, diffs against the previous run and sends a **Slack alert** on a significant drop.
- Runs are **resumable**: if rate limits stop a run, the worker continues it later.

## 8. Models

- **LLM access via an API key provided by the faculty.** Provider, endpoint, available models and limits: TBD ([§18](#18-open-items)). The key lives only in env / secrets.
- Users of the GitHub Action bring **their own key** as a secret in their repo.
- Roles of LLM calls: models under test (small for PRs, large for nightly), 2 claim extractors, task-text writer, 2 strong round-trip solvers, LLM judge for borderline L2 answers.
- **Local CPU models:** NLI cross-encoder and embeddings run locally (no GPU on the VM). Models under test are not run locally.
- Every call is recorded with exact model ID, temperature (0) and all parameters, plus token usage and cost.
- The client is rate-limit aware (queue, backoff on 429) and caches responses by (run ID, model, prompt hash) so a resumed run never re-asks. The cache never crosses runs, otherwise change over time could not be measured.
- A model that disappears is a normal, displayed state, not an error.

## 9. Stack

| Area | Choice |
|---|---|
| Language | Python 3.12+ (core, API, worker), TypeScript (web) |
| Packaging / tooling | uv, ruff, mypy (core), pytest, pre-commit |
| API | FastAPI; its generated OpenAPI is validated in CI |
| Reading docs | Sphinx (`xml` builder / docutils doctree, `objects.inv`) in the MVP; `markitdown`, `trafilatura` later (*candidates*) |
| Parsers | Python `ast`, tree-sitter, `shlex`, `json`, `yaml`, `graphql-core`, protobuf |
| Spec tooling | OpenAPI 3.x + JSON Schema, **Prism** (mock server, L4 and K7), **Schemathesis** (tests our own API) |
| NLI / embeddings | `sentence-transformers` CrossEncoder, `cross-encoder/nli-deberta-v3-base`, mDeBERTa XNLI, `all-MiniLM-L6-v2` (*candidates*), CPU only |
| LLM access | faculty-provided API (TBD) |
| Evaluation / statistics | scikit-learn, bootstrap, McNemar test |
| Database | PostgreSQL, SQLAlchemy 2, Alembic |
| Scheduler | APScheduler in a dedicated `worker` container, job state in Postgres (no Redis/Celery) |
| Web UI | React + Vite + TypeScript SPA, ECharts or Recharts, served by nginx |
| Alerts | Slack incoming webhook |
| Agent formats | `AGENTS.md` in our repo, our own `llms.txt`; MCP server (stretch) |

## 10. Data

- **Raw LLM responses are append-only** (models under test, extractors, task-text writer, judge): stored as JSONB, never updated or deleted. They cannot be reconstructed retroactively.
- Postgres holds the inventory and the out-of-inventory models (`Chunk`, `Example`, `CallRecord`, `Claim`, `Finding`, `TestItem`, `Reference`). Model attributes: TBD.
- Every result row records: input snapshot hash, docs version, generator version, test item ID, mode, model ID + params, raw response, evaluation result, error category, cost, timestamps.
- The **golden set** is a set of files in the repo of the documented project; chunk IDs are stable, so only changed parts are regenerated.
- Database backed up daily from the VM (pg_dump, off-machine copy), see [DEPLOY.md](DEPLOY.md).
- The dataset is intended to be published. **TBD:** check that the model terms allow publishing outputs.

## 11. GitHub Action

- Reusable action that runs the CLI + Prism inside the CI runner. **No dependency on our hosted service.**
- Reads `notinspec.yaml` from the caller repo; the model API key comes from the caller's secrets.
- UC2: evaluates only changed chunks and their test items, compares with the `main` baseline, posts a **PR comment** and a **status check**, fails on the conditions in [§7](#7-ci-behaviour-and-repeated-runs).
- Outputs JSON results and an HTML report as workflow artifacts.
- Golden-set changes appear in the PR for review ([§2.5](#25-keeping-golden-set-review-small)).
- Dogfooded on a small demo repo we own.

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
- **Docker Compose** services: `postgres`, `api`, `worker` (starts Prism per spec when needed), `web` (nginx), `proxy` (Caddy, HTTPS), `backup`; `prism` profile for local dev.
- **CI (GitHub Actions):** lint (ruff, mypy, oxlint), unit tests, Compose integration tests, build images, push to **GHCR** (including the CLI image used by the Action).
- **CD:** the faculty VM is reachable only over VPN, so a **self-hosted GitHub runner on the VM** pulls images from GHCR and runs `docker compose up -d`. The repo is public, so the runner is used **only by the deploy job on pushes to `main`** (dedicated runner label + protected `production` environment). Fork PRs never run on the VM.
- Public GitHub repository under a team organization, **MIT license**.

## 13. Testing

- **Fake LLM provider** replaying recorded responses for every LLM role. **CI never calls a real LLM.**
- **Determinism tests:** same input + generator version ⇒ same references (hash); golden files per adapter and per reader (a small fixture Sphinx project → expected chunks and NLI windows).
- NLI: fake classifier in unit tests, the real local model only in marked slow tests.
- **Integration:** Compose up → fixture Sphinx docs + spec → chunking → inventory → cross-checks → L3 / L4 via Prism → report.
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

- **L0:** "Which parameter of `connect()` exists in 2.0? a) `retries` b) `retry_policy` c) `max_retry` d) `backoff`" (`retries` comes from `Change`).
- **L1:** "List the optional parameters of `connect()` and their defaults."
- **L2:** "In what unit is `timeout`?" (from the claim "timeout is in seconds").
- **L3 (adaptation, semantic):** "Give up connecting after 2 minutes and try at most three times." Answer `client.connect(timeout=120, retries=3)` → `timeout` correct, `retries` = `deprecated-api`, `retry_policy` missing.
- **L4:** unavailable, `connect()` is not an OpenAPI operation. For `POST /orders` the model's request would go to Prism.

## 16. Milestones

Faculty checkpoint dates: **TBD**.

### 16.1 MVP

1. One OpenAPI spec with guides + one Python library with **Sphinx-based documentation**, examples and a changelog (pilot).
2. Sphinx and Markdown readers, section chunking, component detector, inventory (`Symbol`, `Signature`, `Parameter`, `Constraint`, `Change`, `Source`), `Example` and `CallRecord`.
3. Adapters Python `ast` and curl; cross-checks K1, K4, K7.
4. L1 and L3 tasks (copy, adaptation, variation), L0 from `Change`, L4 via Prism for OpenAPI.
5. 2 small models + 1 large model, 3 modes.
6. Output: JSON results + PR comment (UC2) with findings and recommended fix type; web UI with results.
7. Check hypothesis H1 on the OpenAPI part.
8. CI/CD to the faculty VM, nightly runs of the pilot.

### 16.2 Next iteration

`Claim` and L2 (with NLI windows), cross-checks K2, K3, K5, K6, composition, statistics in CI, HTML report, readers for other documentation generators (*candidates:* MkDocs, Docusaurus, TypeDoc).

### 16.3 Future development

- Execution beyond OpenAPI: sandbox for SDKs and libraries (L4 for code), running CLI commands.
- Docs vs. reality: `inspect.signature` of the installed library vs. `Signature`, OpenAPI vs. the real backend.
- Stateful checking of multi-step tasks (stateful mock or a test backend).
- Mocks for GraphQL and gRPC (today call-record comparison only).
- Agentic tasks: the model searches the docs itself via a tool (e.g. MCP).
- Docs websites without a supported generator (rendered HTML → Markdown).

## 17. Roles

Mapping of roles to the v3 pipeline is a proposal until the team confirms it.

| # | Role | Owns |
|---|---|---|
| 1 | Lead / architecture | core package, golden-set format, this spec |
| 2 | Inputs & inventory | Sphinx and Markdown readers, chunking, NLI windows, component detector, spec / signature parsers, adapters, inventory |
| 3 | Runner & evaluation | LLM client, rate limiting, Prism, L0–L4 evaluation, error categories |
| 4 | ML / NLP | claim extraction, NLI grounding, cross-checks, retrieval, statistics, validation track |
| 5 | Backend & data | FastAPI, Postgres schema, migrations, worker |
| 6 | Frontend & viz | web UI, reports, charts |
| 7 | DevOps | CI, Compose, GHCR, self-hosted runner, GitHub Action packaging, monitoring |

## 18. Open items

- [ ] Faculty API key: provider, endpoint, available models, rate limits, budget, whether it may be used from GitHub-hosted runners
- [ ] Faculty checkpoint dates
- [ ] Pilot documentation: which OpenAPI and which Python library (must have Sphinx-based docs). *Recommended library:* **urllib3 v2**: Sphinx + autodoc API reference, example-heavy user guide, parameters with units and ranges (`Timeout`, `Retry`), and a v1 → v2 migration guide and changelog with renames and removals (e.g. `Retry(method_whitelist=…)` → `allowed_methods`) that exercise `Change`, migration, K4 and `deprecated-api`. Alternatives: marshmallow v4, attrs, click. Verify the docs are still built with Sphinx before committing to it
- [ ] Sphinx build environment: autodoc imports the documented library, so the reader needs the project's dependencies and Sphinx extensions installed (in the Action and in the worker)
- [ ] **Main risk of section chunks:** evidence for a claim may be spread across a section (e.g. a parameter named in one paragraph, its unit in another), and grounding only on the windows around the citation can miss it, so good claims get dropped. Measure on the annotated sample; options are wider windows or combining several windows as the premise
- [ ] Soft limit for oversized sections, NLI window size and overlap
- [ ] Models under test (small vs. large) and per-run budget
- [ ] Attributes of the DB models
- [ ] Golden-set review: how much users will do, which items are auto-approved
- [ ] Definition of "gold context" for multi-step tasks
- [ ] NLI model choice, English vs. other languages, threshold calibration
- [ ] Retrieval for the `retrieved` mode (BM25, embeddings, hybrid)
- [ ] Shape of the report and the web UI
- [ ] Model terms on publishing outputs ([§10](#10-data))
