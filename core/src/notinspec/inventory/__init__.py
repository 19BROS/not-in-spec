"""Inventory: what exists in the API, each fact with its `Source` (SPEC §6.3).

`objects.py` holds the dataclasses, `build.py` builds them from API reference blocks
(component B), `merge.py` merges objects from several sources (PEP 440 versions). Pipeline code
works on the dataclasses; only `notinspec.db` maps them to tables (SPEC §18).
"""

from notinspec.inventory.build import INVENTORY_BUILDER_VERSION, InventoryBuild, build_inventory
from notinspec.inventory.merge import Conflict, change_key, merge, parse_version
from notinspec.inventory.objects import (
    SOURCE_CONFIDENCE,
    SOURCE_PRIORITY,
    Change,
    ChangeKind,
    Confidence,
    Constraint,
    ConstraintKind,
    Inventory,
    Parameter,
    ParameterKind,
    ParameterLocation,
    ReturnType,
    Signature,
    Source,
    SourceType,
    Symbol,
)

__all__ = [
    "INVENTORY_BUILDER_VERSION",
    "SOURCE_CONFIDENCE",
    "SOURCE_PRIORITY",
    "Change",
    "ChangeKind",
    "Confidence",
    "Conflict",
    "Constraint",
    "ConstraintKind",
    "Inventory",
    "InventoryBuild",
    "Parameter",
    "ParameterKind",
    "ParameterLocation",
    "ReturnType",
    "Signature",
    "Source",
    "SourceType",
    "Symbol",
    "build_inventory",
    "change_key",
    "merge",
    "parse_version",
]
