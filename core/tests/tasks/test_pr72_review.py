"""Regressions for answer leakage, stale-rule reuse and diagnostics in PR #72."""

from dataclasses import replace

import pytest

from notinspec.chunking import Document, chunk_document
from notinspec.inventory import Change, Inventory, Parameter, Signature, Source, Symbol
from notinspec.tasks import GenerationContext, TaskText, TemplateWriter, generate_l0, generate_l1


def fixture(*parameters):
    chunks = chunk_document(Document("api.md", "# API\nDocumented API."), project="pkg")
    sources = (Source("signature", chunks[0].section_id),)
    params = tuple(Parameter(p, "keyword_only", True, sources) for p in parameters)
    symbol = Symbol("pkg.fetch_pool", "function", sources, (Signature(params, sources),))
    return Inventory((symbol,)), chunks, GenerationContext("pkg", "2.0", "snapshot")


@pytest.mark.parametrize("parameters", [(), ("get_pool",)])
def test_single_anchor_cannot_make_its_own_mcq(parameters):
    inv, chunks, ctx = fixture(*parameters)
    result = generate_l0(inv, context=ctx, chunks=chunks)
    assert result.items  # yes/no remains available
    assert not any(i.question_kind == "choice" for i in result.items)


def test_shared_edit_is_excluded_for_every_originating_anchor():
    inv, chunks, ctx = fixture("get_pool", "fetch_pools", "max_size")
    result = generate_l0(inv, context=ctx, chunks=chunks)
    refs = [i.reference for i in result.items if i.question_kind == "choice"]
    assert {r.subject.parameter for r in refs} == {"get_pool", "fetch_pools", "max_size"}
    for ref in refs:
        wrong = {o.text for o in ref.options if o.id != ref.correct_id}
        if ref.subject.parameter in ("get_pool", "fetch_pools"):
            # get_pool -> get_pools and fetch_pools -> get_pools. Remember BOTH origins.
            assert "get_pools" not in wrong
    assert any(
        i.reference.subject.parameter == "get_pools" and not i.reference.exists
        for i in result.items
        if i.question_kind == "exists"
    )


@pytest.mark.parametrize("label,api_version", [("2.0", None), ("latest", "2.0")])
def test_removals_positives_and_near_misses_have_the_same_writer_framing(label, api_version):
    inv, chunks, ctx = fixture("pool_key", "read_timeout", "max_size")
    inv = replace(inv, changes=(Change("pkg.old", "removed", "1.0", inv.symbols[0].sources),))
    seen = []

    class Capture(TemplateWriter):
        def write(self, question):
            seen.append(question)
            return super().write(question)

    result = generate_l0(
        inv,
        context=replace(ctx, docs_version=label, api_version=api_version),
        chunks=chunks,
        writer=Capture(),
    )
    yes_no = [i for i in result.items if i.question_kind == "exists"]
    assert any(i.reference.exists for i in yes_no)
    assert any(not i.reference.exists and i.reference.tested_version for i in yes_no)
    assert any(not i.reference.exists and i.reference.tested_version is None for i in yes_no)
    assert all(q.tested_version is None for q in seen)
    for item in yes_no:
        assert all(
            "according to the supplied documentation" in text and "in version" not in text
            for text in (item.wording.text, *item.wording.paraphrases)
        )


@pytest.mark.parametrize("version", [1, 2, 3])
def test_old_l0_override_is_rejected_even_without_candidates(version):
    inv, chunks, ctx = fixture("pool_key")
    with pytest.raises(ValueError, match="L0 operator_version must be at least 4"):
        generate_l0(Inventory(()), context=replace(ctx, operator_version=version), chunks=chunks)
    old_l1 = generate_l1(inv, context=replace(ctx, operator_version=2), chunks=chunks)
    assert old_l1.items and all(i.operator_version == 2 for i in old_l1.items)


def test_v3_frozen_l0_items_are_not_reused_under_corrected_rules():
    inv, chunks, ctx = fixture("pool_key")
    current = generate_l0(inv, context=ctx, chunks=chunks)
    old = tuple(
        replace(i, operator_version=3, wording=TaskText("Old", ("Old 1", "Old 2")))
        for i in current.items
    )
    updated = generate_l0(inv, context=ctx, chunks=chunks, existing=old)
    assert updated == current
    assert {i.id for i in old}.isdisjoint(i.id for i in updated.items)
    with pytest.raises(ValueError, match="L0 operator_version"):
        generate_l0(inv, context=replace(ctx, operator_version=3), chunks=chunks, existing=old)


def test_diagnostics_are_aggregated_per_namespace():
    inv, chunks, ctx = fixture()
    base = inv.symbols[0]
    inv = Inventory(
        tuple(replace(base, path=name) for name in ("pkg.func0", "pkg.func1", "pkg.other.func2"))
    )
    result = generate_l0(inv, context=ctx, chunks=chunks)
    skips = [s for s in result.skipped if s.question_kind == "choice"]
    assert len(skips) == 2
    assert {s.symbol for s in skips} == {"pkg", "pkg.other"}
    no_edits = [s for s in result.skipped if s.reason.startswith("no safe near-miss")]
    assert len(no_edits) == 2
    assert any(s.symbol == "pkg" and "2 anchors" in s.reason for s in no_edits)
