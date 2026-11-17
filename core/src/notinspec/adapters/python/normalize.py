"""Raw call records → `CallRecord`s, using the inventory (SPEC §4, §6.2 component C, §6.10 L3).

The same code normalizes the calls of a docs example and of a model's answer, so both end up
in the same shape: inventory symbol + named arguments.

**Callee → `Symbol.path`**, by what the raw record's callee is:

- an import path (`urllib3.PoolManager`, `urllib3.util.Timeout`): that path if the inventory has
  it (`exact`), else the one top-level symbol of the same package with the same name (`alias`:
  `urllib3.Retry` is documented as `urllib3.util.Retry`). A path through a class
  (`urllib3.Timeout.from_float`) resolves the class first, then the member.
- a variable holding a call result (`http.request`): the member of the result's type
  (`variable`). The type of a call result is the class itself for a class or exception, else
  the documented `ReturnType` (`BaseHTTPResponse`, `float | None`, `Self`), resolved like an
  alias. Only one attribute deep: `resp.data.decode` has no known type.
- a name the example never binds: a package name works as an import (`urllib3.PoolManager`
  in a snippet without `import urllib3`), a symbol's own name as an alias (`Retry(…)` in a
  docstring) (`name`). Other variables (`http` in a snippet that starts mid-way) stay unknown.

Anything else is an `UnresolvedCall` with a reason; it is never guessed. `print`, `open` and
other packages' calls are `not-in-inventory`.

**Arguments → `Parameter`s**, the way Python binds them: positional arguments fill the
positional parameters in order, then `*args`; keywords go to their parameter, else to
`**kwargs`. Of several signatures, the first that binds cleanly is used. What does not bind
(unknown keyword, too many positional arguments, a missing required parameter, `*xs` / `**kw`
that cannot be mapped) is an `issue` on the record: input for K1, and `hallucinated-api` /
`wrong-arguments` in L3. The record is kept with what did bind.

**Inventory additions** (SPEC §6.3, `example_additions`): a call into the project's own
packages whose symbol the inventory does not have becomes a `Symbol` with an example
`Source`; keyword arguments become its parameters. A symbol with a documented signature never
gets parameters from an example: an unknown keyword there is an issue, not a new parameter.
"""

import re
from collections import defaultdict
from collections.abc import Callable, Iterable, Sequence
from dataclasses import dataclass
from typing import Literal

from notinspec.adapters.python.calls import RawCallRecord, Value
from notinspec.inventory import Inventory, Parameter, Signature, Source, Symbol

CLASS_KINDS = frozenset({"class", "exception"})
_POSITIONAL = ("positional_only", "positional_or_keyword")
_BY_KEYWORD = ("positional_or_keyword", "keyword_only")

type ResolvedBy = Literal["exact", "alias", "variable", "name"]
type IssueKind = Literal[
    "unknown-parameter",  # keyword with no parameter and no **kwargs
    "too-many-positional",  # positional argument with no slot and no *args
    "multiple-values",  # the same parameter given twice
    "missing-required",
    "unpacked",  # `*xs` / `**kw`: what it binds is unknown
]
type UnresolvedReason = Literal[
    "not-in-inventory",  # the path is known, the inventory has no such symbol
    "ambiguous",  # several symbols could be meant
    "unknown-type",  # the callee is an attribute of a value whose type is unknown
]


@dataclass(frozen=True)
class Argument:
    name: str  # keyword as written; for a positional argument, its parameter's name
    parameter: str | None  # inventory parameter ("connection_pool_kw" for an extra keyword)
    values: tuple[Value, ...]  # one, except for a `*args` parameter


@dataclass(frozen=True)
class CallIssue:
    kind: IssueKind
    detail: str  # parameter or keyword name, or the argument as written


@dataclass(frozen=True)
class CallRecord:
    """A normalized call: inventory symbol + named arguments."""

    index: int  # the raw record's index: `Value.call` points to these
    line: int
    end_line: int
    symbol: str  # `Symbol.path`
    resolved_by: ResolvedBy
    signature: int | None  # index into `Symbol.signatures`; None = no documented signature
    args: tuple[Argument, ...]  # in signature order; extra keywords at `**kwargs`, by name
    unmapped: tuple[Value, ...]  # positional arguments with no parameter to go to
    issues: tuple[CallIssue, ...]


@dataclass(frozen=True)
class UnresolvedCall:
    index: int
    line: int
    symbol: str  # as written
    reason: UnresolvedReason
    path: str | None  # what was looked up ("urllib3.HTTPHeaderDict"), when known
    candidates: tuple[str, ...] = ()  # ambiguous only


@dataclass(frozen=True)
class NormalizedCalls:
    calls: tuple[CallRecord, ...]
    unresolved: tuple[UnresolvedCall, ...]


@dataclass(frozen=True)
class Lookup:
    """Result of `ApiIndex.resolve`."""

    path: str | None  # the inventory symbol, or None
    how: ResolvedBy | None = None  # exact | alias
    wanted: str | None = None  # not found: the canonical path it would have
    candidates: tuple[str, ...] = ()  # ambiguous alias


class ApiIndex:
    """Lookups over one inventory. Build once, reuse for every example and answer."""

    def __init__(self, inventory: Inventory) -> None:
        self.symbols = {s.path: s for s in inventory.symbols}
        self.packages = frozenset(path.split(".")[0] for path in self.symbols)
        self._by_name: dict[tuple[str, str], list[str]] = defaultdict(list)
        for path in self.symbols:
            if not self.is_member(path):
                top, _, rest = path.partition(".")
                self._by_name[(top, rest.rsplit(".", 1)[-1] or top)].append(path)

    def resolve(self, path: str) -> Lookup:
        """The symbol a dotted path (as imported) means. A path through a class is a member."""
        if path in self.symbols:
            return Lookup(path, "exact")
        parts = path.split(".")
        for cut in range(len(parts) - 1, 0, -1):
            owner = self._top_level(".".join(parts[:cut]))
            if owner.path is not None and self.is_class(owner.path):
                member = ".".join([owner.path, *parts[cut:]])
                if member in self.symbols:
                    return Lookup(member, owner.how)
                return Lookup(None, wanted=member)
        return self._top_level(path)

    def result_type(self, symbol: Symbol, signature: Signature | None) -> str | None:
        """Class path of what calling `symbol` returns, if the docs say and it is ours."""
        if symbol.kind in CLASS_KINDS:
            return symbol.path
        returns = signature.returns if signature is not None else None
        if returns is None:
            returns = next((s.returns for s in symbol.signatures if s.returns), None)
        if returns is None:
            return None
        names = [t for t in re.split(r"\s*(?:\||,|\bor\b)\s*", returns.type.strip()) if t]
        names = [n for n in names if n != "None"]
        if len(names) != 1:
            return None
        name = names[0].strip("`")
        if name == "Self":
            owner = symbol.path.rsplit(".", 1)[0]
            return owner if self.is_class(owner) else None
        if "." not in name:  # a bare class name: in the symbol's own package
            name = f"{symbol.path.split('.')[0]}.{name}"
        path = self.resolve(name).path
        return path if path is not None and self.is_class(path) else None

    def _top_level(self, path: str) -> Lookup:
        """Exact path, or the one non-member symbol of the same package with the same name."""
        if path in self.symbols:
            return Lookup(path, "exact")
        top, _, rest = path.partition(".")
        found = self._by_name.get((top, rest.rsplit(".", 1)[-1]), []) if rest else []
        if len(found) == 1:
            return Lookup(found[0], "alias")
        return Lookup(None, wanted=path, candidates=tuple(sorted(found)))

    def is_class(self, path: str) -> bool:
        symbol = self.symbols.get(path)
        return symbol is not None and symbol.kind in CLASS_KINDS

    def is_member(self, path: str) -> bool:
        return self.is_class(path.rsplit(".", 1)[0]) if "." in path else False


def normalize_calls(raw: Sequence[RawCallRecord], api: ApiIndex) -> NormalizedCalls:
    """Raw call records of one piece of code → call records. Pure: same input ⇒ equal output."""
    types: dict[int, str | None] = {}
    calls: list[CallRecord] = []
    unresolved: list[UnresolvedCall] = []
    for record in raw:
        target = _callee(record, api, types)
        if isinstance(target, UnresolvedCall):
            unresolved.append(target)
            types[record.index] = None
            continue
        path, how = target
        symbol = api.symbols[path]
        normalized, signature = _bind(record, symbol, how)
        calls.append(normalized)
        types[record.index] = api.result_type(symbol, signature)
    return NormalizedCalls(tuple(calls), tuple(unresolved))


def example_additions(
    raw: Sequence[RawCallRecord], normalized: NormalizedCalls, api: ApiIndex, section_id: str
) -> tuple[Symbol, ...]:
    """Symbols of the project's packages that the example calls but the inventory lacks."""
    source = Source("example", section_id=section_id)
    by_index = {r.index: r for r in raw}
    keywords: dict[str, dict[str, None]] = {}
    for call in normalized.unresolved:
        if call.reason != "not-in-inventory" or call.path is None:
            continue
        if call.path.split(".")[0] not in api.packages:
            continue
        names = keywords.setdefault(call.path, {})
        for keyword in by_index[call.index].kwargs:
            if keyword.name is not None:
                names[keyword.name] = None
    return tuple(
        Symbol(
            path,
            _guess_kind(path, api),
            (source,),
            (_example_signature(names, source),),
        )
        for path, names in sorted(keywords.items())
    )


def _guess_kind(path: str, api: ApiIndex) -> str:
    """PEP 8 naming: a member of a class is a method, CapWords a class, else a function."""
    if api.is_member(path):
        return "method"
    return "class" if path.rsplit(".", 1)[-1][:1].isupper() else "function"


def _example_signature(names: Iterable[str], source: Source) -> Signature:
    parameters = tuple(
        Parameter(name, "positional_or_keyword", False, (source,)) for name in sorted(names)
    )
    return Signature(parameters, (source,))


type _Target = tuple[str, ResolvedBy] | UnresolvedCall
type _Missing = Callable[[UnresolvedReason, str | None, Iterable[str]], UnresolvedCall]


def _callee(record: RawCallRecord, api: ApiIndex, types: dict[int, str | None]) -> _Target:
    callee = record.callee

    def missing(
        reason: UnresolvedReason, path: str | None, found: Iterable[str] = ()
    ) -> UnresolvedCall:
        return UnresolvedCall(record.index, record.line, record.symbol, reason, path, tuple(found))

    def lookup(path: str, how: ResolvedBy | None = None) -> _Target:
        found = api.resolve(path)
        if found.path is None:
            reason: UnresolvedReason = "ambiguous" if found.candidates else "not-in-inventory"
            return missing(reason, found.wanted, found.candidates)
        assert found.how is not None
        return found.path, how or found.how

    if callee.kind == "import" and callee.path is not None:
        return lookup(callee.path)
    if callee.kind == "call" and callee.call is not None:
        owner = types.get(callee.call)
        if owner is None or len(callee.attrs) != 1:
            return missing("unknown-type", None, ())
        member = f"{owner}.{callee.attrs[0]}"
        if member not in api.symbols:
            return missing("not-in-inventory", member, ())
        return member, "variable"
    if callee.kind == "name" and callee.name is not None:
        if callee.name in api.packages:
            return lookup(".".join((callee.name, *callee.attrs)), "name")
        return _short_name(record, api, missing)
    return missing("unknown-type", None, ())


def _short_name(record: RawCallRecord, api: ApiIndex, missing: _Missing) -> _Target:
    """An unbound name used as a symbol's own name: `Retry(…)`, `Timeout.from_float(…)`.

    Only the first name is looked up, so an unbound variable (`http.request`) never matches a
    symbol by its last part.
    """
    callee = record.callee
    assert callee.name is not None
    found: set[str] = set()
    candidates: set[str] = set()
    for package in api.packages:
        lookup = api.resolve(f"{package}.{callee.name}")
        if lookup.path is not None:
            found.add(lookup.path)
        candidates.update(lookup.candidates)
    if len(found) > 1 or (not found and candidates):
        return missing("ambiguous", None, sorted(found | candidates))
    if not found:
        return missing("unknown-type" if callee.attrs else "not-in-inventory", None, ())
    (owner,) = found
    if not callee.attrs:
        return owner, "name"
    if not api.is_class(owner):
        return missing("unknown-type", None, ())
    member = ".".join((owner, *callee.attrs))
    if member not in api.symbols:
        return missing("not-in-inventory", member, ())
    return member, "name"


def _bind(
    record: RawCallRecord, symbol: Symbol, how: ResolvedBy
) -> tuple[CallRecord, Signature | None]:
    if not symbol.signatures:
        args, unmapped, issues = _bind_keywords_only(record)
        return _record(record, symbol, how, None, args, unmapped, issues), None
    attempts = [_bind_signature(record, signature) for signature in symbol.signatures]
    best = min(range(len(attempts)), key=lambda i: (len(attempts[i][2]), i))
    args, unmapped, issues = attempts[best]
    signature = symbol.signatures[best]
    return _record(record, symbol, how, best, args, unmapped, issues), signature


def _record(
    record: RawCallRecord,
    symbol: Symbol,
    how: ResolvedBy,
    signature: int | None,
    args: tuple[Argument, ...],
    unmapped: tuple[Value, ...],
    issues: tuple[CallIssue, ...],
) -> CallRecord:
    return CallRecord(
        index=record.index,
        line=record.line,
        end_line=record.end_line,
        symbol=symbol.path,
        resolved_by=how,
        signature=signature,
        args=args,
        unmapped=unmapped,
        issues=issues,
    )


type _Bound = tuple[tuple[Argument, ...], tuple[Value, ...], tuple[CallIssue, ...]]


def _bind_keywords_only(record: RawCallRecord) -> _Bound:
    """No documented signature: keywords keep their names, positional arguments stay unmapped."""
    args = tuple(Argument(k.name, None, (k.value,)) for k in record.kwargs if k.name is not None)
    issues = tuple(CallIssue("unpacked", k.value.source) for k in record.kwargs if k.name is None)
    return tuple(sorted(args, key=lambda a: a.name)), record.args, issues


def _bind_signature(record: RawCallRecord, signature: Signature) -> _Bound:
    parameters = signature.parameters
    slots = [p for p in parameters if p.kind in _POSITIONAL]
    var_positional = next((p for p in parameters if p.kind == "var_positional"), None)
    var_keyword = next((p for p in parameters if p.kind == "var_keyword"), None)
    bound: dict[str, list[Value]] = {}
    extra: dict[str, Value] = {}
    unmapped: list[Value] = []
    issues: list[CallIssue] = []
    unpacked = False

    for position, value in enumerate(record.args):
        if unpacked or value.kind == "unpack":
            if not unpacked:
                issues.append(CallIssue("unpacked", value.source))
            unpacked = True
            unmapped.append(value)
        elif position < len(slots):
            bound[slots[position].name] = [value]
        elif var_positional is not None:
            bound.setdefault(var_positional.name, []).append(value)
        else:
            issues.append(CallIssue("too-many-positional", value.source))
            unmapped.append(value)

    by_name = {p.name: p for p in parameters if p.kind in _BY_KEYWORD}
    for keyword in record.kwargs:
        if keyword.name is None:
            issues.append(CallIssue("unpacked", keyword.value.source))
            unpacked = True
        elif keyword.name in by_name:
            if keyword.name in bound:
                issues.append(CallIssue("multiple-values", keyword.name))
            else:
                bound[keyword.name] = [keyword.value]
        elif var_keyword is not None:
            if keyword.name in extra:
                issues.append(CallIssue("multiple-values", keyword.name))
            extra[keyword.name] = keyword.value
        else:
            issues.append(CallIssue("unknown-parameter", keyword.name))

    if not unpacked:
        issues += [
            CallIssue("missing-required", p.name)
            for p in parameters
            if p.required and p.name not in bound
        ]

    args: list[Argument] = []
    for parameter in parameters:
        if parameter.name in bound:
            args.append(Argument(parameter.name, parameter.name, tuple(bound[parameter.name])))
        elif parameter is var_keyword:
            args += [Argument(k, parameter.name, (extra[k],)) for k in sorted(extra)]
    return tuple(args), tuple(unmapped), tuple(issues)
