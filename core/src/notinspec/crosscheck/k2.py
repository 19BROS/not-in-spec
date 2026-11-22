"""K2 · claim vs. signature (SPEC §6.5): does a claim contradict the signature it describes?

Two checks, both reported as `Finding(check="K2")`:

1. **Claim vs. signature fact** (NLI, `check_claims_against_signatures`). Each fact of a
   symbol's signature becomes one sentence (`signature_facts`), the NLI premise:

   | fact | sentence |
   |---|---|
   | default | The default value of the total parameter of Retry is 10. |
   | type | The conn parameter of is_connection_dropped() has type BaseHTTPConnection. |
   | return type | Retry.increment() returns Retry. |
   | attribute / property type | The read_timeout property of Timeout has type float or None. |
   | enum, range, unit, format | The method parameter of request() must be one of 'GET', 'POST'. |

   Facts that are left out, because on urllib3 (run 009) they gave only false contradictions:

   - a default of `None` or one that is not a literal (`_TYPE_DEFAULT.token`): `None` means
     "computed inside", so "defaults to `ssl.CERT_REQUIRED`" in the prose is no contradiction
     (with `None` defaults, 14 more contradiction pairs, all false, as many as all others);
   - "is required": NLI reads it as "is not None" ("The timeout parameter … accepts None");
   - a value that differs between overloads (`tls_in_tls: Literal[False]` / `bool`).

   **Prefilter:** a claim is compared only with facts of the symbol documented in the claim's
   own section (an API description; guide claims name symbols by short, ambiguous names, so
   they are not compared yet), and only with facts it can be about: a parameter fact when the
   claim names the parameter, a return type when it says "return", an attribute's type always.
   A parameter name that is a plain word (`read`, `method`, `total`) counts only in backticks,
   next to "parameter" / "argument", or as `name=`.

   **Decision:** NLI in both directions (premise = fact, hypothesis = claim, and back), argmax.
   A contradiction in **either** direction is a contradiction. Unlike K5, one direction is
   enough: on run 009 the one real error in the docs that K2 finds (urllib3's
   `is_connection_dropped()` prose says `HTTPConnection`, the parameter entry
   `BaseHTTPConnection`) is a contradiction only from claim to fact. A K2 finding still has
   `low` confidence: most of them are not errors in the docs (see SPEC §6.5), so they go to
   review by our team.

2. **Annotation vs. documented type** (deterministic, `check_documented_types`): within one API
   description, the signature's annotation and the type its `Parameters` entry or `Return type`
   line states. urllib3's `Timeout.read_timeout: float | None` says `int, float or None` in its
   `Return type`. Types are compared as sets of names (`type_names`): module prefixes, `|`,
   commas and "or", `Optional`, `Literal` values and overloads (their union) do not count as a
   difference. A finding has `medium` confidence: the comparison is code, but type text written
   by hand is read by heuristics.

Pure: same claims, chunks, inventory and scores ⇒ equal result, in any order of `claims`.
"""

import ast
import re
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass
from typing import Literal

from notinspec.chunking import Block, Chunk, SignatureParameter
from notinspec.claims import GroundedClaim
from notinspec.crosscheck.k5a import claim_ref
from notinspec.findings import Evidence, EvidenceKind, Finding, NliEvidence
from notinspec.grounding import normalize
from notinspec.inventory import Constraint, Inventory, Parameter, Symbol
from notinspec.nli import DECISION_RULE, NliModel, NliScores

# bump when a result can change for the same input (facts, prefilter, decision, grouping)
K2_VERSION = 1
PREFILTER_RULE = "own-section+names-fact"
PREMISE_RULE = "fact-sentence"  # the templates in `_sentence` and friends
TYPE_RULE = "type-names"  # `type_names`

type FactKind = Literal["default", "type", "returns", "enum", "range", "unit", "format"]

_CALLABLE = frozenset({"function", "method", "classmethod", "staticmethod"})
_CLASS = frozenset({"class", "exception"})
_RETURN = re.compile(r"\breturn(?:s|ed|ing)?\b", re.IGNORECASE)
_PLAIN_WORD = re.compile(r"[a-z]+")
_ARG_WORD = r"(?:parameter|argument|param|arg|keyword)s?"


@dataclass(frozen=True)
class SignatureFact:
    """One fact of a signature, as one sentence for NLI and the docs text it comes from."""

    ref: str  # "urllib3.util.Retry(total).default", "urllib3.util.Timeout.read_timeout.type"
    symbol: str  # `Symbol.path`
    kind: FactKind
    parameter: str | None  # None: about the symbol (return type, attribute type)
    value: str  # as written: "10", "int | None", "'GET', 'POST'"
    sentence: str  # the NLI premise
    quote: str  # docs text the author can find: "total=10", "conn (BaseHTTPConnection)"
    section_id: str
    chunk_id: str  # the chunk with the signature
    evidence: EvidenceKind  # "parameter", "constraint" or "signature"


@dataclass(frozen=True)
class FactPair:
    claim: str  # claim_ref
    fact: str  # SignatureFact.ref, in the claim's section
    fact_to_claim: NliScores  # premise = fact sentence, hypothesis = claim
    claim_to_fact: NliScores
    contradiction: bool  # argmax contradiction in either direction


@dataclass(frozen=True)
class K2Versions:
    check: int  # K2_VERSION
    prefilter: str
    premise: str
    nli_model: str
    nli_revision: str
    decision_rule: str

    def pairs(self) -> tuple[tuple[str, str], ...]:
        return (
            ("decision_rule", self.decision_rule),
            ("k2", str(self.check)),
            ("nli_model", self.nli_model),
            ("nli_revision", self.nli_revision),
            ("premise", self.premise),
            ("prefilter", self.prefilter),
        )


@dataclass(frozen=True)
class K2Result:
    facts: tuple[SignatureFact, ...]  # sections in docs order, then signature order
    pairs: tuple[FactPair, ...]  # input order of the claims, then fact order
    findings: tuple[Finding, ...]  # sorted by key
    # claims in a contradiction, sorted: no test material until review (as K5's `contradicted`)
    contradicted: tuple[str, ...]
    versions: K2Versions


# --- facts ------------------------------------------------------------------------------------


def signature_facts(chunks: Sequence[Chunk], inventory: Inventory) -> tuple[SignatureFact, ...]:
    """The facts of every symbol documented in an API description in `chunks`.

    Parameters, defaults, constraints and return types come from the inventory; the type of an
    attribute or property from its signature block (the inventory has no type for them).
    """
    symbols = {s.path: s for s in inventory.symbols}
    out: list[SignatureFact] = []
    for section in _sections(chunks):
        for path, (chunk, blocks) in _documented(section).items():
            symbol = symbols.get(path)
            if symbol is not None:
                out += _facts(symbol, symbols, section, chunk, blocks)
    return tuple(out)


def _facts(
    symbol: Symbol,
    symbols: dict[str, Symbol],
    section: Sequence[Chunk],
    chunk: Chunk,
    blocks: Sequence[Block],
) -> list[SignatureFact]:
    name = _display(symbol, symbols)
    owner = _owner(symbol, symbols)
    section_id = chunk.section_id
    fields = _field_types(section)
    out: list[SignatureFact] = []

    def fact(kind: FactKind, parameter: str | None, value: str, sentence: str, quote: str) -> None:
        evidence: EvidenceKind = (
            "signature"
            if parameter is None
            else "parameter"
            if kind in ("default", "type")
            else "constraint"
        )
        suffix = f"({parameter}).{kind}" if parameter else f".{kind}"
        out.append(
            SignatureFact(
                f"{symbol.path}{suffix}",
                symbol.path,
                kind,
                parameter,
                value,
                sentence,
                quote,
                section_id,
                chunk.id,
                evidence,
            )
        )

    if not symbol.signatures:
        typed = next((b for b in blocks if b.parameters is None and b.type), None)
        if typed is not None and typed.type:
            what = f"The {_short(symbol.path)} {symbol.kind} of {owner}" if owner else name
            short = _short(symbol.path)
            fact(
                "type",
                None,
                typed.type,
                f"{what} has type {_render(typed.type, owner)}.",
                f"{short}: {typed.type}",
            )
        return out

    for param in _parameters(symbol):
        p = param.name
        written = _written(blocks, p)
        default = _same(s.default for s in _overloads(symbol, p))
        if default is not None and default != "None" and _literal(default):
            fact(
                "default",
                p,
                default,
                f"The default value of the {p} parameter of {name} is {default}.",
                written or f"{p}={default}",
            )
        type_ = _same(s.type for s in _overloads(symbol, p))
        if type_ and not _is_literal_type(type_):
            quote = written if written and ":" in written else None
            if quote is None:
                quote = f"{p} ({type_})" if fields.get(p) == type_ else f"{p}: {type_}"
            fact(
                "type",
                p,
                type_,
                f"The {p} parameter of {name} has type {_render(type_, owner)}.",
                quote,
            )
        constraints = _same(s.constraints for s in _overloads(symbol, p))
        for c in constraints or ():
            sentence = _constraint_sentence(c, p, name)
            if sentence:
                fact(c.kind, p, _constraint_value(c), sentence, written or p)

    if symbol.kind not in _CLASS:
        returns = _same(sig.returns.type if sig.returns else None for sig in symbol.signatures)
        if returns:
            arrow = next((b.type for b in blocks if b.parameters is not None and b.type), None)
            quote = f"-> {arrow}" if arrow == returns else f"Return type: {returns}"
            fact("returns", None, returns, f"{name} returns {_render(returns, owner)}.", quote)
    return out


def _constraint_sentence(c: Constraint, p: str, name: str) -> str | None:
    subject = f"The {p} parameter of {name}"
    if c.kind == "enum" and c.values:
        return f"{subject} must be one of {', '.join(c.values)}."
    if c.kind == "range" and (c.minimum is not None or c.maximum is not None):
        low = f"greater than {c.minimum}" if c.exclusive_minimum else f"at least {c.minimum}"
        high = f"less than {c.maximum}" if c.exclusive_maximum else f"at most {c.maximum}"
        if c.minimum is not None and c.maximum is not None:
            return f"{subject} must be {low} and {high}."
        return f"{subject} must be {low if c.minimum is not None else high}."
    if c.kind == "unit" and c.unit:
        return f"{subject} is given in {c.unit}."
    if c.kind == "format" and c.format:
        return f"{subject} has the format {c.format}."
    return None


def _constraint_value(c: Constraint) -> str:
    if c.kind == "enum":
        return ", ".join(c.values)
    if c.kind == "range":
        return f"{c.minimum or ''}..{c.maximum or ''}"
    return c.unit or c.format or ""


def _parameters(symbol: Symbol) -> list[Parameter]:
    """Each parameter once, in the order of its first signature; `*args` / `**kwargs` skipped."""
    seen: dict[str, Parameter] = {}
    for sig in symbol.signatures:
        for p in sig.parameters:
            if p.kind not in ("var_positional", "var_keyword"):
                seen.setdefault(p.name, p)
    return list(seen.values())


def _overloads(symbol: Symbol, name: str) -> list[Parameter]:
    return [p for sig in symbol.signatures for p in sig.parameters if p.name == name]


def _same[T](values: Iterable[T]) -> T | None:
    """The value if every overload has the same one, else None (it depends on the overload)."""
    distinct = list(dict.fromkeys(values))
    return distinct[0] if len(distinct) == 1 else None


def _literal(value: str) -> bool:
    """A Python literal as written (`10`, `'latin-1'`, `frozenset({'GET'})`), not a name."""
    try:
        node = ast.parse(value, mode="eval").body
    except SyntaxError:
        return False
    return _literal_node(node)


def _literal_node(node: ast.expr) -> bool:
    match node:
        case ast.Constant():
            return True
        case ast.UnaryOp(op=ast.USub() | ast.UAdd(), operand=ast.Constant()):
            return True
        case ast.Tuple(elts=items) | ast.List(elts=items) | ast.Set(elts=items):
            return all(_literal_node(i) for i in items)
        case ast.Dict(keys=keys, values=values):
            return all(k is not None and _literal_node(k) for k in keys) and all(
                _literal_node(v) for v in values
            )
        case ast.Call(func=ast.Name(id="frozenset" | "set" | "tuple" | "list"), args=args):
            return not node.keywords and all(_literal_node(a) for a in args)
    return False


def _is_literal_type(value: str) -> bool:
    return re.fullmatch(r"(?:typing(?:_extensions)?\.)?Literal\[.*\]", value) is not None


def _render(type_: str, owner: str | None) -> str:
    """`bool | int | None` → "bool, int or None"; `Self` → the class; numpydoc's `, optional`
    and `, default 3` are left out (they are not the type)."""
    kept = [p for p in _split_top(type_, ",") if p != "optional" and not re.match(r"default\b", p)]
    parts = _split_top(", ".join(kept), "|")
    text = parts[0] if len(parts) == 1 else ", ".join(parts[:-1]) + " or " + parts[-1]
    return re.sub(r"\bSelf\b", owner, text) if owner else text


def _display(symbol: Symbol, symbols: dict[str, Symbol]) -> str:
    short = _short(symbol.path)
    owner = _owner(symbol, symbols)
    name = f"{owner}.{short}" if owner and symbol.kind not in _CLASS else short
    return f"{name}()" if symbol.kind in _CALLABLE else name


def _owner(symbol: Symbol, symbols: dict[str, Symbol]) -> str | None:
    """Short name of the class the symbol is in, None for a module-level symbol."""
    parent = symbols.get(symbol.path.rsplit(".", 1)[0])
    if parent is not None and parent.kind in _CLASS:
        return _short(parent.path)
    return _short(symbol.path) if symbol.kind in _CLASS else None


def _short(path: str) -> str:
    return path.rsplit(".", 1)[-1]


def _written(blocks: Sequence[Block], name: str) -> str | None:
    """The parameter as the signature shows it: `total=10`, `keyfile: str | None = None`."""
    for block in blocks:
        for p in block.parameters or ():
            if p.name.lstrip("*") == name:
                return _parameter_text(p)
    return None


def _parameter_text(p: SignatureParameter) -> str:
    out = p.name + (f": {p.annotation}" if p.annotation else "")
    if p.default is not None:
        out += f" = {p.default}" if p.annotation else f"={p.default}"
    return out


def _field_types(section: Sequence[Chunk]) -> dict[str, str]:
    types: dict[str, str] = {}
    for chunk in section:
        for b in chunk.blocks:
            if b.kind == "field" and b.field == "param" and b.name and b.type:
                types.setdefault(b.name.lstrip("*"), b.type)
    return types


def _sections(chunks: Sequence[Chunk]) -> list[list[Chunk]]:
    """All parts of each section, in docs order (first appearance, then part)."""
    by_id: dict[str, list[Chunk]] = defaultdict(list)
    for chunk in chunks:
        by_id[chunk.section_id].append(chunk)
    return [sorted(parts, key=lambda c: c.part) for parts in by_id.values()]


def _documented(section: Sequence[Chunk]) -> dict[str, tuple[Chunk, list[Block]]]:
    """Symbol path → the chunk with its first signature block and all its signature blocks."""
    out: dict[str, tuple[Chunk, list[Block]]] = {}
    for chunk in section:
        for b in chunk.blocks:
            if b.kind == "signature" and b.objtype and b.name:
                out.setdefault(b.name, (chunk, []))[1].append(b)
    return out


# --- claims vs. facts -------------------------------------------------------------------------


def names_fact(claim: str, fact: SignatureFact) -> bool:
    """Prefilter: can the claim be about this fact?"""
    if fact.parameter is not None:
        return names_parameter(claim, fact.parameter)
    if fact.kind == "returns":
        return _RETURN.search(claim) is not None
    return True  # the type of an attribute or property: every claim of its section


def names_parameter(claim: str, name: str) -> bool:
    """Does the claim name the parameter? A plain word (`read`, `total`) only in backticks,
    next to "parameter" / "argument", or as `name=`; other names (`backoff_factor`) anywhere."""
    if re.search(rf"`{re.escape(name)}(?:=[^`]*)?`", claim):
        return True
    text = claim.replace("`", "")
    n = re.escape(name)
    if _PLAIN_WORD.fullmatch(name) is None:
        return re.search(rf"(?<!\w){n}(?!\w)", text) is not None
    return (
        re.search(rf"(?<![\w.]){n}\s+{_ARG_WORD}\b", text, re.IGNORECASE) is not None
        or re.search(rf"\b{_ARG_WORD}\s+{n}(?![\w.])", text, re.IGNORECASE) is not None
        or re.search(rf"(?<![\w.]){n}=", text) is not None
    )


def check_claims_against_signatures(
    claims: Sequence[GroundedClaim],
    chunks: Sequence[Chunk],
    inventory: Inventory,
    nli: NliModel,
) -> K2Result:
    """K2 with NLI on the `kept` claims of `claims` (other statuses are ignored).

    `chunks` are all chunks of the docs: a claim's section is found through its chunk, and a
    section split into parts has its signature in the first part only.
    """
    kept = [c for c in claims if c.status == "kept"]
    refs = [claim_ref(c) for c in kept]
    if len(set(refs)) != len(refs):
        raise ValueError("two kept claims have the same chunk, extractor and local id")
    by_id = {c.id: c for c in chunks}
    facts = signature_facts(chunks, inventory)
    by_section: dict[str, list[SignatureFact]] = defaultdict(list)
    for f in facts:
        by_section[f.section_id].append(f)

    candidates: list[tuple[int, SignatureFact]] = []
    for i, c in enumerate(kept):
        chunk = by_id.get(c.claim.chunk_id)
        if chunk is None:
            raise ValueError(f"claim {refs[i]} is in chunk {c.claim.chunk_id}, not in `chunks`")
        candidates += [
            (i, f) for f in by_section.get(chunk.section_id, ()) if names_fact(c.claim.text, f)
        ]
    texts: list[tuple[str, str]] = []
    for i, f in candidates:
        texts += [(f.sentence, kept[i].claim.text), (kept[i].claim.text, f.sentence)]
    texts = list(dict.fromkeys(texts))
    scores = dict(zip(texts, nli.score(texts), strict=True)) if texts else {}
    pairs = []
    for i, f in candidates:
        forward = scores[(f.sentence, kept[i].claim.text)]
        back = scores[(kept[i].claim.text, f.sentence)]
        contradiction = "contradiction" in (forward.label, back.label)
        pairs.append(FactPair(refs[i], f.ref, forward, back, contradiction))

    versions = K2Versions(
        K2_VERSION, PREFILTER_RULE, PREMISE_RULE, nli.model_id, nli.revision, DECISION_RULE
    )
    findings = _findings(kept, refs, by_id, candidates, pairs, versions)
    contradicted = tuple(sorted({p.claim for p in pairs if p.contradiction}))
    return K2Result(facts, tuple(pairs), findings, contradicted, versions)


def _findings(
    kept: Sequence[GroundedClaim],
    refs: Sequence[str],
    by_id: dict[str, Chunk],
    candidates: Sequence[tuple[int, SignatureFact]],
    pairs: Sequence[FactPair],
    versions: K2Versions,
) -> tuple[Finding, ...]:
    """One finding per signature fact and docs text: claims that contradict the same fact and
    quote the same text, or overlapping text of one chunk, are one problem in the docs. On run
    009, qwen quoted ":param conn: `…HTTPConnection` object." and gemma "`param conn: …`", and
    one of them ended a quote with a full stop where the other did not."""
    by_fact: dict[tuple[str, str], list[tuple[int, SignatureFact, FactPair]]] = {}
    for (i, f), p in zip(candidates, pairs, strict=True):
        if p.contradiction:
            by_fact.setdefault((f.section_id, f.ref), []).append((i, f, p))
    groups: list[list[tuple[int, SignatureFact, FactPair]]] = []
    for members in by_fact.values():
        groups += _same_text(kept, members)
    findings = []
    for group in groups:
        # the message names the claim that comes first in the docs, in any input order
        members = sorted(group, key=lambda m: (kept[m[0]].citation_span or (-1, -1), refs[m[0]]))
        i, f, _ = members[0]
        claims = [
            _claim_evidence(kept[k], refs[k], by_id[kept[k].claim.chunk_id]) for k, _, _ in members
        ]
        more = len(members) - 1
        findings.append(
            Finding(
                check="K2",
                kind="contradiction",
                subject=f.symbol,
                message=(
                    f"a claim contradicts the signature of {f.symbol}: “{kept[i].claim.text}” "
                    f"vs `{f.quote}`" + (f" (+{more} more claims)" if more else "")
                ),
                confidence="low",
                evidence=(_fact_evidence(f), *claims),
                nli=tuple(
                    n
                    for _, _, p in members
                    for n in (
                        NliEvidence(p.fact, p.claim, p.fact_to_claim),
                        NliEvidence(p.claim, p.fact, p.claim_to_fact),
                    )
                ),
                versions=versions.pairs(),
            )
        )
    return tuple(sorted(findings, key=lambda x: x.key))


def _same_text[T](
    kept: Sequence[GroundedClaim], members: list[tuple[int, SignatureFact, T]]
) -> list[list[tuple[int, SignatureFact, T]]]:
    """Members grouped (transitively) by equal normalized citation or overlapping citation
    span in one chunk; groups in the order of their first member."""
    parent = list(range(len(members)))

    def find(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x

    for x, (i, _, _) in enumerate(members):
        for y in range(x):
            a, b = kept[i].claim, kept[members[y][0]].claim
            sa, sb = kept[i].citation_span, kept[members[y][0]].citation_span
            overlap = (
                a.chunk_id == b.chunk_id
                and sa is not None
                and sb is not None
                and sa[0] < sb[1]
                and sb[0] < sa[1]
            )
            if overlap or normalize(a.citation) == normalize(b.citation):
                parent[find(x)] = find(y)
    groups: dict[int, list[tuple[int, SignatureFact, T]]] = {}
    for x, member in enumerate(members):
        groups.setdefault(find(x), []).append(member)
    return list(groups.values())


def _fact_evidence(f: SignatureFact) -> Evidence:
    return Evidence(
        kind=f.evidence,
        ref=f.ref,
        text=f.sentence,
        section_id=f.section_id,
        chunk_id=f.chunk_id,
        quote=f.quote,
    )


def _claim_evidence(claim: GroundedClaim, ref: str, chunk: Chunk) -> Evidence:
    return Evidence(
        kind="claim",
        ref=ref,
        text=claim.claim.text,
        section_id=chunk.section_id,
        chunk_id=chunk.id,
        quote=claim.claim.citation,
        span=claim.citation_span,
    )


# --- annotation vs. documented type -----------------------------------------------------------


def check_documented_types(chunks: Sequence[Chunk]) -> tuple[Finding, ...]:
    """Deterministic K2: annotation vs. the type the `Parameters` entry or `Return type` states,
    within one API description. Sorted by key."""
    findings: list[Finding] = []
    versions = (("k2", str(K2_VERSION)), ("type_rule", TYPE_RULE))
    for section in _sections(chunks):
        documented = _documented(section)
        if not documented:
            continue
        path, (chunk, blocks) = next(iter(documented.items()))
        signatures = [b for _, bs in documented.values() for b in bs]
        for field_chunk, field in _fields(section):
            if field.field == "param" and field.name and field.type:
                name = field.name.lstrip("*")
                annotations = [
                    p.annotation
                    for b in signatures
                    for p in b.parameters or ()
                    if p.name.lstrip("*") == name and p.annotation
                ]
                written = f"{name} ({field.type})"
                ref = f"{path}({name})"
                what = f"the {name} parameter"
            elif field.field == "return-type" and field.type:
                annotations = [b.type for b in signatures if b.type]
                written = f"Return type: {field.type}"
                ref = path
                what = "the return type" if blocks[0].parameters is not None else "the type"
            else:
                continue
            if not annotations or _union(annotations) == type_names(field.type):
                continue
            shown = " / ".join(dict.fromkeys(annotations))
            kind: EvidenceKind = "parameter" if field.field == "param" else "signature"
            findings.append(
                Finding(
                    check="K2",
                    kind="type-mismatch",
                    subject=path,
                    message=(
                        f"{path}: the signature gives {what} as `{shown}`, "
                        f"the docs text as `{field.type}`"
                    ),
                    confidence="medium",
                    evidence=(
                        Evidence(
                            kind,
                            f"{ref}.annotation",
                            shown,
                            chunk.section_id,
                            chunk_id=chunk.id,
                            quote=shown,
                        ),
                        Evidence(
                            kind,
                            f"{ref}.documented",
                            field.type,
                            field_chunk.section_id,
                            chunk_id=field_chunk.id,
                            quote=written,
                        ),
                    ),
                    versions=versions,
                )
            )
    return tuple(sorted(findings, key=lambda f: f.key))


def _fields(section: Sequence[Chunk]) -> list[tuple[Chunk, Block]]:
    """The first `Return type` line and every typed `Parameters` entry of the section."""
    out: list[tuple[Chunk, Block]] = []
    seen_return = False
    for chunk in section:
        for b in chunk.blocks:
            if b.field == "param" and b.kind == "field" and b.type:
                out.append((chunk, b))
            elif b.field == "return-type" and b.type and not seen_return:
                seen_return = True
                out.append((chunk, b))
    return out


def _union(types: Iterable[str]) -> frozenset[str]:
    out: set[str] = set()
    for t in types:
        out |= type_names(t)
    return frozenset(out)


_WORDS = {"integer": "int", "string": "str", "boolean": "bool", "none": "None"}


def type_names(text: str) -> frozenset[str]:
    """The types a type text allows, as names: `int, float, or None` → {int, float, None},
    `Optional[ssl.SSLSocket]` → {SSLSocket, None}, `Literal[False]` → {bool}. numpydoc's
    "optional" and "default …" (`int, optional`) say nothing about the type and are skipped."""
    out: set[str] = set()
    for part in _split_top(text, "|", ",", " or "):
        part = re.sub(r"^or\s+", "", part).strip()
        if part == "optional" or re.match(r"default\b", part):
            continue
        part = re.sub(r"\btyping(?:_extensions)?\.", "", part)
        head, bracket, rest = part.partition("[")
        inner = rest[:-1] if bracket and rest.endswith("]") else None
        if head in ("Optional", "Union") and inner is not None:
            out |= type_names(inner)
            if head == "Optional":
                out.add("None")
        elif head == "Literal" and inner is not None:
            out |= {_literal_type(v) for v in _split_top(inner, ",")}
        elif part:
            name = _WORDS.get(head.lower(), head.rsplit(".", 1)[-1])
            out.add(name + ("[" + "".join(rest.split()) if bracket else ""))
    return frozenset(out)


def _literal_type(value: str) -> str:
    try:
        literal = ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return value
    return "None" if literal is None else type(literal).__name__


def _split_top(text: str, *separators: str) -> list[str]:
    """Split at separators outside brackets; empty parts are dropped, the others stripped."""
    parts: list[str] = []
    depth, start, i = 0, 0, 0
    while i < len(text):
        char = text[i]
        if char in "([{":
            depth += 1
        elif char in ")]}":
            depth -= 1
        elif depth == 0:
            sep = next((s for s in separators if text.startswith(s, i)), None)
            if sep is not None:
                parts.append(text[start:i])
                i += len(sep)
                start = i
                continue
        i += 1
    parts.append(text[start:])
    return [p.strip() for p in parts if p.strip()]
