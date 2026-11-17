"""Merge inventory objects from several sources (SPEC §6.3).

Priority **spec > signature > example > changelog**: of the objects that describe the same
thing, the one whose best source ranks highest wins and the others add their `Source`s.
Where both say something and it differs, the winner's value is kept and the difference is a
`Conflict` (later a `Finding`).

Identity:

- `Symbol`: path. Different kinds are a conflict.
- `Signature` of one symbol: everything but the sources (parameters with kinds, types,
  defaults, constraints; return type). Equal signatures merge into one with all sources;
  different ones are overloads (`ssl_wrap_socket` has two that differ only in types).
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
    SOURCE_PRIORITY,
    Change,
    Inventory,
    Source,
    Symbol,
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
        object.__setattr__(self, "sources", tuple(sorted(set(self.sources), key=_source_rank)))


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
    signatures = _group((s for sym in group for s in sym.signatures), _identity)
    return Symbol(winner.path, winner.kind, _sources(group), tuple(_union(g) for g in signatures))


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
    """Groups of equal key, each ranked best first. Group order does not matter: the
    dataclasses sort their tuples themselves."""
    groups: dict[Hashable, list[T]] = defaultdict(list)
    for item in items:
        groups[key(item)].append(item)
    return [_ranked(g) for g in groups.values()]


def _ranked[T](items: Iterable[T]) -> list[T]:
    """Best source first; ties broken by content, so input order never matters."""
    return sorted(items, key=lambda o: (_source_rank(_best(o)), canonical_json(o)))


def _best(obj: Any) -> Source:
    best: Source = obj.sources[0]  # sources are sorted best first
    return best


def _source_rank(source: Source) -> tuple[int, str, str]:
    return (SOURCE_PRIORITY.index(source.type), source.section_id or "", source.pointer or "")


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


def _union[T](group: Sequence[T]) -> T:
    """Objects equal apart from their sources → the first, with all sources at every level."""
    first: Any = group[0]
    changes: dict[str, Any] = {"sources": _sources(group)}
    for f in fields(first):
        value = getattr(first, f.name)
        if f.name == "sources" or value is None:
            continue
        if is_dataclass(value):
            changes[f.name] = _union([getattr(o, f.name) for o in group])
        elif isinstance(value, tuple) and value and is_dataclass(value[0]):
            items = _group((v for o in group for v in getattr(o, f.name)), _identity)
            changes[f.name] = tuple(_union(g) for g in items)
    merged: T = replace(first, **changes)
    return merged
