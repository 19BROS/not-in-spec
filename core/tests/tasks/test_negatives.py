"""Absence is a snapshot-wide veto, not an inference from a missing local parameter."""

from collections import Counter
from dataclasses import replace

import pytest

from notinspec.chunking import Document, chunk_document
from notinspec.inventory import Change, Conflict, Inventory, Parameter, Signature, Source, Symbol
from notinspec.tasks import (
    GenerationContext,
    TemplateWriter,
    dumps,
    generate_l0,
    generate_l1,
    loads,
)
from notinspec.tasks.negatives import AbsenceIndex, near_misses


@pytest.fixture
def api():
    chunks = chunk_document(
        Document("api.md", "# API\nfetch_pool(pool_key, read_timeout, max_size)"), project="pkg"
    )
    sources = (Source("signature", chunks[0].section_id),)
    params = tuple(
        Parameter(n, "keyword_only", True, sources)
        for n in ("pool_key", "read_timeout", "max_size")
    )
    symbol = Symbol("pkg.fetch_pool", "function", sources, (Signature(params, sources),))
    return Inventory((symbol,)), chunks, GenerationContext("pkg", "latest", "snapshot")


def negative_names(result):
    return {
        i.reference.subject.parameter or i.reference.subject.symbol
        for i in result.items
        if i.question_kind == "exists" and not i.reference.exists
    }


@pytest.mark.parametrize(
    "name",
    [
        "_private",
        "__getattr__",
        "x",
        "CONSTANT",
        "x2",
        "has__gap",
        "réseau",
        "set_X",
        "Pool_Manager",
    ],
)
def test_no_arbitrary_private_or_ambiguous_names(name):
    assert near_misses(name) == ()


def test_lexical_proposals_preserve_style_and_are_bounded():
    assert near_misses("get_pool") == ("fetch_pool", "get_pools", "pool_get")
    assert near_misses("getPool") == ("fetchPool", "getPools", "poolGet")
    assert near_misses("GetPool") == ("FetchPool", "GetPools", "PoolGet")
    assert near_misses("proxy") == ("proxies",)
    assert near_misses("HTTPPool") == ()
    assert all(n.isidentifier() for n in near_misses("point_y"))
    assert all(n.isidentifier() for n in near_misses("point_s"))


@pytest.mark.parametrize(
    "name",
    [
        "hosts",
        "headers",
        "addresses",
        "retries",
        "kwargs",
        "has",
        "alias",
        "analysis",
        "series",
        "status",
    ],
)
def test_ambiguous_s_endings_are_not_singularized_or_pluralized(name):
    assert near_misses(name) == ()


@pytest.mark.parametrize(
    "mention",
    [
        "pool_keys",
        "POOL_KEYS",
        "other.pool_keys",
        "prefix_pool_keys_suffix",
        "[alias](https://docs.example/pool_keys)",
        "ｐｏｏｌ＿ｋｅｙｓ",
        "```python\ncall(pool_keys=1)\n```",
        "| name |\n| --- |\n| pool_keys |",
        r"pool\_keys",
        "pool&#95;keys",
        "pool&lowbar;keys",
        "pool_\u00adkeys",
        "pool_\u200bkeys",
        "pool_\u200dkeys",
        r"pool_\u200bkeys",
        r"pool\u005fkeys",
        "pool\\_&#x200b;keys",
    ],
)
def test_mention_anywhere_in_docs_vetoes_short_name(api, mention):
    inventory, chunks, ctx = api
    extra = chunk_document(Document("guide.md", f"# Guide\n{mention}"), project="pkg")
    index = AbsenceIndex(inventory, chunks + extra, ())
    assert not index.absent("pool_keys")
    assert not index.absent("pkg.pool_keys")
    result = generate_l0(inventory, context=ctx, chunks=chunks + extra)
    assert "pool_keys" not in negative_names(result)
    assert all(
        "pool_keys" not in {o.text for o in i.reference.options}
        for i in result.items
        if i.question_kind == "choice"
    )


@pytest.mark.parametrize("kind", ["symbol", "parameter", "change", "replacement", "conflict"])
def test_inventory_and_conflict_mentions_veto_even_without_doc_text(api, kind):
    inventory, chunks, _ = api
    weak = (Source("example", chunks[0].section_id),)
    conflicts = ()
    if kind == "symbol":
        inventory = replace(
            inventory, symbols=(*inventory.symbols, Symbol("other.pool_keys", "function", weak))
        )
    elif kind == "parameter":
        p = Parameter("pool_keys", "keyword_only", True, weak)
        other = Symbol("other.func", "function", weak, (Signature((p,), weak),))
        inventory = replace(inventory, symbols=(*inventory.symbols, other))
    elif kind in ("change", "replacement"):
        change = Change(
            "pkg.old",
            "deprecated",
            "next",
            weak,
            parameter="pool_keys" if kind == "change" else None,
            replacement="pool_keys" if kind == "replacement" else None,
        )
        inventory = replace(inventory, changes=(change,))
    else:
        conflicts = (Conflict("pkg.pool_keys", "kind", "function", "class", weak),)
    assert not AbsenceIndex(inventory, chunks, conflicts).absent("pool_keys")


@pytest.mark.parametrize("ambiguity", ["kwargs", "overload", "weak"])
def test_ambiguous_signatures_do_not_generate_parameter_negatives(api, ambiguity):
    inventory, chunks, ctx = api
    symbol = inventory.symbols[0]
    sig = symbol.signatures[0]
    if ambiguity == "kwargs":
        sig = replace(
            sig,
            parameters=(*sig.parameters, Parameter("kwargs", "var_keyword", False, sig.sources)),
        )
        symbol = replace(symbol, signatures=(sig,))
    elif ambiguity == "overload":
        symbol = replace(symbol, signatures=(sig, replace(sig, text="other overload")))
    else:
        sig = replace(sig, parameters=(replace(sig.parameters[0], sources=()),))
        symbol = replace(symbol, signatures=(sig,))
    result = generate_l0(Inventory((symbol,)), context=ctx, chunks=chunks)
    assert all(
        i.reference.subject.parameter is None
        for i in result.items
        if i.question_kind == "exists" and not i.reference.exists
    )


def test_missing_split_part_disables_absence_evidence(api):
    inventory, chunks, ctx = api
    partial = (replace(chunks[0], parts=2),)
    result = generate_l0(inventory, context=ctx, chunks=partial)
    assert result.items == ()
    assert any("need both classes" in s.reason for s in result.skipped)
    assert (
        sum(s.reason == "near misses disabled: incomplete chunk set" for s in result.skipped) == 1
    )
    assert not any("no safe near-miss" in s.reason for s in result.skipped)


def test_balanced_deterministic_roundtrip_and_label_reuse(api):
    inventory, chunks, ctx = api
    original = generate_l0(inventory, context=ctx, chunks=chunks)
    counts = Counter(i.reference.exists for i in original.items if i.question_kind == "exists")
    assert counts[True] == counts[False] > 0
    assert any(i.question_kind == "choice" for i in original.items)
    assert loads(dumps(original)) == original
    reverse = generate_l0(inventory, context=ctx, chunks=tuple(reversed(chunks)))
    assert dumps(original) == dumps(reverse)

    class NoWriter:
        def write(self, question):
            pytest.fail("must reuse frozen wording")

    for label in ("main", "2.0", "2.1"):
        result = generate_l0(
            inventory,
            context=replace(ctx, docs_version=label),
            chunks=chunks,
            existing=original.items,
            writer=NoWriter(),
        )
        assert result == original
    assert all(i.operator_version == 4 and i.generator_version == 4 for i in original.items)
    l1 = generate_l1(inventory, context=ctx, chunks=chunks)
    old_l1 = generate_l1(
        inventory, context=replace(ctx, generator_version=2, operator_version=2), chunks=chunks
    )
    assert [i.id for i in l1.items] == [i.id for i in old_l1.items]


def test_new_doc_mention_invalidates_old_negative_before_reuse(api):
    inventory, chunks, ctx = api
    original = generate_l0(inventory, context=ctx, chunks=chunks)
    names = negative_names(original)
    assert names
    extra = chunk_document(
        Document("aliases.md", "# Aliases\n" + "\n".join(sorted(names))), project="pkg"
    )
    current = generate_l0(
        inventory,
        context=replace(ctx, input_snapshot_hash="changed"),
        chunks=chunks + extra,
        existing=original.items,
    )
    assert not (negative_names(current) & names)
    for item in current.items:
        if item.question_kind == "choice":
            assert not (
                {o.text for o in item.reference.options if o.id != item.reference.correct_id}
                & names
            )


def test_writer_gets_no_absence_or_generation_hint(api):
    inventory, chunks, ctx = api
    questions = []

    class Capture(TemplateWriter):
        def write(self, question):
            questions.append(question)
            return super().write(question)

    result = generate_l0(inventory, context=ctx, chunks=chunks, writer=Capture())
    assert len(questions) == len(result.items)
    assert all(q.tested_version is None for q in questions)
    assert all(not hasattr(q, "exists") and not hasattr(q, "strategy") for q in questions)
    assert all("documented API" in i.wording.text for i in result.items)
