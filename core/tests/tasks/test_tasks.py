import json
from dataclasses import FrozenInstanceError, replace
from pathlib import Path

import pytest

from notinspec.adapters.canonical import canonical_json, content_hash
from notinspec.chunking import Document, chunk_document
from notinspec.config import IngestConfig
from notinspec.ingestion import ingest
from notinspec.inventory import Change, Conflict, Inventory, Parameter, Signature, Source, Symbol
from notinspec.tasks import (
    ChoiceReference,
    DefaultReference,
    ExistsReference,
    GenerationContext,
    GenerationResult,
    Option,
    PathReference,
    RequiredParametersReference,
    Subject,
    TaskText,
    TemplateWriter,
    dumps,
    generate_l0,
    generate_l1,
    load,
    loads,
    save,
)
from notinspec.tasks.__main__ import main
from notinspec.tasks.serialization import reference_from_json, reference_json

CHUNKS = chunk_document(Document("api.md", "# API\nDocumentation."), project="pkg")
SOURCES = (Source("signature", CHUNKS[0].section_id),)
CONTEXT = GenerationContext("pkg", "2.0", content_hash("snapshot"))
SUBJECT = Subject("pkg.connect", "2.0")
FIXTURE = Path(__file__).parents[1] / "fixtures" / "sphinx"


def parameter(name="host", *, required=True, default=None, kind="positional_or_keyword"):
    return Parameter(name, kind, required, SOURCES, default=default)


def symbol(path="pkg.connect", parameters=None):
    if parameters is None:
        parameters = (parameter(),)
    return Symbol(path, "function", SOURCES, (Signature(parameters, SOURCES),))


def run(inventory, level="L0", **kwargs):
    return (generate_l0 if level == "L0" else generate_l1)(
        inventory, context=kwargs.pop("context", CONTEXT), chunks=CHUNKS, **kwargs
    )


def removal(name, version="2.0", *, parameter=None, kind="removed", sources=SOURCES):
    return Change(name, kind, version, sources, parameter=parameter)


def answers(result):
    return {
        (i.reference.subject.symbol, i.reference.subject.parameter): i.reference.exists
        for i in result.items
        if isinstance(i.reference, ExistsReference)
    }


def item():
    return next(
        i for i in run(Inventory((symbol(),))).items if i.reference.subject.parameter is None
    )


@pytest.mark.parametrize(
    "reference",
    [
        ExistsReference(SUBJECT, True),
        ChoiceReference(SUBJECT, tuple(Option(str(i), f"name{i}") for i in range(4)), "2"),
        RequiredParametersReference(SUBJECT, ("z", "a")),
        RequiredParametersReference(SUBJECT, ()),
        DefaultReference(replace(SUBJECT, parameter="timeout"), "None"),
        PathReference(SUBJECT, "pkg.connect"),
    ],
)
def test_tagged_reference_roundtrip(reference):
    assert reference_from_json(reference_json(reference)) == reference
    assert json.loads(reference_json(reference))["kind"] == reference.kind


def test_models_are_frozen_and_validate_compatibility():
    task = item()
    with pytest.raises(FrozenInstanceError):
        task.project = "changed"
    for change in (
        {"level": "L1"},
        {"question_kind": "path"},
        {"sources": ()},
        {"chunk_ids": ()},
        {"generator_version": 0},
        {"operator_version": True},
        {"project": ""},
        {"docs_version": "3.0"},
        {"operator": "copy"},
        {"status": "approved"},
    ):
        with pytest.raises(ValueError):
            replace(task, **change)
    with pytest.raises(ValueError):
        ExistsReference(SUBJECT, 1)
    with pytest.raises(ValueError):
        Subject("pkg.connect", "next")
    with pytest.raises(ValueError):
        DefaultReference(SUBJECT, "None")
    with pytest.raises(ValueError):
        RequiredParametersReference(SUBJECT, ("x", "x"))
    with pytest.raises(ValueError):
        TaskText("question", ("question", "other"))


def test_mcq_structure_and_position_independence():
    opts = tuple(Option(str(i), f"name{i}") for i in range(4))
    ref = ChoiceReference(SUBJECT, opts, "2")
    assert replace(ref, options=tuple(reversed(opts))) == ref
    for changes in (
        {"options": opts[:3]},
        {"options": (*opts[:3], opts[0])},
        {"options": (*opts[:3], Option("3", "name0"))},
        {"correct_id": "absent"},
    ):
        with pytest.raises(ValueError):
            replace(ref, **changes)


@pytest.mark.parametrize(
    ("target", "expected"),
    [
        ("1.9", None),
        ("2.0rc1", None),
        ("2.0", False),
        ("2.0.0", False),
        ("2.10", False),
    ],
)
def test_removal_version_boundary(target, expected):
    inv = Inventory((), (removal("pkg.old"),))
    result = run(inv, context=replace(CONTEXT, docs_version=target))
    assert answers(result).get(("pkg.old", None)) is expected


def test_pep440_is_not_lexicographic():
    inv = Inventory((), (removal("pkg.old", "2.10"),))
    assert not answers(run(inv, context=replace(CONTEXT, docs_version="2.9")))


def test_deprecated_still_exists_and_planned_removal_is_not_removal():
    change = replace(removal("pkg.connect", kind="deprecated"), removal_planned="2.0")
    result = run(Inventory((symbol(),), (change,)))
    assert answers(result)[("pkg.connect", None)] is True
    assert not any(isinstance(i.reference, ChoiceReference) for i in result.items)


def test_incomplete_conflicting_and_unreviewed_evidence_is_skipped():
    cases = [
        Inventory((replace(symbol(), signatures=()),)),
        Inventory((), (removal("pkg.old", "next"),)),
        Inventory((symbol(),), (removal("pkg.connect"),)),
        Inventory((symbol(),), (removal("pkg.connect", "3", kind="added"),)),
        Inventory((), (removal("pkg.old", sources=(Source("changelog", SOURCES[0].section_id),)),)),
        Inventory((), (removal("pkg.old"), removal("pkg.old", kind="added"))),
        Inventory((), (removal("pkg.old"), removal("pkg.old", "2.1", kind="added"))),
    ]
    for inv in cases:
        result = run(inv, context=replace(CONTEXT, docs_version="2.5"))
        assert result.items == ()
        assert result.skipped
    # No negative task is fabricated for an absent arbitrary name.
    assert run(Inventory(())).items == ()


def test_readded_name_and_future_removal_do_not_make_distractors():
    changes = (
        removal("pkg.connect", "1"),
        removal("pkg.connect", "1.5", kind="added"),
        removal("pkg.connect", "3"),
    )
    assert answers(run(Inventory((symbol(),), changes)))[("pkg.connect", None)] is True


def test_mcq_uses_only_three_proven_removals_for_the_same_scope():
    changes = tuple(removal("pkg.connect", parameter=n) for n in ("old1", "old2", "old3"))
    changes += (
        removal("pkg.connect", parameter="deprecated", kind="deprecated"),
        removal("pkg.connect", "3", parameter="future"),
        removal("pkg.other", parameter="foreign"),
    )
    inv = Inventory((symbol(parameters=(parameter(), parameter("deprecated"))),), changes)
    result = run(inv)
    choices = [i.reference for i in result.items if isinstance(i.reference, ChoiceReference)]
    assert len(choices) == 2
    for ref in choices:
        wrong = {o.text for o in ref.options if o.id != ref.correct_id}
        assert wrong == {"old1", "old2", "old3"}
        assert len({o.id for o in ref.options}) == 4
    assert not any(
        isinstance(i.reference, ChoiceReference)
        for i in run(Inventory((symbol(),), changes[:2])).items
    )


def test_symbol_mcq_and_skipped_conflicting_distractors():
    changes = tuple(removal(f"pkg.old{i}") for i in range(3))
    inv = Inventory((symbol(),), changes)
    assert any(isinstance(i.reference, ChoiceReference) for i in run(inv).items)
    conflict = Conflict("pkg.old0", "kind", "removed", "deprecated", ())
    assert not any(
        isinstance(i.reference, ChoiceReference) for i in run(inv, conflicts=(conflict,)).items
    )


def test_l1_defaults_required_and_variadics():
    params = (
        parameter(),
        parameter("timeout", required=False, default="None"),
        parameter("unknown", required=False),
        parameter("args", required=False, kind="var_positional"),
        parameter("kwargs", required=False, kind="var_keyword"),
    )
    result = run(Inventory((symbol(parameters=params),)), "L1")
    required = next(i.reference for i in result.items if i.question_kind == "required-parameters")
    assert required.names == ("host",)
    defaults = [i.reference for i in result.items if i.question_kind == "default"]
    assert defaults == [DefaultReference(replace(SUBJECT, parameter="timeout"), "None")]
    assert any("unknown" in s.reason for s in result.skipped)
    path_item = next(i for i in result.items if i.question_kind == "path")
    assert path_item.reference.path == "pkg.connect"
    assert "pkg.connect" not in path_item.model_prompt().text


def test_empty_required_set_is_known_not_missing():
    result = run(Inventory((symbol(parameters=()),)), "L1")
    assert (
        next(i.reference.names for i in result.items if i.question_kind == "required-parameters")
        == ()
    )


def test_overloads_unreliable_missing_and_ambiguous_short_name():
    base = symbol()
    overloaded = replace(
        base, signatures=(*base.signatures, Signature((parameter("other"),), SOURCES))
    )
    assert run(Inventory((overloaded,)), "L1").items == ()
    for bad in (
        replace(base, signatures=()),
        replace(base, signatures=(replace(base.signatures[0], sources=()),)),
        symbol(parameters=(replace(parameter(), sources=()),)),
        symbol(parameters=(parameter(), parameter())),
    ):
        assert not run(Inventory((bad,)), "L1").items
    result = run(Inventory((base, symbol("other.connect"))), "L1")
    assert not any(i.question_kind == "path" for i in result.items)
    assert any(i.question_kind == "required-parameters" for i in result.items)


def test_identity_ignores_wording_generator_and_snapshot_but_not_answers_or_operator():
    original = item()
    assert (
        original.id
        == replace(
            original,
            wording=TaskText("New?", ("Another?", "Third?")),
            generator_version=2,
            input_snapshot_hash=content_hash("typo"),
            docs_version="2.0.0",
        ).id
    )
    assert original.id != replace(original, operator_version=2).id
    assert original.id != replace(original, reference=replace(original.reference, exists=False)).id
    assert (
        original.id
        != replace(
            original,
            reference=replace(original.reference, subject=replace(SUBJECT, symbol="pkg.other")),
        ).id
    )


def test_reordering_input_keeps_ids_references_and_output_bytes():
    inv = Inventory(
        (symbol(), symbol("pkg.other")), tuple(removal(f"pkg.old{i}") for i in range(4))
    )
    reverse = Inventory(tuple(reversed(inv.symbols)), tuple(reversed(inv.changes)))
    assert dumps(run(inv)) == dumps(run(reverse))
    params = (parameter("a"), parameter("b"), parameter("c", required=False, default="3"))
    first = run(Inventory((symbol(parameters=params),)), "L1")
    second = run(Inventory((symbol(parameters=tuple(reversed(params))),)), "L1")
    assert dumps(first) == dumps(second)


def test_model_payload_has_no_internal_answer_fields_or_defaults():
    inv = Inventory((symbol(parameters=(parameter("token", required=False, default="'SECRET'"),)),))
    task = next(i for i in run(inv, "L1").items if i.question_kind == "default")
    payload = json.loads(canonical_json(task.model_prompt()))
    assert set(payload) == {"text", "answer_format", "options"}
    assert "SECRET" not in json.dumps(payload)
    assert task.model_prompt(paraphrase=0).text == task.wording.paraphrases[0]


def test_reuse_preserves_whole_frozen_item_and_never_calls_writer():
    class NoWriter:
        def write(self, question):
            pytest.fail("writer must not be called on reuse")

    inv = Inventory((symbol(),))
    original = run(inv)
    updated = run(
        inv,
        existing=original.items,
        writer=NoWriter(),
        context=replace(
            CONTEXT, generator_version=2, input_snapshot_hash=content_hash("new snapshot")
        ),
    )
    assert updated == original


def test_export_import_rejects_tampering_duplicates_and_overwrites(tmp_path):
    result = run(Inventory((symbol(),)))
    path = tmp_path / "tasks.json"
    save(path, result)
    assert load(path) == result
    assert dumps(loads(dumps(result))) == dumps(result)
    with pytest.raises(FileExistsError):
        save(path, result)
    data = json.loads(dumps(result))
    data["items"][0]["reference"]["exists"] = not data["items"][0]["reference"]["exists"]
    with pytest.raises(ValueError, match="identity"):
        loads(json.dumps(data))
    data = json.loads(dumps(result))
    data["items"].append(data["items"][0])
    with pytest.raises(ValueError, match="duplicate"):
        loads(json.dumps(data))
    with pytest.raises(ValueError, match="duplicate JSON"):
        loads('{"schema_version":1,"schema_version":1}')


def test_existing_sphinx_ingestion_to_tasks_and_local_entrypoint(tmp_path):
    config = IngestConfig(
        FIXTURE, content_hash("config"), "fixturelib", (), None, None, "xml-plain"
    )
    ingestion = ingest(config, output=tmp_path / "ingestion")
    context = GenerationContext("fixturelib", "2.0", ingestion.input_hash)
    results = [
        generate(
            ingestion.inventory,
            context=context,
            chunks=ingestion.chunks,
            conflicts=ingestion.conflicts,
        )
        for generate in (generate_l0, generate_l1)
    ]
    result = GenerationResult(tuple(i for r in results for i in r.items), ())
    assert answers(results[0])[("fixturelib.connect", None)] is True
    defaults = [i.reference for i in result.items if isinstance(i.reference, DefaultReference)]
    assert DefaultReference(Subject("fixturelib.connect", "2", "timeout"), "None") in defaults
    required = [
        i.reference for i in result.items if isinstance(i.reference, RequiredParametersReference)
    ]
    assert RequiredParametersReference(Subject("fixturelib.connect", "2"), ("host",)) in required
    out = tmp_path / "tasks.json"
    assert (
        main(
            [
                str(FIXTURE / "xml-plain"),
                "--project",
                "fixturelib",
                "--docs-version",
                "2.0",
                "--out",
                str(out),
            ]
        )
        == 0
    )
    assert {i.id for i in load(out).items} == {i.id for i in result.items}
    assert all(i.status == "candidate" and i.wording.writer == "template-v1" for i in result.items)


def test_mcq_writer_and_model_only_receive_neutral_scope_and_options():
    questions = []

    class RecordingWriter(TemplateWriter):
        def write(self, question):
            questions.append(question)
            return super().write(question)

    inv = Inventory((symbol(),), tuple(removal(f"pkg.old{i}") for i in range(3)))
    result = run(inv, writer=RecordingWriter())
    task = next(i for i in result.items if isinstance(i.reference, ChoiceReference))
    assert task.reference.subject.symbol == "pkg.connect"
    question = next(q for q in questions if q.kind == "choice")
    assert question.subject.symbol == CONTEXT.project
    assert question.display_name == CONTEXT.project
    payload = json.loads(canonical_json(task.model_prompt()))
    assert "correct_id" not in payload and "reference" not in payload
    assert len(payload["options"]) == 4
    assert payload["answer_format"] == "option-id"


def test_low_confidence_parameter_cannot_become_positive_or_removed_distractor():
    weak = Source("example", SOURCES[0].section_id)
    p = replace(parameter(), sources=(weak,))
    inv = Inventory((symbol(parameters=(p,)),))
    assert ("pkg.connect", "host") not in answers(run(inv))
    changes = (removal("pkg.connect", parameter="host"),)
    assert ("pkg.connect", "host") not in answers(run(replace(inv, changes=changes)))


def test_missing_chunks_conflicts_and_out_of_scope_inputs():
    inv = Inventory((symbol(),))
    result = generate_l0(inv, context=CONTEXT, chunks=())
    assert result.items == () and any("missing" in s.reason for s in result.skipped)
    conflict = Conflict("pkg.connect", "default", "1", "2", SOURCES)
    assert not run(inv, "L1", conflicts=(conflict,)).items
    operation = replace(symbol(), kind="operation")
    assert not run(Inventory((operation,))).items
    assert not run(Inventory((operation,)), "L1").items
    changed = replace(inv, changes=(removal("pkg.connect", parameter="host"),))
    assert not run(changed, "L1").items


def test_reference_decoder_rejects_wrong_tags_fields_and_types():
    invalid = [
        {},
        {"kind": "unknown"},
        {
            "kind": "exists",
            "subject": {"symbol": "x", "version": "2", "parameter": None},
            "exists": "false",
        },
        {
            "kind": "required-parameters",
            "subject": {
                "symbol": "x",
                "version": "2",
                "parameter": None,
            },
            "names": "host",
        },
    ]
    for value in invalid:
        with pytest.raises(ValueError):
            reference_from_json(json.dumps(value))
    result = json.loads(dumps(run(Inventory((symbol(),)))))
    result["items"][0]["sources"][0]["type"] = "unknown"
    with pytest.raises(ValueError):
        loads(json.dumps(result))


def test_reuse_rejects_two_different_frozen_texts_with_the_same_id():
    original = item()
    other = replace(original, wording=TaskText("Other", ("Variant 1", "Variant 2")))
    with pytest.raises(ValueError, match="same identity"):
        run(Inventory((symbol(),)), existing=(original, other))
