"""Inventory objects: what exists in the API (SPEC §4, §6.3).

```
Inventory
 ├─ Symbol
 │   └─ 1:n  Signature
 │            ├─ 1:n  Parameter
 │            │        └─ 1:n  Constraint
 │            └─ 1:1  ReturnType
 └─ Change   – keyed on its own (old name), also for names that are no longer a Symbol
Source       – attached to every object above
```

Plain frozen dataclasses: builders (spec parser, Sphinx `desc` nodes, examples, *change*
claims) create them, merge combines them, and only `notinspec.db` maps them to tables.

Same input ⇒ same `canonical_json` / `content_hash`, so:

- values are kept **as written** (`str`): defaults, constraint values and bounds, versions.
  Numbers parsed by different builders would serialize differently (`0` vs `0.0`, `1` vs `True`).
- every tuple has a fixed order. Order that carries meaning (`Signature.parameters`, enum
  `Constraint.values`) is the documented order; every other tuple is sorted and de-duplicated
  in `__post_init__`, so the order in which sources are merged never matters.
- `__post_init__` rejects objects that contradict themselves.
"""

from collections.abc import Callable, Iterable
from dataclasses import dataclass
from typing import Any, Literal

from notinspec.adapters.canonical import canonical_json

# who wrote the fact (SPEC §6.3 table): A spec parser, B signature / version directive,
# C example normalization, D *change* claim
type SourceType = Literal["spec", "signature", "example", "changelog"]
type Confidence = Literal["high", "medium", "low"]

SOURCE_CONFIDENCE: dict[SourceType, Confidence] = {
    "spec": "high",
    "signature": "high",
    "example": "medium",
    "changelog": "low",  # → review by our team (SPEC §2.5)
}
# merge priority: spec > signature > example > changelog
SOURCE_PRIORITY: tuple[SourceType, ...] = ("spec", "signature", "example", "changelog")

# Python `inspect.Parameter.kind`, lower case; OpenAPI parameters and body fields are keyword-only
type ParameterKind = Literal[
    "positional_only",
    "positional_or_keyword",
    "var_positional",  # *args
    "keyword_only",
    "var_keyword",  # **kwargs
]
_VARIADIC: frozenset[ParameterKind] = frozenset({"var_positional", "var_keyword"})

# OpenAPI: `adapters.openapi.normalize.PARAMETER_LOCATIONS` + "body"
type ParameterLocation = Literal["path", "query", "header", "cookie", "body"]

type ConstraintKind = Literal["enum", "range", "unit", "format"]

# status of the name the change is about; a rename is `deprecated` or `removed` + `replacement`
type ChangeKind = Literal["added", "deprecated", "removed"]


@dataclass(frozen=True)
class Source:
    """Where a fact comes from. Confidence follows from the type, so it is never set by hand."""

    type: SourceType
    # `Chunk.section_id`: always the whole section, never one part (SPEC §6.1).
    # None only for a formal spec fact outside any chunk (then `pointer` is set).
    section_id: str | None = None
    pointer: str | None = None  # formal spec: JSON pointer ("/paths/~1orders/post")

    def __post_init__(self) -> None:
        if self.section_id is None and (self.type != "spec" or self.pointer is None):
            raise ValueError(f"{self.type} source needs a section_id")

    @property
    def confidence(self) -> Confidence:
        return SOURCE_CONFIDENCE[self.type]


@dataclass(frozen=True)
class Constraint:
    """A rule for a parameter value. Only the fields of its `kind` are set, all as written."""

    kind: ConstraintKind
    sources: tuple[Source, ...]
    values: tuple[str, ...] = ()  # enum: allowed values as written ("'GET'", "1"), documented order
    minimum: str | None = None  # range: inclusive unless `exclusive_*`
    maximum: str | None = None
    exclusive_minimum: bool = False
    exclusive_maximum: bool = False
    unit: str | None = None  # unit: "seconds", "bytes"
    format: str | None = None  # format: "date-time", "uri"

    def __post_init__(self) -> None:
        sort_sources(self)


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
    location: ParameterLocation | None = None  # OpenAPI only
    constraints: tuple[Constraint, ...] = ()  # sorted

    def __post_init__(self) -> None:
        if self.required and self.default is not None:
            raise ValueError(f"parameter {self.name}: required, but has default {self.default}")
        if self.kind in _VARIADIC and (self.required or self.default is not None):
            raise ValueError(f"parameter {self.name}: {self.kind} is never required or defaulted")
        sort_sources(self)
        _sort(self, "constraints", canonical_json)


@dataclass(frozen=True)
class ReturnType:
    """What a symbol returns; input of the composition operator."""

    type: str  # as documented: "HTTPResponse", "None"
    sources: tuple[Source, ...]

    def __post_init__(self) -> None:
        sort_sources(self)


@dataclass(frozen=True)
class Signature:
    """Header of a symbol, no body. A symbol can have several (overloads, versions)."""

    parameters: tuple[Parameter, ...]  # in signature order
    sources: tuple[Source, ...]
    text: str | None = None  # as documented: "sleep(response=None)"; for display
    returns: ReturnType | None = None  # None = not documented

    def __post_init__(self) -> None:
        sort_sources(self)


@dataclass(frozen=True)
class Change:
    """Addition, deprecation or removal of a symbol or parameter in a version.

    Key: `symbol` + `parameter` + `kind` + `version`, always with the **old** name. A deprecated
    name still exists and works; a removed one may have no `Symbol` at all. Versions are kept as
    written ("2.0") and compared as PEP 440 versions (`2.0 == 2.0.0`) when changes are merged.
    """

    symbol: str  # `Symbol.path` of the old name, whether or not it is in the inventory
    kind: ChangeKind
    version: str
    sources: tuple[Source, ...]
    parameter: str | None = None  # old parameter name; None = the change is about the symbol
    replacement: str | None = None  # symbol or parameter to use instead
    removal_planned: str | None = None  # version, as written

    def __post_init__(self) -> None:
        sort_sources(self)


@dataclass(frozen=True)
class Symbol:
    """Anything callable: function, method, class, endpoint, CLI command."""

    path: str  # fully qualified: "urllib3.util.Retry.sleep", "POST /orders"
    # Sphinx object type ("function", "method", "class", "exception", "decorator", ...);
    # "operation" for OpenAPI, "command" for CLI
    kind: str
    sources: tuple[Source, ...]
    signatures: tuple[Signature, ...] = ()  # sorted

    def __post_init__(self) -> None:
        sort_sources(self)
        _sort(self, "signatures", canonical_json)


@dataclass(frozen=True)
class Inventory:
    """Everything that exists in the API, for one input snapshot.

    `changes` are not under their `Symbol`: a removed name known only from the changelog has no
    symbol (what the docs do not describe does not exist, SPEC §1.1), but still has its changes.
    """

    symbols: tuple[Symbol, ...]  # sorted by path, one per path
    changes: tuple[Change, ...] = ()  # sorted by key

    def __post_init__(self) -> None:
        _sort(self, "symbols", lambda s: s.path)
        _sort(self, "changes", _change_order)
        paths = [s.path for s in self.symbols]
        if len(paths) != len(set(paths)):
            raise ValueError(
                f"duplicate symbol paths: {sorted({p for p in paths if paths.count(p) > 1})}"
            )


def _change_order(change: Change) -> tuple[str, str, str, str, bytes]:
    return (
        change.symbol,
        change.parameter or "",
        change.kind,
        change.version,
        canonical_json(change),
    )


def source_order(source: Source) -> tuple[int, str, str]:
    """Merge priority first, then location: the one order of sources (also used by `merge`)."""
    return (SOURCE_PRIORITY.index(source.type), source.section_id or "", source.pointer or "")


def sort_sources(obj: Any) -> None:
    """Highest merge priority first, so `sources[0]` is the source that wins."""
    _sort(obj, "sources", source_order)


def _sort(obj: Any, name: str, key: Callable[[Any], Any]) -> None:
    """Sort and de-duplicate a tuple field of a frozen dataclass, in place."""
    items: Iterable[Any] = getattr(obj, name)
    object.__setattr__(obj, name, tuple(sorted(set(items), key=key)))
