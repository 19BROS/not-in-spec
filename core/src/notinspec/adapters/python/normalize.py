"""Raw call records → `CallRecord`s, using the inventory (SPEC §4, §6.2 component C, §6.10 L3).

The same code normalizes the calls of a docs example and of a model's answer, so both end up
in the same shape: inventory symbol + named arguments.

**Callee → `Symbol.path`**, by what the raw record's callee is:

- an import path (`urllib3.PoolManager`, `urllib3.util.Timeout`): that path if the inventory has
  it (`exact`), else the one top-level symbol of the same package with the same name (`alias`:
  `urllib3.Retry` is documented as `urllib3.util.Retry`). A path through a class
  (`urllib3.Timeout.from_float`) resolves the class first, then the member.
  An alias is a re-export only when it is written in a module *above* the documented one
  (`urllib3.Retry` for `urllib3.util.Retry`). Any other module (`urllib3.exceptions.Timeout`,
  `urllib3.fake.PoolManager`, also the undocumented `urllib3.util.retry.Retry`) still names the
  symbol, but the record gets a `wrong-module` issue: the docs never say it can be imported
  from there, and in L3 that is a hallucinated API.
- a variable holding a call result (`http.request`): the member of the result's type
  (`variable`). The type of a call result is the class itself for a class or exception, else
  the `ReturnType` of the signature the call bound to (`BaseHTTPResponse`, `float | None`,
  `Self`), resolved like an alias. Never another overload's return type. Only one attribute
  deep: `resp.data.decode` has no known type.
- a name the example never binds: a package name works as an import (`urllib3.PoolManager`
  in a snippet without `import urllib3`), a symbol's own name as an alias (`Retry(…)` in a
  docstring) (`name`). Other variables (`http` in a snippet that starts mid-way) stay unknown.

Anything else is an `UnresolvedCall` with a reason; it is never guessed. `print`, `open` and
other packages' calls are `not-in-inventory`.

**Arguments → `Parameter`s**, the way Python binds them: positional arguments fill the
positional parameters in order, then `*args`; keywords go to their parameter, else to
`**kwargs`. Of several signatures, the one with the fewest issues is used (of equals, the
first in the inventory's order). What does not fit (unknown keyword, too many positional
arguments, a missing required parameter, `*xs` / `**kw` that cannot be mapped, calling an
attribute or property, an import from the wrong module) is an `issue` on the record: input for
K1, and `hallucinated-api` / `wrong-arguments` in L3. The record is kept with what did bind.

**Inventory additions** (SPEC §6.3, `example_additions`): what an example shows that the
inventory lacks, with an example `Source`:

- a called symbol of the project's own packages that the inventory does not have: a `Symbol`
  whose keyword arguments are its parameters;
- the keyword arguments of a symbol the inventory has without any signature.

A symbol with a documented signature never gets parameters from an example: an unknown keyword
there is an issue, not a new parameter. `merge_additions` combines the additions of all
examples into one `Symbol` per path (one example signature with every keyword seen), so the
inventory merge sees one example source per symbol instead of a fake overload per example.
"""

import re
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Literal

from notinspec.adapters.python.calls import RawCallRecord, Value
from notinspec.inventory import Inventory, Parameter, Signature, Source, Symbol

CLASS_KINDS = frozenset({"class", "exception"})
# Sphinx Python object types that can be called; attributes, properties and data cannot
CALLABLE_KINDS = CLASS_KINDS | {"function", "method", "classmethod", "staticmethod", "decorator"}
_POSITIONAL = ("positional_only", "positional_or_keyword")
_BY_KEYWORD = ("positional_or_keyword", "keyword_only")

type ResolvedBy = Literal["exact", "alias", "variable", "name"]
type IssueKind = Literal[
    "unknown-parameter",  # keyword with no parameter and no **kwargs
    "too-many-positional",  # positional argument with no slot and no *args
    "multiple-values",  # the same parameter given positionally and by keyword
    "missing-required",
    "unpacked",  # `*xs` / `**kw`: what it binds is unknown
    "not-callable",  # the symbol is an attribute, property or data (detail: its kind)
    "wrong-module",  # imported from a module the docs do not name (detail: the path written)
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
    detail: str  # parameter or keyword name, the argument as written, a kind or a path


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
    wrong_module: bool = False  # an alias written in a module that is not above the symbol's


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
                    return Lookup(member, owner.how, wrong_module=owner.wrong_module)
                return Lookup(None, wanted=member)
        return self._top_level(path)

    def result_type(self, symbol: Symbol, signature: Signature | None) -> str | None:
        """Class path of what calling `symbol` returns, if the docs say and it is ours."""
        if symbol.kind in CLASS_KINDS:
            return symbol.path
        if signature is None or signature.returns is None:
            return None
        names = [t for t in re.split(r"\s*(?:\||,|\bor\b)\s*", signature.returns.type) if t]
        names = [n.strip("` ") for n in names if n.strip("` ") != "None"]
        if len(names) != 1:
            return None
        name = names[0]
        if name == "Self":
            owner = symbol.path.rsplit(".", 1)[0]
            return owner if self.is_class(owner) else None
        if "." not in name:  # a bare class name: in the symbol's own package
            name = f"{symbol.path.split('.')[0]}.{name}"
        path = self.resolve(name).path
        return path if path is not None and self.is_class(path) else None

    def is_class(self, path: str) -> bool:
        symbol = self.symbols.get(path)
        return symbol is not None and symbol.kind in CLASS_KINDS

    def is_member(self, path: str) -> bool:
        return self.is_class(path.rsplit(".", 1)[0]) if "." in path else False

    def _top_level(self, path: str) -> Lookup:
        """Exact path, or the one non-member symbol of the same package with the same name."""
        if path in self.symbols:
            return Lookup(path, "exact")
        top, _, rest = path.partition(".")
        found = self._by_name.get((top, rest.rsplit(".", 1)[-1]), []) if rest else []
        if len(found) == 1:
            return Lookup(found[0], "alias", wrong_module=not _reexported(path, found[0]))
        return Lookup(None, wanted=path, candidates=tuple(sorted(found)))


def _reexported(written: str, documented: str) -> bool:
    """`urllib3.Retry` for `urllib3.util.Retry`: written in the same module or one above it."""
    module = written.rsplit(".", 1)[0]
    home = documented.rsplit(".", 1)[0]
    return home == module or home.startswith(module + ".")


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
        symbol = api.symbols[target.path]
        normalized, signature = _bind(record, symbol, target)
        calls.append(normalized)
        types[record.index] = api.result_type(symbol, signature)
    return NormalizedCalls(tuple(calls), tuple(unresolved))


def example_additions(
    raw: Sequence[RawCallRecord], normalized: NormalizedCalls, api: ApiIndex, section_id: str
) -> tuple[Symbol, ...]:
    """What one example adds to the inventory (module docstring), sorted by path."""
    by_index = {r.index: r for r in raw}
    keywords: dict[str, dict[str, None]] = {}
    for call in normalized.unresolved:
        if call.reason != "not-in-inventory" or call.path is None:
            continue
        if call.path.split(".")[0] not in api.packages:
            continue
        names = keywords.setdefault(call.path, {})
        names.update((k.name, None) for k in by_index[call.index].kwargs if k.name is not None)
    for record in normalized.calls:
        if record.signature is None and record.args:
            keywords.setdefault(record.symbol, {}).update((a.name, None) for a in record.args)
    source = Source("example", section_id=section_id)
    return tuple(
        Symbol(path, _kind(path, api), (source,), (_example_signature(names, (source,)),))
        for path, names in sorted(keywords.items())
    )


def merge_additions(additions: Iterable[Symbol]) -> Inventory:
    """The additions of many examples as one inventory: one `Symbol` per path, its one example
    signature holding every keyword seen and every example `Source`. Order does not matter."""
    by_path: dict[str, list[Symbol]] = defaultdict(list)
    for symbol in additions:
        by_path[symbol.path].append(symbol)
    merged = []
    for path, group in by_path.items():
        sources = tuple(source for symbol in group for source in symbol.sources)
        names = {p.name: None for s in group for sig in s.signatures for p in sig.parameters}
        kind = min(s.kind for s in group)  # the same for one path; `min` keeps it order-free
        merged.append(Symbol(path, kind, sources, (_example_signature(names, sources),)))
    return Inventory(tuple(merged))


def _kind(path: str, api: ApiIndex) -> str:
    """The inventory's kind if it has the symbol; else by PEP 8 naming: a member of a class is a
    method, CapWords a class, anything else a function."""
    if path in api.symbols:
        return api.symbols[path].kind
    if api.is_member(path):
        return "method"
    return "class" if path.rsplit(".", 1)[-1][:1].isupper() else "function"


def _example_signature(names: Iterable[str], sources: tuple[Source, ...]) -> Signature:
    """Only what an example shows: the keywords used, none of them known to be required."""
    parameters = tuple(
        Parameter(name, "positional_or_keyword", False, sources) for name in sorted(names)
    )
    return Signature(parameters, sources)


@dataclass(frozen=True)
class _Target:
    path: str
    how: ResolvedBy
    wrong_module: str | None = None  # the path as written, when imported from the wrong module


def _callee(
    record: RawCallRecord, api: ApiIndex, types: dict[int, str | None]
) -> _Target | UnresolvedCall:
    callee = record.callee

    def missing(
        reason: UnresolvedReason, path: str | None = None, found: Iterable[str] = ()
    ) -> UnresolvedCall:
        return UnresolvedCall(record.index, record.line, record.symbol, reason, path, tuple(found))

    def lookup(path: str, how: ResolvedBy | None = None) -> _Target | UnresolvedCall:
        found = api.resolve(path)
        if found.path is None:
            reason: UnresolvedReason = "ambiguous" if found.candidates else "not-in-inventory"
            return missing(reason, found.wanted, found.candidates)
        assert found.how is not None
        return _Target(found.path, how or found.how, path if found.wrong_module else None)

    if callee.kind == "import" and callee.path is not None:
        return lookup(callee.path)
    if callee.kind == "call" and callee.call is not None:
        owner = types.get(callee.call)
        if owner is None or len(callee.attrs) != 1:
            return missing("unknown-type")
        member = f"{owner}.{callee.attrs[0]}"
        return (
            _Target(member, "variable")
            if member in api.symbols
            else missing("not-in-inventory", member)
        )
    if callee.kind != "name" or callee.name is None:
        return missing("unknown-type")
    if callee.name in api.packages:
        return lookup(".".join((callee.name, *callee.attrs)), "name")

    # an unbound name used as a symbol's own name: `Retry(…)`, `Timeout.from_float(…)`. Only
    # the first name is looked up, so a variable (`http.request`) never matches by its last part
    found: set[str] = set()
    candidates: set[str] = set()
    for package in api.packages:
        result = api.resolve(f"{package}.{callee.name}")
        if result.path is not None:
            found.add(result.path)
        candidates.update(result.candidates)
    if len(found) > 1 or (not found and candidates):
        return missing("ambiguous", None, sorted(found | candidates))
    if not found:
        return missing("unknown-type" if callee.attrs else "not-in-inventory")
    (owner,) = found
    if not callee.attrs:
        return _Target(owner, "name")
    if not api.is_class(owner):
        return missing("unknown-type")
    member = ".".join((owner, *callee.attrs))
    return _Target(member, "name") if member in api.symbols else missing("not-in-inventory", member)


def _bind(
    record: RawCallRecord, symbol: Symbol, target: _Target
) -> tuple[CallRecord, Signature | None]:
    if symbol.signatures:
        attempts = [_bind_signature(record, signature) for signature in symbol.signatures]
        best = min(range(len(attempts)), key=lambda i: (len(attempts[i][2]), i))
        args, unmapped, issues = attempts[best]
        number: int | None = best
        signature: Signature | None = symbol.signatures[best]
    else:
        args, unmapped, issues = _bind_keywords_only(record)
        number = signature = None
    found: list[CallIssue] = []
    if target.wrong_module is not None:
        found.append(CallIssue("wrong-module", target.wrong_module))
    if symbol.kind not in CALLABLE_KINDS:
        found.append(CallIssue("not-callable", symbol.kind))
    normalized = CallRecord(
        index=record.index,
        line=record.line,
        end_line=record.end_line,
        symbol=symbol.path,
        resolved_by=target.how,
        signature=number,
        args=args,
        unmapped=unmapped,
        issues=(*found, *issues),
    )
    return normalized, signature


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
    extra: dict[str, Value] = {}  # Python rejects a repeated keyword, so no duplicates here
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
