import os
from collections.abc import Callable, Mapping
from pathlib import Path
from typing import Any

import pytest
import yaml

from notinspec.adapters.canonical import canonical_json
from notinspec.inventory import (
    Inventory,
    Parameter,
    ParameterKind,
    ReturnType,
    Signature,
    Source,
    Symbol,
)


@pytest.fixture
def golden(request: pytest.FixtureRequest) -> Callable[[str, object], None]:
    """Compare an object with golden/<name>.json next to the test file.

    Run with UPDATE_GOLDEN=1 to rewrite the file. When output changes on purpose, regenerate the
    golden files in the same PR so the reviewer sees exactly what changed.
    """
    golden_dir = request.path.parent / "golden"

    def check(name: str, obj: object) -> None:
        path = golden_dir / f"{name}.json"
        actual = canonical_json(obj, pretty=True).decode()
        if os.environ.get("UPDATE_GOLDEN") == "1":
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(actual, encoding="utf-8")
            return
        if not path.exists():
            pytest.fail(f"missing golden file {path}; run with UPDATE_GOLDEN=1 to create it")
        assert actual == path.read_text(encoding="utf-8"), (
            f"output differs from {path.name}; if intended, rerun with UPDATE_GOLDEN=1"
        )

    return check


# Inventories for component C tests, until component B builds them from Sphinx `desc` nodes.
# Format: {path: {kind, params: ["a", "/", "b=1", "*args", "*", "c: int = 2", "**kw"], returns}};
# `signatures: [[...], [...]]` instead of `params` for several signatures.
INVENTORY_SOURCE = Source("signature", section_id="0" * 16)
URLLIB3_INVENTORY = Path(__file__).parent / "examples" / "fixtures" / "urllib3-inventory.yaml"


def _parameters(texts: list[str]) -> tuple[Parameter, ...]:
    parameters: list[Parameter] = []
    keyword_only = False
    for text in texts:
        if text == "/":
            parameters = [
                Parameter(p.name, "positional_only", p.required, p.sources, p.type, p.default)
                for p in parameters
            ]
            continue
        if text == "*":
            keyword_only = True
            continue
        head, eq, default = text.partition("=")
        name, _, annotation = head.partition(":")
        kind: ParameterKind = "keyword_only" if keyword_only else "positional_or_keyword"
        if name.startswith("**"):
            kind, name = "var_keyword", name[2:]
        elif name.startswith("*"):
            kind, name, keyword_only = "var_positional", name[1:], True
        parameters.append(
            Parameter(
                name.strip(),
                kind,
                required=not eq and kind not in ("var_positional", "var_keyword"),
                sources=(INVENTORY_SOURCE,),
                type=annotation.strip() or None,
                default=default.strip() if eq else None,
            )
        )
    return tuple(parameters)


def inventory_from(data: Mapping[str, Mapping[str, Any]]) -> Inventory:
    symbols = []
    for path, entry in data.items():
        returns = ReturnType(entry["returns"], (INVENTORY_SOURCE,)) if "returns" in entry else None
        lists = entry.get("signatures", [entry["params"]] if "params" in entry else [])
        signatures = tuple(
            Signature(_parameters(params), (INVENTORY_SOURCE,), None, returns) for params in lists
        )
        symbols.append(Symbol(path, entry["kind"], (INVENTORY_SOURCE,), signatures))
    return Inventory(tuple(symbols))


@pytest.fixture(scope="session")
def make_inventory() -> Callable[[Mapping[str, Mapping[str, Any]]], Inventory]:
    return inventory_from


@pytest.fixture(scope="session")
def urllib3_inventory() -> Inventory:
    return inventory_from(yaml.safe_load(URLLIB3_INVENTORY.read_text("utf-8")))
