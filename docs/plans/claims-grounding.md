# Plan: claims with NLI grounding in `core/` (SPEC §6.4)

Goal: a working path **chunk → claim extractor (LLM) → citation check → NLI premise → NLI → identifier check → `Claim`**. It runs on real docs (urllib3 Sphinx XML in `core/examples/sphinx/urllib3`) with real models: Groq for the extractors and the DeBERTa NLI model on CPU. Our own tests and CI still never call a real LLM (SPEC §13): they replay **recorded real** answers (`RecordingProvider` → `FakeProvider`), and NLI uses recorded scores in unit tests, with the real model only in marked slow tests. The product itself (CLI, later the worker) calls the real models.

**Demo scope first:** the first real run covers only part of urllib3, so it fits in Groq's free tier (200k tokens/day per model, §8) in one go. The pages are `user-guide`, `reference/urllib3.util` (`Retry`, `Timeout`) and `v2-migration-guide`: 81 prose chunks, ~13k tokens of chunk text. That is ~120k tokens per extractor even with one call per chunk. The pages cover guide prose and docstrings, and overlap with the `experiments/nli` sections. The whole of urllib3 (430 chunks, 54k tokens; the changelog alone is 16.5k) comes after the demo works.

The work is split into three parts that run in parallel, then one integration step. The parts never import each other. Each part owns its own directory, and shared files have a single owner (table below), so the three branches merge in any order without conflicts.

| Part | Branch | Who | Owns |
|---|---|---|---|
| A · deterministic grounding checks | `core/grounding-checks` | Hinzun (agent session 1) | `core/src/notinspec/grounding/`, `core/tests/grounding/` |
| B · claim extractor | `core/claim-extractor` | Hinzun (agent session 2) | `core/src/notinspec/claims/`, `core/tests/claims/`, `cli.py`, `config.py` |
| C · NLI runtime | `core/nli-runtime` | jmiticky4130 | `core/src/notinspec/nli/`, `core/tests/nli/`, `pyproject.toml` (root and `core/`), `uv.lock`, `worker/Dockerfile`, `deploy/` |
| D · integration + measurement | `core/claims-pipeline` | Hinzun, after A, B and C are merged | `claims/pipeline.py`, CLI `claims`, report, `experiments/nli` run 008 |

SPEC edits: each part changes only its own lines. A: §18 identifier-check bullet. B: §6.4 step 1 and §8 (extractor models). C: §6.4 NLI paragraph, §9, §12. Nobody rewrites a shared paragraph. This file is deleted in the last commit of C's PR, or moved to an issue.

## Contracts

D composes the parts through these interfaces. A part may add things to its own interface, but not change these shapes without telling the others.

```python
# A · notinspec.grounding (pure, no new dependencies)
GROUNDING_VERSION: int                    # bump when any result can change for the same input

@dataclass(frozen=True)
class CitationCheck:
    status: Literal["found", "not_found", "not_checkable"]
    span: tuple[int, int] | None          # offsets into chunk.text
def check_citation(chunk: Chunk, citation: str) -> CitationCheck

@dataclass(frozen=True)
class Premise:
    text: str                             # "<breadcrumb>: <sentences>"
    span: tuple[int, int]                 # sentences used, offsets into chunk.text
    rule: str                             # e.g. "cited±1-in-block+lead-in"
def nli_premise(chunk: Chunk, span: tuple[int, int]) -> Premise

def section_reference(section: Sequence[Chunk], inventory: Inventory) -> str
def missing_identifiers(claim: str, reference: str, *, project: str,
                        known_names: frozenset[str]) -> tuple[str, ...]   # () = passes

# B · notinspec.claims
@dataclass(frozen=True)
class ExtractedClaim:
    chunk_id: str
    extractor: str                        # ExtractorSpec.name
    local_id: str                         # "c1" from the answer
    text: str
    citation: str
    type: Literal["fact", "change"]
@dataclass(frozen=True)
class ExtractorSpec:
    name: str
    model: str
    prompt_version: int
def extract_claims(chunks: Sequence[Chunk], spec: ExtractorSpec, client: ModelClient,
                   run_id: str, calls: CallLog) -> ExtractionResult   # claims + per-chunk failures

# C · notinspec.nli
@dataclass(frozen=True)
class NliScores:
    entailment: float
    neutral: float
    contradiction: float
    @property
    def label(self) -> Literal["entailment", "neutral", "contradiction"]: ...   # argmax
class NliModel(Protocol):
    model_id: str
    revision: str                         # pinned HF commit
    def score(self, pairs: Sequence[tuple[str, str]]) -> list[NliScores]: ...   # (premise, hypothesis)
```

## A · deterministic grounding checks (`core/grounding-checks`)

Built on `prose_sentences` / `find_citation` in `chunking/windows.py`. Don't edit that file: it belongs to chunking. Wrap or extend it in `grounding/` instead.

1. **Citation check** (§6.4 step 1): match on normalized text (whitespace collapsed, Markdown markup and backticks removed, typographic quotes → plain). `not_found` → drop. Found only outside prose (code, table, signature, type) → `not_checkable`. A citation that spans two prose blocks is `found`.
2. **NLI premise** (§6.1): `<breadcrumb>:` + cited sentence(s) ±1 sentence, without leaving the cited prose block. A list item gets the list's lead-in sentence (the last sentence of the paragraph before it, ending with ":"). A `field` block adds the parameter name to the breadcrumb (`urllib3 > API Reference > Retry > total`). The prototype is `local_block()` in `experiments/nli/nli_run.py`.
3. **Identifier / number / version check**: port `experiments/nli/id_check.py` with **every item of issue #26** (numbers compared by value, `2.5s`, `` `.request()` ``, `TLSv1.2`, acronym plurals, capitalized inventory names, the project prefix, inventory names in the reference for docstring sections). The reference is the whole section's prose (all parts) + the breadcrumb.
4. Tests: unit tests for every #26 case. Add a golden test on the Sphinx fixture project (`core/tests/fixtures/sphinx/xml-*`) that checks the expected premises for a few citations (SPEC §13).

## B · claim extractor (`core/claim-extractor`)

1. Port the prompt from `experiments/nli/prompt.md` (project, breadcrumb, the chunk text as the Sphinx reader renders it) with `PROMPT_VERSION`. The answer schema goes in `response_format` (best effort, §8) and is parsed and validated. A malformed answer is a recorded failure of that chunk, not a crash.
2. **Two extractors** (§6.4): `qwen/qwen3.8-27b` and `openai/gpt-oss-20b` (agreed with the team). Both are on Groq's structured-output list, and gpt-oss-20b has measured limits (§8). Run `notinspec models --probe` on gpt-oss-20b first. Groq limits count per model, so the two extractors don't share a budget.
3. **Budget:** the demo pages (top of this file) fit with one call per chunk. For the whole of urllib3 (430 prose chunks, 54k tokens), one call per chunk with a ~1k-token prompt is ~560k tokens per extractor, which is ~3 days of Groq's 200k tokens/day. So, after the demo, batch several small chunks of the **same page** into one call, up to a token budget. Each chunk is tagged by id, every claim returns its chunk id, and each chunk is still read whole. Measure the tokens per extractor on the demo and write them down.
4. **Raw responses are append-only:** every call (request, raw body, usage, time, run id) is appended to a `CallLog`. In the CLI that is a JSONL file in the output folder (`llm-calls.jsonl`). The DB later stores the same records.
5. **Reuse:** extraction is generation, not a model under test, so claims are reused by (chunk `content_hash`, extractor name, model, prompt version). A second run asks only for changed chunks.
6. CLI `notinspec claims extract <config> --out <dir>` (live Groq, needs `GROQ_API_KEY`). Extractor models can be set in config. `--source <glob>` (repeatable) limits extraction to the chunks whose `source` (Sphinx docname) matches, for the demo pages.
7. Tests: record real Groq answers with `RecordingProvider` on the Sphinx fixture project and a few urllib3 chunks, then replay them with `FakeProvider`.

## C · NLI runtime (`core/nli-runtime`), jmiticky4130

1. `TransformersNli`: model `MoritzLaurer/DeBERTa-v3-large-mnli-fever-anli-ling-wanli` at a **pinned revision**, fp32 (fp16 is ~9× slower on CPU, run 003), batching, a CPU thread setting, truncation at 512 tokens (record it if a premise is cut). torch and transformers are imported lazily, so the rest of `core` works without them.
2. **Packaging (decided):** an extra `notinspec[nli]` (transformers + torch **CPU** wheels from the PyTorch CPU index through `[tool.uv.index]` / `[tool.uv.sources]`), the same pattern as `notinspec[db]`, run in-process in the worker. No separate NLI service. The worker installs the extra. CI must not download the model. Decide whether CI installs torch at all (only `uv sync --all-packages` pulls it in if the worker depends on the extra).
3. `RecordedNli` / `RecordingNli`: scores keyed by (model, revision, premise, hypothesis), replayed in CI like `FakeProvider`. Unit tests use scores recorded from the real model. Tests with the real model are marked slow and skipped in CI (SPEC §13).
4. **Deploy:** the model weights live in the worker image or a named volume (`HF_HOME`) and are fetched once. At run time use `HF_HUB_OFFLINE=1`, so the worker never fetches from the network during a run. Measure the speed on the VM (claims/s). Also fix the worker env: the client reads `GROQ_API_KEY` (§8), but compose and `.env.example` still pass `LLM_API_KEY`.
5. Every decision records the model ID, the revision and the decision rule (argmax), §6.4.

## D · integration + measurement (`core/claims-pipeline`), after A, B and C are merged

1. `claims/pipeline.py`: extract (2 extractors) → `check_citation` → `nli_premise` → `NliModel.score` → `missing_identifiers` → `GroundedClaim` with status `kept` / `citation_not_found` / `not_checkable` / `nli_neutral` / `nli_contradiction` / `id_missing`. Each claim records all versions (prompt, grounding, NLI model + revision). Dropped claims are kept with their reason (§6.4).
2. CLI `notinspec claims <config> --out <dir>` → `claims.json` + `llm-calls.jsonl`, plus a claims section in the report. End-to-end test on the fixture project with recorded extractor answers and recorded NLI scores.
3. **Real run on the demo pages of urllib3** (see the top of this file; the whole library later), then a blind human-labelled sample like `experiments/nli/labeling` (run 008), stratified by status and by guide vs. docstring. It measures: precision of kept claims, recall on good claims, false drops of the identifier check (is it still 0?), docstring vs. guide grounding. This closes "check again" in #26 and the docstring item in §18.
4. Later, not in this plan: K5a/K5b, *change* claim → `Change` (§6.3), DB tables for claims and LLM calls (they need the DB models), the worker job.
