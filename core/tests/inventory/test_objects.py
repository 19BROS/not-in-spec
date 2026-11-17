import dataclasses

import orjson
import pytest

from notinspec.adapters.canonical import canonical_json, content_hash
from notinspec.inventory import (
    Change,
    Constraint,
    Inventory,
    Parameter,
    ReturnType,
    Signature,
    Source,
    Symbol,
)

SIGNATURE = Source("signature", section_id="s" * 16)
EXAMPLE = Source("example", section_id="e" * 16)
CHANGELOG = Source("changelog", section_id="c" * 16)
SPEC = Source("spec", pointer="/paths/~1orders/post")


def format_header_param(sources: tuple[Source, ...] = (SIGNATURE,)) -> Symbol:
    params = (
        Parameter("name", "positional_or_keyword", True, sources, type="str"),
        Parameter("value", "positional_or_keyword", True, sources, type="str | bytes"),
    )
    signature = Signature(
        params, sources, text="format_header_param(name, value)", returns=ReturnType("str", sources)
    )
    return Symbol("urllib3.fields.format_header_param", "function", sources, (signature,))


def renamed(sources: tuple[Source, ...]) -> Change:
    """urllib3 2.0.0: mentioned by a directive and the changelog, one key (SPEC §6.3)."""
    return Change(
        symbol="urllib3.fields.format_header_param",
        kind="deprecated",
        version="2.0.0",
        sources=sources,
        replacement="urllib3.fields.format_multipart_header_param",
    )


def timeout(constraints: tuple[Constraint, ...]) -> Parameter:
    return Parameter(
        "timeout",
        "positional_or_keyword",
        False,
        (SIGNATURE,),
        type="float | None",
        default="None",
        constraints=constraints,
    )


RANGE = Constraint("range", (SIGNATURE,), minimum="0")
UNIT = Constraint("unit", (SIGNATURE,), unit="seconds")


def test_objects_are_frozen_and_hashable() -> None:
    symbol = format_header_param()
    with pytest.raises(dataclasses.FrozenInstanceError):
        symbol.path = "other"  # type: ignore[misc]
    assert hash(symbol) == hash(format_header_param())
    assert symbol == format_header_param()


def test_inventory_serializes_canonically() -> None:
    sleep = Symbol(
        "urllib3.util.Retry.sleep",
        "method",
        (SIGNATURE,),
        (Signature((timeout((RANGE, UNIT)),), (SIGNATURE,)),),
    )
    inventory = Inventory((sleep, format_header_param()), (renamed((SIGNATURE, CHANGELOG)),))
    data = orjson.loads(canonical_json(inventory))
    assert [s["path"] for s in data["symbols"]] == [
        "urllib3.fields.format_header_param",
        "urllib3.util.Retry.sleep",
    ]
    constraints = data["symbols"][1]["signatures"][0]["parameters"][0]["constraints"]
    assert constraints[0]["sources"] == [
        {"type": "signature", "section_id": "s" * 16, "pointer": None}
    ]
    assert {c["kind"]: c["minimum"] or c["unit"] for c in constraints} == {
        "range": "0",
        "unit": "seconds",
    }
    change = data["changes"][0]
    assert (change["kind"], change["replacement"], change["removal_planned"]) == (
        "deprecated",
        "urllib3.fields.format_multipart_header_param",
        None,
    )


def test_merge_order_does_not_change_the_hash() -> None:
    a = Inventory(
        (format_header_param((SIGNATURE, EXAMPLE)),),
        (renamed((SIGNATURE, CHANGELOG)), renamed((CHANGELOG,))),
    )
    b = Inventory(
        (format_header_param((EXAMPLE, SIGNATURE, EXAMPLE)),),
        (renamed((CHANGELOG,)), renamed((CHANGELOG, SIGNATURE))),
    )
    assert a == b
    assert content_hash(a) == content_hash(b)
    assert timeout((UNIT, RANGE)) == timeout((RANGE, UNIT))
    # highest merge priority first: sources[0] wins
    assert renamed((CHANGELOG, EXAMPLE, SPEC, SIGNATURE)).sources == (
        SPEC,
        SIGNATURE,
        EXAMPLE,
        CHANGELOG,
    )


def test_values_are_kept_as_written() -> None:
    # parsed numbers would be equal (0 == 0.0, 1 == True) but serialize differently
    zero, zero_float = (Constraint("range", (SIGNATURE,), minimum=m) for m in ("0", "0.0"))
    assert zero != zero_float
    assert len({Constraint("enum", (SIGNATURE,), values=(v,)) for v in ("1", "True")}) == 2


def test_confidence_follows_from_the_source_type() -> None:
    assert [s.confidence for s in (SPEC, SIGNATURE, EXAMPLE, CHANGELOG)] == [
        "high",
        "high",
        "medium",
        "low",
    ]
    with pytest.raises(TypeError):
        Source("changelog", confidence="high")  # type: ignore[call-arg]


def test_source_needs_a_location() -> None:
    with pytest.raises(ValueError, match="needs a section_id"):
        Source("changelog")
    with pytest.raises(ValueError, match="needs a section_id"):
        Source("signature", pointer="/x")
    with pytest.raises(ValueError, match="needs a section_id"):
        Source("spec")


def test_parameter_rejects_contradictions() -> None:
    with pytest.raises(ValueError, match="required, but has default"):
        Parameter("x", "positional_or_keyword", True, (SIGNATURE,), default="None")
    with pytest.raises(ValueError, match="never required"):
        Parameter("kwargs", "var_keyword", True, (SIGNATURE,))
    with pytest.raises(ValueError, match="never required"):
        Parameter("args", "var_positional", False, (SIGNATURE,), default="()")


def test_removed_symbol_has_changes_but_no_symbol() -> None:
    gone = Change("urllib3.contrib.securetransport", "removed", "2.0.0", (CHANGELOG,))
    inventory = Inventory((format_header_param(),), (gone,))
    assert gone.symbol not in {s.path for s in inventory.symbols}
    assert inventory.changes == (gone,)


def test_inventory_rejects_duplicate_symbols() -> None:
    with pytest.raises(ValueError, match="duplicate symbol paths"):
        Inventory((format_header_param(), format_header_param((CHANGELOG,))))
