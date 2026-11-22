"""Regression cases from PR #44, including the actual urllib3 Sphinx inventory."""

import json
from collections import Counter
from dataclasses import replace
from pathlib import Path

import pytest

from notinspec.adapters.canonical import canonical_json, content_hash
from notinspec.chunking import Document, chunk_blocks, chunk_document
from notinspec.inventory import Change, Inventory, Signature, Source, Symbol, build_inventory
from notinspec.sphinx import read_sphinx_xml
from notinspec.tasks import (
    ChoiceReference,
    ExistsReference,
    GenerationContext,
    GenerationResult,
    Question,
    TaskText,
    TemplateWriter,
    generate_l0,
    generate_l1,
    loads,
)
from notinspec.tasks.serialization import dumps


class NoWriter:
    def write(self, question: Question) -> TaskText:
        pytest.fail("skipped/reused tasks must not invoke the writer")


@pytest.fixture(scope="module")
def urllib3():
    root = Path(__file__).parents[2] / "examples" / "sphinx" / "urllib3" / "xml"
    xml = read_sphinx_xml(root)
    chunks = tuple(c for d in xml.documents for c in chunk_blocks(d, project="urllib3"))
    return build_inventory(chunks), chunks, content_hash(dict(xml.files))


def test_real_urllib3_cannot_be_scored_by_always_answering_yes(urllib3):
    built, chunks, snapshot = urllib3
    result = generate_l0(
        built.inventory,
        context=GenerationContext("urllib3", "2.8.0", snapshot),
        chunks=chunks,
        conflicts=built.conflicts,
        writer=NoWriter(),
    )
    assert result.items == ()
    assert any("need both classes" in s.reason and "no=0" in s.reason for s in result.skipped)


@pytest.mark.parametrize("label", ["2.8.1", "latest", "main"])
def test_real_urllib3_label_change_reuses_ids_references_and_text(urllib3, label):
    built, chunks, snapshot = urllib3
    ctx = GenerationContext("urllib3", "2.8.0", snapshot)
    original = generate_l1(built.inventory, context=ctx, chunks=chunks, conflicts=built.conflicts)
    new = generate_l1(
        built.inventory,
        context=replace(ctx, docs_version=label),
        chunks=chunks,
        conflicts=built.conflicts,
    )
    assert original.items
    assert [i.id for i in new.items] == [i.id for i in original.items]
    assert [i.reference for i in new.items] == [i.reference for i in original.items]
    assert [i.wording for i in new.items] == [i.wording for i in original.items]
    assert all(i.docs_version == label for i in new.items)
    reused = generate_l1(
        built.inventory,
        context=replace(ctx, docs_version=label, generator_version=3),
        chunks=chunks,
        conflicts=built.conflicts,
        existing=original.items,
        writer=NoWriter(),
    )
    assert reused == original


def test_real_path_writer_payload_contains_no_qualified_answer(urllib3):
    built, chunks, snapshot = urllib3
    seen = []

    class InspectWriter(TemplateWriter):
        def write(self, question):
            if question.kind == "path":
                seen.append(question)
                assert question.subject.symbol == question.display_name
            return super().write(question)

    result = generate_l1(
        built.inventory,
        context=GenerationContext("urllib3", "latest", snapshot),
        chunks=chunks,
        conflicts=built.conflicts,
        writer=InspectWriter(),
    )
    paths = {
        i.reference.path.rsplit(".", 1)[-1]: i.reference.path
        for i in result.items
        if i.question_kind == "path"
    }
    assert len(seen) == len(paths) > 0
    for question in seen:
        # Check all fields received by any future writer, not just TemplateWriter's output.
        assert paths[question.display_name] not in canonical_json(question).decode()


@pytest.fixture
def mixed():
    chunks = chunk_document(Document("api.md", "# API\nKnown functions."), project="pkg")
    sources = (Source("signature", chunks[0].section_id),)
    symbols = tuple(
        Symbol(f"pkg.function{n}", "function", sources, (Signature((), sources),)) for n in range(5)
    )
    changes = tuple(Change(f"pkg.old{n}", "removed", "2.0", sources) for n in range(3))
    return Inventory(symbols, changes), chunks, GenerationContext("pkg", "2.8.0", "snapshot")


def test_yes_no_has_both_classes_balanced_before_writing(mixed):
    inventory, chunks, ctx = mixed
    seen = []

    class InspectWriter(TemplateWriter):
        def write(self, question):
            seen.append(question)
            return super().write(question)

    result = generate_l0(inventory, context=ctx, chunks=chunks, writer=InspectWriter())
    counts = Counter(i.reference.exists for i in result.items if i.question_kind == "exists")
    assert counts == {True: 3, False: 3}
    assert len(seen) == len(result.items)
    assert any("omitted 2" in s.reason for s in result.skipped)
    reverse = replace(inventory, symbols=tuple(reversed(inventory.symbols)))
    assert dumps(result) == dumps(generate_l0(reverse, context=ctx, chunks=chunks))


def test_missing_negative_source_cannot_leave_a_yes_only_test(mixed):
    inventory, chunks, ctx = mixed
    unavailable = (Source("signature", "not-in-input"),)
    inventory = replace(
        inventory, changes=tuple(replace(c, sources=unavailable) for c in inventory.changes)
    )
    result = generate_l0(inventory, context=ctx, chunks=chunks, writer=NoWriter())
    assert result.items == ()
    assert any("need both classes" in s.reason for s in result.skipped)


def test_current_l0_reference_is_label_independent_but_change_reference_is_versioned(mixed):
    inventory, chunks, ctx = mixed
    old = generate_l0(inventory, context=ctx, chunks=chunks)
    new = generate_l0(inventory, context=replace(ctx, docs_version="2.8.1"), chunks=chunks)

    def current(result: GenerationResult) -> set[str]:
        return {
            i.id
            for i in result.items
            if isinstance(i.reference, ExistsReference) and i.reference.exists
        }

    def removed(result: GenerationResult) -> set[str]:
        return {
            i.id
            for i in result.items
            if isinstance(i.reference, ExistsReference) and not i.reference.exists
        }

    assert current(old) == current(new) and current(old)
    assert removed(old).isdisjoint(removed(new)) and removed(old)
    assert all(
        i.reference.tested_version == "2.8.1"
        for i in new.items
        if isinstance(i.reference, ExistsReference) and not i.reference.exists
    )
    explicit = generate_l0(
        inventory, context=replace(ctx, docs_version="main", api_version="2.8.0"), chunks=chunks
    )
    assert {i.id for i in explicit.items} == {i.id for i in old.items}
    unknown = generate_l0(inventory, context=replace(ctx, docs_version="main"), chunks=chunks)
    assert unknown.items == ()
    assert any("comparable API version" in s.reason for s in unknown.skipped)


def test_mcq_letters_map_back_to_internal_ids_in_each_presented_order(mixed):
    inventory, chunks, ctx = mixed
    result = generate_l0(inventory, context=ctx, chunks=chunks)
    item = next(i for i in result.items if isinstance(i.reference, ChoiceReference))
    ref = item.reference
    for order in (None, tuple(o.id for o in reversed(ref.options))):
        prompt = item.model_prompt(option_order=order)
        assert prompt.answer_format == "choice-label"
        assert [o.label for o in prompt.options] == list("ABCD")
        for option in prompt.options:
            internal = next(o for o in ref.options if o.text == option.text)
            assert ref.option_id(option.label, order) == internal.id
        payload = canonical_json(prompt).decode()
        assert all(o.id not in payload for o in ref.options)
        assert "correct_id" not in payload
    restored = loads(dumps(result))
    restored_ref = next(i.reference for i in restored.items if i.id == item.id)
    assert restored_ref.model_options() == ref.model_options()
    with pytest.raises(ValueError):
        ref.option_id("E")
    with pytest.raises(ValueError):
        item.model_prompt(option_order=(ref.options[0].id,) * 4)


def test_v1_exports_are_rejected_without_silent_identity_migration():
    with pytest.raises(ValueError, match="schema version"):
        loads(json.dumps({"schema_version": 1, "items": [], "skipped": []}))


def test_invalid_api_version_is_rejected_but_display_labels_are_allowed():
    assert GenerationContext("pkg", "latest", "snapshot").comparison_version is None
    with pytest.raises(ValueError, match="api_version"):
        GenerationContext("pkg", "main", "snapshot", api_version="tomorrow")
