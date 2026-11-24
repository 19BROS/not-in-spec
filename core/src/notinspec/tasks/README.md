# L0/L1 task candidates

`notinspec.tasks` consumes the existing `Inventory`, `Chunk`s and inventory `Conflict`s.
It performs no network calls, database access, Sphinx builds or model evaluation.
All output is **unapproved candidates**, not a golden set. SPEC takes precedence over this note.

From the repository root, using the committed built Sphinx fixture:

```sh
uv run python -m notinspec.tasks core/tests/fixtures/sphinx/xml-plain --project fixturelib --docs-version 2.0 --out tasks.json
uv run python -m notinspec.tasks core/tests/fixtures/sphinx/xml-plain --project fixturelib --docs-version 2.0 --reuse tasks.json --out tasks-next.json
uv run pytest core/tests/tasks
```

The destination must not exist: exports are created with exclusive `xb`, never overwritten.
`load`/`loads` validate the schema, reference tags and recomputed item identities.
The CLI reads existing XML through the Sphinx reader and inventory builder. It adds no reader.
The library entry points `generate_l0` and `generate_l1` also work directly with `ingest()` output:

```python
from notinspec.tasks import GenerationContext, generate_l1

context = GenerationContext(ingestion.project, "2.0", ingestion.input_hash)
result = generate_l1(
    ingestion.inventory,
    context=context,
    chunks=ingestion.chunks,
    conflicts=ingestion.conflicts,
)
prompt = result.items[0].model_prompt()  # text, answer_format, options; no reference
```

`docs_version` is a display label: `2.8.0`, `latest` and `main` are all valid. It never
enters references for current-snapshot facts or L1. To interpret versioned `Change` evidence,
pass the actual API version as `GenerationContext(..., api_version="2.8.0")` or CLI
`--api-version 2.8.0`. If omitted, a PEP 440-compatible docs label supplies that comparison
version for changes only; otherwise change-dependent facts are skipped. An inventory is a
snapshot, not a history of signatures. Changing a version cannot reconstruct an older API.

## Conservative generation rules

- L0 yes/no tests symbols and named parameters. Positive evidence needs a reliable signature;
  negative evidence needs an explicit effective `removed` change. Missing entries alone never
  imply absence. Versions use the inventory's PEP 440 parser (`2.0 == 2.0.0`, `2.10 > 2.9`).
- Yes/no is emitted only when **both classes have valid source evidence**, then deterministically
  balanced to equal counts before invoking the writer. Otherwise it is disabled, with eligible
  yes/no counts in `skipped`; a positive-only set would give an always-yes baseline 100%.
  Invented near-miss negatives are not implemented. The committed real urllib3 snapshot has
  no confirmed removals, so it intentionally produces **0 L0 and 511 L1 candidates**.
- The latest applicable change determines removal status, including re-additions. `deprecated`
  still exists; `removal_planned` is not removal. Inconsistent snapshots, invalid versions and
  changes backed only by changelog/example sources are skipped pending review. Conflicts are
  excluded conservatively by symbol or shared source section. Pass ingestion's conflicts;
  a merged inventory alone does not retain them.
- MCQ freezes one confirmed positive and the first three distinct confirmed removed names
  in lexical order, within the same symbol for parameters. No invented names or rejected
  claims. Insufficient evidence produces a `SkippedTask`. Options have content-derived IDs;
  the correct ID survives reordering. Semantic correctness comes from generation evidence;
  the dataclass additionally validates four unique options and exactly one correct ID.
- L1 requires exactly one reliable signature. Overloads are skipped rather than displaying a
  signature containing the answer. Required names form a sorted set; an empty set is valid.
  `*args`/`**kwargs` are never required/defaulted. Each known optional default gets a separate
  task; unknown defaults are skipped. Values stay **as written**: `"None"` is a documented
  Python value, while inventory `None` means missing. No evaluation of default expressions.
- Qualified-path questions use a unique short symbol name. The entire `Question` sent to
  the writer, including `subject.symbol`, omits the qualified answer path. Ambiguous short
  names and already-unqualified names are skipped.
- The initial scope is the Sphinx/Python inventory. OpenAPI operations and location-bearing
  parameters are skipped. The OpenAPI loader is not treated as a shared inventory mapper.
  Call-record fallback for symbols without signatures remains a separate integration.

## Representation and identity

Frozen `TestItem` contains a typed `Reference` union (existence, choice, required names,
one default, qualified path), sources, primary/all source chunk IDs, snapshot hash,
docs/generator/operator versions, wording and two or three paraphrases.
`question_kind` describes the question. **`operator=None`** means direct inventory recall:
SPEC §6.7 defines usage/perturbation operators, but no L0/L1 operator. We do not redefine `copy`.
`operator_version` versions these recall rules even though the operator is null.

Identity follows §10: project, primary chunk ID, level, operator, operator version, format
(`python`), difficulty (`explicit-single-step`), source example ID (`None`) and canonical
reference. Primary chunk selection is deterministic by source section and part; all chunks
of the referenced sections are retained for gold context. Text, paraphrases, sources,
snapshot hash, docs display label and generator version are not in the identity.

Reference serialization uses `asdict` followed by the existing `canonical_json`:
an explicit `kind` tag, subject (symbol/parameter), and answer; MCQ also includes its frozen
options. The subject prevents collisions between two equal answers for different symbols in
the same chunk. Only removal-based existence references and MCQs carry a semantic
`tested_version`; current positive existence has `None`, and L1 has no version field.
Equivalent PEP 440 spellings normalize identically. Numeric/default expressions
are preserved as strings, matching the inventory contract; no unit conversions are invented.
Use `reference_json()` for canonical standalone references.

`existing=` reuses the entire frozen item by ID **before** invoking the text writer, including
its original generation metadata. New-run snapshot metadata belongs to the run. Changed
references/operator versions create new IDs; old items remain untouched.

The corrected contract uses JSON schema **2**, generator/operator version **2** and
`template-v2`. Schema 1 exports are rejected rather than silently changing their identity.
Keep old exports unchanged and regenerate into a new file. Within schema 2, changing only
the docs display label preserves current-fact IDs and allows `existing=` / `--reuse` to keep
their frozen wording and original metadata.

## Text and remaining integration

`TemplateWriter` is explicitly a local template implementation (`writer="template-v2"`).
It creates two deterministic wording variants. `TaskTextWriter.write(Question) -> TaskText`
is the replacement interface for a recorded/fake or eventual LLM writer. Never send a whole
`TestItem` to the model under test: use `model_prompt()`. For MCQ, the writer receives a neutral
scope and all options; internal IDs and the correct option ID are withheld.

MCQ `model_prompt()` returns `answer_format="choice-label"` with `{label, text}` options
labelled **A-D**. Internal content-derived IDs stay in the reference. The runner can provide
an explicit permutation of those IDs and must retain that same order when decoding:

```python
from notinspec.tasks import ChoiceReference

assert isinstance(task.reference, ChoiceReference)
order = tuple(option.id for option in reversed(task.reference.options))
prompt = task.model_prompt(option_order=order)  # send only this to the tested model
selected_id = task.reference.option_id("B", option_order=order)
is_correct = selected_id == task.reference.correct_id
```

The example illustrates the mapping; the full runner/evaluator is separate work. A writer
must keep option bodies in the structured options, not bake labels into frozen question text,
so presentation reordering remains safe. Regression tests in `core/tests/tasks/test_review_regressions.py`
cover the real urllib3 inventory, label-only version changes, writer leakage and MCQ reordering.

The generic §6.8 statement that reference values appear in task text cannot literally apply
to recall answers (it would disclose the answer). Templates name the question's subject and
leave its answer internal. Usage-task value checks and LLM round-trip QC are not implemented
here. Approval, review decisions, DB reuse, golden-set versions, runner/evaluator integration,
recorded LLM wording and reviewed changelog changes remain separate work. JSON here is a local
verification/export format, not a replacement for the hosted golden set required by §10.
