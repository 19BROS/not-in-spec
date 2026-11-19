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

Pass the snapshot's actual version explicitly: `IngestConfig` does not currently retain
`docs.version`. An inventory is a snapshot, not a history of signatures. These generators do
not reconstruct an older inventory by changing the version argument.

## Conservative generation rules

- L0 yes/no tests symbols and named parameters. Positive evidence needs a reliable signature;
  negative evidence needs an explicit effective `removed` change. Missing entries alone never
  imply absence. Versions use the inventory's PEP 440 parser (`2.0 == 2.0.0`, `2.10 > 2.9`).
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
- Qualified-path questions use a unique short symbol name, never the answer path in the
  question. Ambiguous short names and already-unqualified names are skipped.
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
snapshot hash and generator version are not in the identity.

Reference serialization uses `asdict` followed by the existing `canonical_json`:
an explicit `kind` tag, subject (symbol/parameter and normalized tested version), and answer;
MCQ also includes its frozen options. The subject prevents collisions between two equal
answers for different symbols in the same chunk. The tested version is semantic in a versioned
question; equivalent PEP 440 spellings normalize identically. Numeric/default expressions
are preserved as strings, matching the inventory contract; no unit conversions are invented.
Use `reference_json()` for canonical standalone references.

`existing=` reuses the entire frozen item by ID **before** invoking the text writer, including
its original generation metadata. New-run snapshot metadata belongs to the run. Changed
references/operator versions create new IDs; old items remain untouched.

## Text and remaining integration

`TemplateWriter` is explicitly a local template implementation (`writer="template-v1"`).
It creates two deterministic wording variants. `TaskTextWriter.write(Question) -> TaskText`
is the replacement interface for a recorded/fake or eventual LLM writer. Never send a whole
`TestItem` to the model under test: use `model_prompt()`. For MCQ, the writer receives a neutral
scope and all options; the correct option ID is withheld.

The generic §6.8 statement that reference values appear in task text cannot literally apply
to recall answers (it would disclose the answer). Templates name the question's subject and
leave its answer internal. Usage-task value checks and LLM round-trip QC are not implemented
here. Approval, review decisions, DB reuse, golden-set versions, runner/evaluator integration,
recorded LLM wording and reviewed changelog changes remain separate work. JSON here is a local
verification/export format, not a replacement for the hosted golden set required by §10.
