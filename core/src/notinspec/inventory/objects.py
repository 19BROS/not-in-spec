"""Inventory objects: what exists in the API (SPEC §4, §6.3).

```
Symbol
 ├─ 1:n  Signature
 │        ├─ 1:n  Parameter
 │        │        └─ 1:n  Constraint
 │        └─ 1:1  ReturnType
 └─ 1:n  Change
Source  – attached to every object above
```

Plain frozen dataclasses, no logic: builders (spec parser, Sphinx `desc` nodes, examples,
*change* claims) create them, merge combines them, and only `notinspec.db` maps them to tables.
Collections are tuples, so objects hash and serialize with `canonical_json`.
"""

from dataclasses import dataclass
from typing import Literal

# who wrote the fact (SPEC §6.3 table): A spec parser, B signature / version directive,
# C example normalization, D *change* claim. Merge priority: spec > signature > example > changelog
type SourceType = Literal["spec", "signature", "example", "changelog"]
type Confidence = Literal["high", "medium", "low"]

SOURCE_CONFIDENCE: dict[SourceType, Confidence] = {
    "spec": "high",
    "signature": "high",
    "example": "medium",
    "changelog": "low",  # → review by our team (SPEC §2.5)
}

# Python `inspect.Parameter.kind`, lower case; OpenAPI parameters and body fields are keyword-only
type ParameterKind = Literal[
    "positional_only",
    "positional_or_keyword",
    "var_positional",  # *args
    "keyword_only",
    "var_keyword",  # **kwargs
]

type ConstraintKind = Literal["enum", "range", "unit", "format"]

# status of the name the change is about; a rename is `deprecated` or `removed` + `replacement`
type ChangeKind = Literal["added", "deprecated", "removed"]

type Scalar = str | int | float | bool | None


@dataclass(frozen=True)
class Source:
    """Where a fact comes from and with what confidence."""

    type: SourceType
    confidence: Confidence
    # `Chunk.section_id`: always the whole section, never one part (SPEC §6.1).
    # None only for facts read from a formal spec outside any chunk.
    section_id: str | None = None
    pointer: str | None = None  # formal spec: JSON pointer ("/paths/~1orders/post")


@dataclass(frozen=True)
class Constraint:
    """A rule for a parameter value. Only the fields of its `kind` are set."""

    kind: ConstraintKind
    sources: tuple[Source, ...]
    values: tuple[Scalar, ...] = ()  # enum: allowed values in documented order
    minimum: float | None = None  # range: inclusive unless `exclusive_*`
    maximum: float | None = None
    exclusive_minimum: bool = False
    exclusive_maximum: bool = False
    unit: str | None = None  # unit: "seconds", "bytes"
    format: str | None = None  # format: "date-time", "uri"


@dataclass(frozen=True)
class Parameter:
    """One input of a signature."""

    name: str  # without `*` / `**`: "kwargs"
    kind: ParameterKind
    required: bool
    sources: tuple[Source, ...]
    type: str | None = None  # as documented: "float | None"; None = not documented
    # as written: "None", "3", "'GET'". None = no default (not the Python value None)
    default: str | None = None
    location: str | None = None  # OpenAPI only: path | query | header | cookie | body
    constraints: tuple[Constraint, ...] = ()


@dataclass(frozen=True)
class ReturnType:
    """What a symbol returns; input of the composition operator."""

    type: str  # as documented: "HTTPResponse", "None"
    sources: tuple[Source, ...]


@dataclass(frozen=True)
class Signature:
    """Header of a symbol, no body. A symbol can have several (overloads, versions)."""

    parameters: tuple[Parameter, ...]  # in signature order
    sources: tuple[Source, ...]
    text: str | None = None  # as documented: "sleep(response=None)"; for display
    returns: ReturnType | None = None  # None = not documented


@dataclass(frozen=True)
class Change:
    """Addition, deprecation or removal of a symbol or parameter in a version.

    Key: `symbol` + `parameter` + `kind` + `version`, always with the **old** name. A deprecated
    name still exists and works. Versions are kept as written ("2.0") and compared as PEP 440
    versions (`2.0 == 2.0.0`) when changes are merged.
    """

    symbol: str  # `Symbol.path` of the old name
    kind: ChangeKind
    version: str
    sources: tuple[Source, ...]
    parameter: str | None = None  # old parameter name; None = the change is about the symbol
    replacement: str | None = None  # symbol or parameter to use instead
    removal_planned: str | None = None  # version, as written


@dataclass(frozen=True)
class Symbol:
    """Anything callable: function, method, class, endpoint, CLI command."""

    path: str  # fully qualified: "urllib3.util.Retry.sleep", "POST /orders"
    # Sphinx object type ("function", "method", "class", "exception", "decorator", ...);
    # "operation" for OpenAPI, "command" for CLI
    kind: str
    sources: tuple[Source, ...]
    signatures: tuple[Signature, ...] = ()
    changes: tuple[Change, ...] = ()


@dataclass(frozen=True)
class Inventory:
    """Everything that exists in the API, for one input snapshot."""

    symbols: tuple[Symbol, ...]  # sorted by path
