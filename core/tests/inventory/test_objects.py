import dataclasses

import orjson
import pytest

from notinspec.adapters.canonical import canonical_json
from notinspec.inventory import (
    SOURCE_CONFIDENCE,
    Change,
    Constraint,
    Inventory,
    Parameter,
    ReturnType,
    Signature,
    Source,
    Symbol,
)

SIGNATURE = Source("signature", SOURCE_CONFIDENCE["signature"], section_id="s" * 16)
CHANGELOG = Source("changelog", SOURCE_CONFIDENCE["changelog"], section_id="c" * 16)


def format_header_param() -> Symbol:
    """urllib3 2.0.0: deprecated, renamed; mentioned by a directive and the changelog (§6.3)."""
    change = Change(
        symbol="urllib3.fields.format_header_param",
        kind="deprecated",
        version="2.0.0",
        sources=(SIGNATURE, CHANGELOG),
        replacement="urllib3.fields.format_multipart_header_param",
    )
    params = (
        Parameter("name", "positional_or_keyword", True, (SIGNATURE,), type="str"),
        Parameter("value", "positional_or_keyword", True, (SIGNATURE,), type="str | bytes"),
    )
    signature = Signature(
        params,
        (SIGNATURE,),
        text="format_header_param(name, value)",
        returns=ReturnType("str", (SIGNATURE,)),
    )
    return Symbol(
        "urllib3.fields.format_header_param",
        "function",
        (SIGNATURE,),
        signatures=(signature,),
        changes=(change,),
    )


def test_objects_are_frozen_and_hashable() -> None:
    symbol = format_header_param()
    with pytest.raises(dataclasses.FrozenInstanceError):
        symbol.path = "other"  # type: ignore[misc]
    assert hash(symbol) == hash(format_header_param())
    assert symbol == format_header_param()


def test_inventory_serializes_canonically() -> None:
    timeout = Parameter(
        "timeout",
        "positional_or_keyword",
        False,
        (SIGNATURE,),
        type="float | None",
        default="None",
        constraints=(
            Constraint("range", (SIGNATURE,), minimum=0),
            Constraint("unit", (SIGNATURE,), unit="seconds"),
        ),
    )
    inventory = Inventory((format_header_param(),))
    data = orjson.loads(canonical_json(inventory))
    change = data["symbols"][0]["changes"][0]
    assert change["kind"] == "deprecated"
    assert change["replacement"] == "urllib3.fields.format_multipart_header_param"
    assert change["removal_planned"] is None
    assert [s["type"] for s in change["sources"]] == ["signature", "changelog"]
    assert canonical_json(inventory) == canonical_json(Inventory((format_header_param(),)))
    assert orjson.loads(canonical_json(timeout))["constraints"][1]["unit"] == "seconds"


def test_every_source_type_has_a_confidence() -> None:
    assert SOURCE_CONFIDENCE == {
        "spec": "high",
        "signature": "high",
        "example": "medium",
        "changelog": "low",
    }
