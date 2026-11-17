import itertools

from notinspec.inventory import (
    Change,
    Conflict,
    Inventory,
    Parameter,
    ReturnType,
    Signature,
    Source,
    Symbol,
    change_key,
    merge,
    parse_version,
)

DIRECTIVE = Source("signature", section_id="a" * 16)
SECOND = Source("signature", section_id="b" * 16)
CHANGELOG = Source("changelog", section_id="c" * 16)
SPEC = Source("spec", pointer="/paths/~1x/get")


def signature(source: Source, default: str | None = None, returns: str = "str") -> Signature:
    timeout = Parameter(
        "timeout", "positional_or_keyword", default is None, (source,), default=default
    )
    return Signature(
        (timeout,), (source,), text="f(timeout)", returns=ReturnType(returns, (source,))
    )


def symbol(source: Source, *signatures: Signature, kind: str = "function") -> Symbol:
    return Symbol("pkg.f", kind, (source,), signatures)


def test_pep_440_versions() -> None:
    assert parse_version("2.0") == parse_version("2.0.0")
    assert parse_version("next") is None
    a = Change("pkg.f", "deprecated", "2.0", (DIRECTIVE,))
    assert change_key(a) == change_key(Change("pkg.f", "deprecated", "2.0.0", (CHANGELOG,)))
    assert change_key(a) != change_key(Change("pkg.f", "deprecated", "2.1", (DIRECTIVE,)))
    assert change_key(Change("pkg.f", "added", "next", (DIRECTIVE,)))[3] == "next"


def test_one_change_from_a_directive_and_the_changelog() -> None:
    """urllib3 2.0.0: `format_header_param` from its directive and from the changelog (§6.3)."""
    directive = Change("pkg.f", "deprecated", "2.0.0", (DIRECTIVE,))
    claim = Change(
        "pkg.f", "deprecated", "2.0", (CHANGELOG,), replacement="pkg.g", removal_planned="3.0"
    )
    inventory, conflicts = merge([Inventory((), (claim,)), Inventory((), (directive,))])
    (change,) = inventory.changes
    assert change.version == "2.0.0"  # the directive ranks above the changelog
    assert change.sources == (DIRECTIVE, CHANGELOG)
    assert (change.replacement, change.removal_planned) == ("pkg.g", "3.0")  # filled from D
    assert conflicts == ()


def test_different_attributes_under_one_key_are_conflicts() -> None:
    """urllib3: "removed in v3.0" in the API reference, "in v2.1.0" in the changelog (§6.3)."""
    reference = Change("pkg.f", "deprecated", "2.0", (DIRECTIVE,), removal_planned="3.0")
    log = Change(
        "pkg.f", "deprecated", "2.0", (CHANGELOG,), replacement="pkg.h", removal_planned="2.1.0"
    )
    same = Change("pkg.f", "deprecated", "2.0", (SECOND,), removal_planned="3.0.0")
    inventory, conflicts = merge([Inventory((), (c,)) for c in (log, reference, same)])
    assert inventory.changes[0].removal_planned == "3.0"
    assert conflicts == (
        Conflict("pkg.f deprecated 2.0", "removal_planned", "3.0", "2.1.0", (CHANGELOG,)),
    )  # 3.0 == 3.0.0; a replacement only one side has is no conflict


def test_equal_signatures_merge_and_overloads_of_one_source_stay() -> None:
    a = symbol(DIRECTIVE, signature(DIRECTIVE))
    b = symbol(SECOND, signature(SECOND), signature(SECOND, default="1"))
    inventory, conflicts = merge([Inventory((b,)), Inventory((a,))])
    (merged,) = inventory.symbols
    assert merged.sources == (DIRECTIVE, SECOND)
    assert len(merged.signatures) == 2  # b's two overloads share a source: never one
    plain = next(s for s in merged.signatures if s.parameters[0].default is None)
    assert plain.sources == plain.parameters[0].sources == (DIRECTIVE, SECOND)
    assert plain.returns is not None and plain.returns.sources == (DIRECTIVE, SECOND)
    assert conflicts == ()  # the identical one merged, not the one with a default


def test_differences_between_sources_are_conflicts_not_overloads() -> None:
    """`pkg.f` documented in two sections, one with a default, a type and another return."""
    a = symbol(DIRECTIVE, signature(DIRECTIVE))
    b_timeout = Parameter("timeout", "positional_or_keyword", False, (SECOND,), "float", "1")
    b = symbol(SECOND, Signature((b_timeout,), (SECOND,), returns=ReturnType("bytes", (SECOND,))))
    inventory, conflicts = merge([Inventory((b,)), Inventory((a,))])
    (merged,) = inventory.symbols[0].signatures
    (timeout,) = merged.parameters
    assert (timeout.required, timeout.default, timeout.type) == (True, None, "float")
    assert merged.returns == ReturnType("str", (DIRECTIVE,))
    assert {(c.subject, c.attribute, c.kept, c.other) for c in conflicts} == {
        ("pkg.f(timeout)", "required", "True", "False"),
        ("pkg.f", "returns", "str", "bytes"),
    }  # a type only one side documents fills the gap; `default` only one side has


def test_the_best_source_wins_a_symbol_kind() -> None:
    inventory, conflicts = merge(
        [Inventory((symbol(CHANGELOG, kind="method"),)), Inventory((symbol(SPEC),))]
    )
    assert inventory.symbols[0].kind == "function"
    assert conflicts == (Conflict("pkg.f", "kind", "function", "method", (CHANGELOG,)),)


def test_merge_does_not_depend_on_order() -> None:
    parts = [
        Inventory((symbol(DIRECTIVE, signature(DIRECTIVE)),)),
        Inventory((symbol(SECOND, signature(SECOND, returns="bytes"), kind="method"),)),
        Inventory((), (Change("pkg.f", "deprecated", "2.0", (CHANGELOG,), replacement="x"),)),
        Inventory((), (Change("pkg.f", "deprecated", "2.0.0", (SECOND,), replacement="y"),)),
    ]
    results = {merge(p) for p in itertools.permutations(parts)}
    assert len(results) == 1


def test_a_value_only_one_source_has_is_no_conflict() -> None:
    with_value = Change("pkg.f", "removed", "2.0", (DIRECTIVE,), replacement="pkg.g")
    without = Change("pkg.f", "removed", "2.0", (CHANGELOG,))
    other = Change("pkg.f", "removed", "2.0", (SECOND,), replacement="pkg.h")
    assert merge([Inventory((), (with_value,)), Inventory((), (without,))])[1] == ()
    _, conflicts = merge([Inventory((), (c,)) for c in (without, other, with_value)])
    assert conflicts == (Conflict("pkg.f removed 2.0", "replacement", "pkg.g", "pkg.h", (SECOND,)),)
