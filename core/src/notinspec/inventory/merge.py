"""Merge inventory objects from several sources (SPEC §6.3).

Priority **spec > signature > example > changelog**: of the objects that describe the same
thing, the one whose best source ranks highest wins and the others add their `Source`s.
Where both say something and it differs, the winner's value is kept and the difference is a
`Conflict` (later a `Finding`).

Identity:

- `Symbol`: path. Different kinds are a conflict.
- `Signature` of one symbol: its shape, the parameter names and kinds in order. Signatures of
  the same shape from different sources merge; their parameters by name. Different types,
  defaults, `required` or return types are conflicts. Signatures that share a source are
  never merged: they are overloads of one description (`ssl_wrap_socket` has two that differ
  only in types). Of several candidates, an identical signature is preferred.
- `Change`: symbol + parameter + kind + version, the version compared as a PEP 440 `Version`
  (`2.0 == 2.0.0`). The merged change keeps the winner's spelling of the version, and fills
  `replacement` / `removal_planned` from the best source that has them; two different
  values are a conflict.

Pure: same objects in any order ⇒ equal result.
"""

from collections import defaultdict
from collections.abc import Callable, Hashable, Iterable, Sequence
from dataclasses import dataclass, fields, is_dataclass, replace
from typing import Any

from packaging.version import InvalidVersion, Version

from notinspec.adapters.canonical import canonical_json
from notinspec.inventory.objects import (
    Change,
    Constraint,
    Inventory,
    Parameter,
    ReturnType,
    Signature,
    Source,
    Symbol,
    sort_sources,
    source_order,
)


@dataclass(frozen=True)
class Conflict:
    """Two sources say different things about the same object; `kept` is the winner's value."""

    subject: str  # "urllib3.util.Retry", "urllib3.util.Retry(total)", "<change key>"
    attribute: str  # "kind", "type", "default", "required", "returns", "replacement", ...
    kept: str | None
    other: str | None
    sources: tuple[Source, ...]  # of the object that lost

    def __post_init__(self) -> None:
        sort_sources(self)


def parse_version(value: str) -> Version | None:
    """PEP 440 version, or None when `value` is not one ("next", "unreleased")."""
    try:
        return Version(value)
    except InvalidVersion:
        return None


def change_key(change: Change) -> tuple[str, str, str, Version | str]:
    """Identity of a change; an invalid version compares as its text."""
    return (change.symbol, change.parameter or "", change.kind, _version_or_text(change.version))


def merge(parts: Iterable[Inventory]) -> tuple[Inventory, tuple[Conflict, ...]]:
    """One inventory from several, plus every disagreement between them."""
    parts = list(parts)
    conflicts: list[Conflict] = []
    symbols = _group((s for p in parts for s in p.symbols), lambda s: s.path)
    changes = _group((c for p in parts for c in p.changes), change_key)
    inventory = Inventory(
        tuple(_symbol(group, conflicts) for group in symbols),
        tuple(_change(group, conflicts) for group in changes),
    )
    return inventory, tuple(sorted(set(conflicts), key=canonical_json))


# --- objects ---------------------------------------------------------------------------------


def _symbol(group: Sequence[Symbol], conflicts: list[Conflict]) -> Symbol:
    winner = group[0]
    for other in group[1:]:
        _differs(conflicts, winner.path, "kind", winner.kind, other.kind, other.sources)
    # 1. identical signatures (apart from sources) are one; 2. groups of the same shape from
    # different sources merge, best first, and their differences are conflicts
    identical = _group((s for symbol in group for s in symbol.signatures), _identity)
    merged: list[list[Signature]] = []
    for same in sorted(identical, key=lambda g: (source_order(_best(g[0])), canonical_json(g[0]))):
        target = _same_shape(same, merged)
        if target is None:
            merged.append(list(same))
        else:
            target.extend(same)
    signatures = tuple(_signature(g, winner.path, conflicts) for g in merged)
    return Symbol(winner.path, winner.kind, _sources(group), signatures)


def _same_shape(group: list[Signature], merged: list[list[Signature]]) -> list[Signature] | None:
    """The merged group that `group` joins: same shape and no shared source. Signatures that
    share a source are overloads of one description, never one signature."""
    sources = {s for o in group for s in o.sources}
    return next(
        (
            m
            for m in merged
            if _shape(m[0]) == _shape(group[0]) and not sources & {s for o in m for s in o.sources}
        ),
        None,
    )


def _signature(group: Sequence[Signature], path: str, conflicts: list[Conflict]) -> Signature:
    winner = group[0]
    parameters = tuple(
        _parameter([s.parameters[i] for s in group], f"{path}({p.name})", conflicts)
        for i, p in enumerate(winner.parameters)  # same shape: same names at the same places
    )
    return Signature(
        parameters,
        _sources(group),
        text=winner.text,
        returns=_return_type([s.returns for s in group if s.returns], path, conflicts),
    )


def _parameter(group: Sequence[Parameter], subject: str, conflicts: list[Conflict]) -> Parameter:
    winner = group[0]  # in the order of the signatures: best source first
    type_ = _first(p.type for p in group)
    for other in group[1:]:
        _differs(conflicts, subject, "required", winner.required, other.required, other.sources)
        if winner.default is not None and other.default is not None:
            _differs(conflicts, subject, "default", winner.default, other.default, other.sources)
        if other.type is not None:
            _differs(conflicts, subject, "type", type_, other.type, other.sources)
    constraints = _group((c for p in group for c in p.constraints), _identity)
    return Parameter(
        winner.name,
        winner.kind,
        winner.required,
        _sources(group),
        type=type_,
        default=winner.default,
        location=_first(p.location for p in group),
        constraints=tuple(_constraint(g) for g in constraints),
    )


def _constraint(group: Sequence[Constraint]) -> Constraint:
    return replace(group[0], sources=_sources(group))


def _return_type(
    group: Sequence[ReturnType], path: str, conflicts: list[Conflict]
) -> ReturnType | None:
    if not group:
        return None
    kept = group[0].type
    for other in group[1:]:
        _differs(conflicts, path, "returns", kept, other.type, other.sources)
    return ReturnType(kept, _sources(r for r in group if r.type == kept))


def _change(group: Sequence[Change], conflicts: list[Conflict]) -> Change:
    winner = group[0]
    subject = _change_subject(winner)
    replacement = _first(c.replacement for c in group)
    removal = _first(c.removal_planned for c in group)
    for other in group:
        if other.replacement is not None and other.replacement != replacement:
            conflicts.append(
                Conflict(subject, "replacement", replacement, other.replacement, other.sources)
            )
        if other.removal_planned is not None and removal is not None:
            if _version_or_text(other.removal_planned) != _version_or_text(removal):
                conflicts.append(
                    Conflict(
                        subject, "removal_planned", removal, other.removal_planned, other.sources
                    )
                )
    return Change(
        winner.symbol,
        winner.kind,
        winner.version,
        _sources(group),
        parameter=winner.parameter,
        replacement=replacement,
        removal_planned=removal,
    )


def _version_or_text(value: str) -> Version | str:
    return parse_version(value) or value


def _change_subject(change: Change) -> str:
    target = f"{change.symbol}({change.parameter})" if change.parameter else change.symbol
    return f"{target} {change.kind} {change.version}"


# --- helpers ---------------------------------------------------------------------------------


def _group[T](items: Iterable[T], key: Callable[[T], Hashable]) -> list[list[T]]:
    """Groups of equal key, each ranked best first, in order of first appearance. Use it only
    where the result is sorted again (symbols, changes, constraints), never for ordered
    tuples such as `Signature.parameters`."""
    groups: dict[Hashable, list[T]] = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    return [_ranked(g) for g in groups.values()]


def _ranked[T](items: Iterable[T]) -> list[T]:
    """Best source first; ties broken by content, so input order never matters."""
    return sorted(items, key=lambda o: (source_order(_best(o)), canonical_json(o)))


def _best(obj: Any) -> Source:
    best: Source = obj.sources[0]  # sources are sorted best first
    return best


def _sources(group: Iterable[Any]) -> tuple[Source, ...]:
    return tuple({s for obj in group for s in obj.sources})


def _first[T](values: Iterable[T | None]) -> T | None:
    return next((v for v in values if v is not None), None)


def _differs(
    conflicts: list[Conflict],
    subject: str,
    attribute: str,
    kept: object,
    other: object,
    sources: tuple[Source, ...],
) -> None:
    if kept != other:
        conflicts.append(Conflict(subject, attribute, _text(kept), _text(other), sources))


def _text(value: object) -> str | None:
    return None if value is None else str(value)


def _identity(obj: Any) -> bytes:
    """Canonical JSON of an object without any of its `sources`, at every level."""
    return canonical_json(_plain(obj))


def _plain(value: Any) -> Any:
    if is_dataclass(value) and not isinstance(value, type):
        return {
            f.name: _plain(getattr(value, f.name)) for f in fields(value) if f.name != "sources"
        }
    if isinstance(value, tuple):
        return [_plain(v) for v in value]
    return value


def _shape(signature: Signature) -> tuple[tuple[str, str], ...]:
    return tuple((p.name, p.kind) for p in signature.parameters)
