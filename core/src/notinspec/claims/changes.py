"""*Change* claims → `Change` candidates for review (SPEC §6.3, component D).

A kept claim of type `change` says something changed, in free text. Code decides what, and the
LLM decides nothing beyond which sentence the claim is about:

- **Sentence:** the prose sentence(s) the citation lies in. Only three forms count, each at the
  start of a sentence: `Removed <names>`, `Deprecated <names>`, `Rename(d) <old> to <new>`.
  So `Removed support for ... via `commonName`` and `an `ImportError` is raised` name nothing.
- **Names:** the code literals of that form that the claim's text also names, so a claim about
  one of three listed names gives one `Change`.
- **Symbol and parameter:** resolved against the inventory (`Retry` → `urllib3.util.Retry`).
- **Version:** the changelog heading the chunk is under (`2.0.0 (2023-04-26)` → `2.0.0`).
- **Kind:** as the sentence says. A rename is `deprecated` if the old name is still in the
  inventory, otherwise `removed`. A name said to be removed that is still in the inventory is
  skipped: `urllib3.request` was a module, and is now a function.

The result is a list of candidates, not inventory: every `Source` is `changelog` (low
confidence), and `review` says what a person has to confirm (SPEC §6.3, "Review of a *change*
claim"). A candidate whose key matches a version directive needs no review of the key.
"""

import re
from collections import defaultdict
from collections.abc import Iterable, Sequence
from dataclasses import dataclass, replace
from typing import Literal

from notinspec.chunking import Chunk, Sentence, prose_sentences
from notinspec.claims.pipeline import GroundedClaim
from notinspec.inventory import (
    Change,
    ChangeKind,
    Conflict,
    Inventory,
    Source,
    change_key,
    merge,
    parse_version,
)

# bump when a result can change for the same claims, chunks and inventory
CHANGE_RULES_VERSION = 1

type ReviewReason = Literal["no-directive", "replacement", "removal-planned"]
type SkipReason = Literal[
    "no-version-heading",  # the chunk is not under a version heading
    "no-api-name",  # the sentence is not one of the three forms, or the claim names none of it
    "unresolved-name",  # not in the inventory and not qualified with the project
    "ambiguous-name",  # a short name that fits several symbols
    "parameter-without-owner",  # a parameter, but the sentence doesn't say of what
    "still-in-inventory",  # said to be removed, but the name exists
]

_LITERAL = r"`[^`\n]+`"
_NAMES = rf"{_LITERAL}(?:\s*(?:,\s*and|,|and)\s+{_LITERAL})*"
_NOUN = (
    r"(?:parameter/attribute|parameters?|options?|arguments?|attributes?|propert(?:y|ies)"
    r"|methods?|functions?|class(?:es)?|modules?|constants?)"
)
_START = r"(?:^|(?<=[.;:])\s+)(?:[-*+]\s+)?"
_FORM = re.compile(
    rf"{_START}(?P<verb>Removed|Deprecated)\s+(?:the\s+)?(?:deprecated\s+)?"
    rf"(?P<first>{_NAMES})(?:\s+(?P<noun>{_NOUN}))?(?:\s+(?P<second>{_NAMES}))?"
    rf"(?:,?\s+(?:from|of)\s+(?:the\s+)?(?:(?:private|public)\s+)?(?:{_NOUN}\s+)?"
    rf"(?P<owners>{_NAMES}))?"
    rf"(?:\s+in\s+favou?r\s+of\s+(?P<new>{_NAMES}))?"
    r"(?:\s+(?:which|and)\s+will\s+be\s+removed\s+in\s+\S+\s+v?(?P<planned>\d+(?:\.\d+)*))?"
)
_RENAME = re.compile(
    rf"{_START}Renamed?\s+(?:the\s+)?(?P<old>{_LITERAL})\s+to\s+(?P<new>{_LITERAL})"
)
_CALL = re.compile(r"(?P<owner>[\w.]+)\((?P<parameter>\w+)=.*\)")
_IDENTIFIER = re.compile(r"[A-Za-z_][\w.]*")
_VERSION_HEADING = re.compile(r"v?(\d+(?:\.\d+)+\S*)(?:\s+\([^)]*\))?")


@dataclass(frozen=True)
class ClaimRef:
    """The claim a candidate came from: its identity in `claims.json`."""

    chunk_id: str
    extractor: str
    local_id: str


@dataclass(frozen=True)
class ChangeCandidate:
    change: Change  # one per key; `sources` are all `changelog`
    claims: tuple[ClaimRef, ...]  # sorted
    review: tuple[ReviewReason, ...]  # what a person has to confirm; () = nothing


@dataclass(frozen=True)
class SkippedChangeClaim:
    claim: ClaimRef
    reason: SkipReason
    name: str | None = None  # the name it is about, when it got that far


@dataclass(frozen=True)
class ChangeClaims:
    candidates: tuple[ChangeCandidate, ...]  # by change key
    skipped: tuple[SkippedChangeClaim, ...]  # claim order
    conflicts: tuple[Conflict, ...]  # same key, different attributes (a `Finding`, SPEC §6.3)


class _Skip(Exception):
    def __init__(self, reason: SkipReason, name: str) -> None:
        self.reason: SkipReason = reason
        self.name = name


@dataclass(frozen=True)
class _Mention:
    """One name of a sentence, before it is resolved."""

    written: str
    kind: Literal["removed", "deprecated", "renamed"]
    noun: str | None
    owners: tuple[str, ...]
    new: str | None
    planned: str | None


def changes_from_claims(
    claims: Iterable[GroundedClaim], chunks: Sequence[Chunk], inventory: Inventory, project: str
) -> ChangeClaims:
    """Candidates from the kept `change` claims. Other claims are ignored."""
    by_id = {c.id: c for c in chunks}
    names = _Names(inventory, project)
    sentences: dict[str, tuple[Sentence, ...]] = {}
    found: list[tuple[Change, ClaimRef, bool]] = []
    skipped: list[SkippedChangeClaim] = []

    for grounded in claims:
        claim = grounded.claim
        if claim.type != "change" or grounded.status != "kept" or grounded.citation_span is None:
            continue
        ref = ClaimRef(claim.chunk_id, claim.extractor, claim.local_id)
        chunk = by_id[claim.chunk_id]
        version = _heading_version(chunk)
        if version is None:
            skipped.append(SkippedChangeClaim(ref, "no-version-heading"))
            continue
        start, end = grounded.citation_span
        split = sentences.setdefault(chunk.id, prose_sentences(chunk))
        cited = [chunk.text[s.start : s.end] for s in split if s.start < end and start < s.end]
        mentions = [m for t in cited for m in _mentions(t) if _named(claim.text, m.written)]
        if not mentions:
            skipped.append(SkippedChangeClaim(ref, "no-api-name"))
            continue
        source = Source("changelog", chunk.section_id)
        citation = chunk.text[start:end]
        for mention in mentions:
            for owner in _owners(mention):  # one bad owner must not lose the others
                try:
                    change, verified = names.change(mention, owner, version, source, citation)
                except _Skip as skip:
                    skipped.append(SkippedChangeClaim(ref, skip.reason, skip.name))
                else:
                    found.append((change, ref, verified))

    merged, conflicts = merge([Inventory((), tuple(c for c, _, _ in found))])
    refs: dict[object, set[ClaimRef]] = defaultdict(set)
    confirmed: set[tuple[object, str | None]] = set()  # replacements in inventory and citation
    for change, ref, ok in found:
        refs[change_key(change)].add(ref)
        if ok:
            confirmed.add((change_key(change), change.replacement))
    directives = {change_key(c) for c in inventory.changes}
    candidates = []
    for change in merged.changes:
        key = change_key(change)
        review: list[ReviewReason] = [] if key in directives else ["no-directive"]
        if change.replacement is not None and (key, change.replacement) not in confirmed:
            review.append("replacement")
        if change.removal_planned is not None:
            review.append("removal-planned")
        ordered = sorted(refs[key], key=lambda r: (r.chunk_id, r.extractor, r.local_id))
        candidates.append(ChangeCandidate(change, tuple(ordered), tuple(review)))
    return ChangeClaims(tuple(candidates), tuple(skipped), conflicts)


def _heading_version(chunk: Chunk) -> str | None:
    """The version of the deepest heading that is one (`2.0.0 (2023-04-26)`, `v1.2`)."""
    for heading in reversed(chunk.breadcrumb.split(" > ")[1:]):
        match = _VERSION_HEADING.fullmatch(heading.strip())
        if match and parse_version(match.group(1)) is not None:
            return match.group(1)
    return None


def _literals(text: str | None) -> tuple[str, ...]:
    return tuple(m[1:-1].strip() for m in re.findall(_LITERAL, text or ""))


def _mentions(sentence: str) -> list[_Mention]:
    """The names one sentence says changed; a sentence may be wrapped over several lines."""
    line = " ".join(sentence.split())
    result: list[_Mention] = []
    for rename in _RENAME.finditer(line):
        old, new = _literals(rename["old"])[0], _literals(rename["new"])[0]
        result.append(_Mention(old, "renamed", None, (), new, None))
    for form in _FORM.finditer(line):
        kind: Literal["removed", "deprecated"] = (
            "removed" if form["verb"] == "Removed" else "deprecated"
        )
        first, second = _literals(form["first"]), _literals(form["second"])
        written = second or first
        owners = _literals(form["owners"]) or (first if second else ())
        replacements = _literals(form["new"])
        for index, name in enumerate(written):
            replacement = replacements[0] if len(replacements) == 1 else None
            if len(replacements) == len(written):
                replacement = replacements[index]
            result.append(_Mention(name, kind, form["noun"], owners, replacement, form["planned"]))
    return result


def _owners(mention: _Mention) -> tuple[str | None, ...]:
    """`Retry(x=...)` names its own owner; otherwise each listed owner, or none."""
    if _CALL.fullmatch(mention.written) or not mention.owners:
        return (None,)
    return mention.owners


def _named(text: str, written: str) -> bool:
    """Does the claim's text name this literal? Compared by its last part, without `()`."""
    call = _CALL.fullmatch(written)
    name = call["parameter"] if call else written.removesuffix("()").rsplit(".", 1)[-1]
    return re.search(rf"(?<!\w){re.escape(name)}(?!\w)", text) is not None


def _is_parameter(noun: str | None, member: str) -> bool:
    if noun is None or member.isupper():  # `Retry` "options" can be class constants
        return False
    return noun.startswith(("parameter", "option", "argument"))


class _Names:
    """Names of one inventory: what exists, and how a written name resolves to a path."""

    def __init__(self, inventory: Inventory, project: str) -> None:
        self.project = project
        self.paths = {s.path for s in inventory.symbols}
        self.parameters = {
            s.path: {p.name for sig in s.signatures for p in sig.parameters}
            for s in inventory.symbols
        }

    def resolve(self, name: str) -> str:
        """Path of a written name, or `_Skip`. A name need not exist: only its owner must."""
        if name in self.paths:
            return name
        fits = sorted(p for p in self.paths if p.endswith(f".{name}"))
        if len(fits) > 1:
            raise _Skip("ambiguous-name", name)
        if fits:
            return fits[0]
        if not _IDENTIFIER.fullmatch(name):
            raise _Skip("unresolved-name", name)
        prefix = f"{self.project}."
        if name.startswith(prefix) and "." not in name[len(prefix) :]:
            # `urllib3.HTTPResponse` is a re-export of `urllib3.response.HTTPResponse`
            short = name[len(prefix) :]
            exported = sorted(p for p in self.paths if p.endswith(f".{short}"))
            return exported[0] if len(exported) == 1 else name
        if "." in name:
            parent, member = name.rsplit(".", 1)
            try:
                return f"{self.resolve(parent)}.{member}"
            except _Skip as skip:
                raise _Skip(skip.reason, name) from None
        raise _Skip("unresolved-name", name)

    def exists(self, symbol: str, parameter: str | None) -> bool:
        if parameter is not None:
            return parameter in self.parameters.get(symbol, ())
        return symbol in self.paths

    def target(self, mention: _Mention, owner: str | None) -> tuple[str, str | None]:
        """(symbol, parameter) the mention is about, for one of its owners."""
        written = mention.written.removesuffix("()")
        call = _CALL.fullmatch(written)
        if call:
            return self.resolve(call["owner"]), call["parameter"]
        if owner is not None:
            bare = owner.removesuffix("()")
            member = written.removeprefix(f"{bare}.")
            path = self.resolve(bare)
            if _is_parameter(mention.noun, member):
                return path, member
            return f"{path}.{member}", None
        if _is_parameter(mention.noun, written):
            if "." not in written:
                raise _Skip("parameter-without-owner", written)
            parent, parameter = written.rsplit(".", 1)
            return self.resolve(parent), parameter
        return self.resolve(written), None

    def replacement(self, new: str, symbol: str, parameter: str | None) -> tuple[str, bool]:
        """The replacement as stored, and whether it is in the inventory."""
        written = new.removesuffix("()")
        call = _CALL.fullmatch(written)
        if parameter is not None:  # a parameter is replaced by a parameter of the same symbol
            name = call["parameter"] if call else written.rsplit(".", 1)[-1]
            return name, self.exists(symbol, name)
        try:
            path = self.resolve(call["owner"] if call else written)
        except _Skip:
            return written, False
        return path, path in self.paths

    def change(
        self, mention: _Mention, owner: str | None, version: str, source: Source, citation: str
    ) -> tuple[Change, bool]:
        """The `Change`, and whether its replacement is in the inventory and the citation."""
        symbol, parameter = self.target(mention, owner)
        present = self.exists(symbol, parameter)
        if mention.kind == "removed" and present:
            raise _Skip("still-in-inventory", mention.written)
        kind: ChangeKind = (
            mention.kind if mention.kind != "renamed" else ("deprecated" if present else "removed")
        )
        change = Change(
            symbol,
            kind,
            version,
            (source,),
            parameter=parameter,
            removal_planned=mention.planned,
        )
        if mention.new is None:
            return change, False
        replacement, known = self.replacement(mention.new, symbol, parameter)
        return replace(change, replacement=replacement), known and mention.new in citation
