"""`Finding`: a problem in the documentation, reported to the docs author (SPEC §4, §6.5).

Every cross-check (K1–K7) reports what it finds in this one shape, so the report, the PR
comment and later the database read findings without knowing which check made them:

- `evidence`: the sides that were compared (two claims, a claim and a signature, a call record
  and a `Change`), each with where it is in the docs and the docs text the author can search for;
- `nli`: the NLI scores behind the decision, for checks that use NLI (K2, K5);
- `confidence`: how far the finding can be trusted without a person looking at it. A
  deterministic check (K1, K4, K7) is `high`. An NLI check is `low`: on urllib3 (run 009)
  none of the K5a contradictions read by eye was one in the docs (two items of one list,
  "previously" vs "now"), so `low` findings go to review by our team (SPEC §2.5) and are not
  shown to the author or used to fail CI until then;
- `key`: identity across runs, so a PR can tell a new finding from one the baseline already
  has (SPEC §7). It is built from the docs text the evidence quotes, not from claim IDs or
  claim wording, which change whenever an extractor reads the chunk again.

Pure: same arguments in any order of `evidence` and `nli` ⇒ equal finding, same `key`.
"""

from dataclasses import dataclass, field
from typing import Literal

from notinspec.adapters.canonical import content_hash
from notinspec.grounding import normalize
from notinspec.inventory.objects import Confidence
from notinspec.nli import NliScores

type Check = Literal["K1", "K2", "K3", "K4", "K5a", "K5b", "K6", "K7"]
# what is wrong; checks add their kinds here ("unknown-parameter" for K1, "removed-symbol" for K4)
type FindingKind = Literal["contradiction"]
type EvidenceKind = Literal[
    "claim", "signature", "parameter", "constraint", "change", "call_record", "example"
]


@dataclass(frozen=True)
class Evidence:
    """One side of a comparison."""

    kind: EvidenceKind
    # stable ID of the object: a claim "<chunk_id>/<extractor>/<local_id>", a symbol path,
    # an example ID
    ref: str
    text: str  # what this side says: the claim, the rendered signature, the call
    # `Chunk.section_id`, as in `Source`: None only for a formal spec fact (then `pointer`)
    section_id: str | None
    pointer: str | None = None  # formal spec: JSON pointer ("/paths/~1orders/post")
    chunk_id: str | None = None
    # the docs text the author can find: the claim's citation, the signature line, the code
    quote: str | None = None
    span: tuple[int, int] | None = None  # offsets of `quote` in the chunk's text

    def __post_init__(self) -> None:
        if not self.ref:
            raise ValueError("evidence needs a ref")
        if self.section_id is None and self.pointer is None:
            raise ValueError(f"evidence {self.ref} needs a section_id or a pointer")


@dataclass(frozen=True)
class NliEvidence:
    """One NLI decision a finding rests on; premise and hypothesis are `Evidence.ref`s."""

    premise: str
    hypothesis: str
    scores: NliScores


@dataclass(frozen=True)
class Finding:
    check: Check
    kind: FindingKind
    subject: str  # what it is about: a symbol path, or the section's breadcrumb (K5)
    message: str  # one line from a template in code, never written by an LLM
    confidence: Confidence
    evidence: tuple[Evidence, ...]  # sorted by place in the docs, then ref; no two with one ref
    nli: tuple[NliEvidence, ...] = ()  # sorted by (premise, hypothesis)
    # what the decision depends on besides its input: the check's version, its prefilter, the
    # NLI model and revision, the decision rule; sorted by name
    versions: tuple[tuple[str, str], ...] = ()
    key: str = field(init=False)

    def __post_init__(self) -> None:
        if not self.evidence:
            raise ValueError("a finding needs evidence")
        evidence = tuple(sorted(self.evidence, key=_place))
        refs = [e.ref for e in evidence]
        if len(set(refs)) != len(refs):
            raise ValueError(f"evidence refs repeat: {refs}")
        for n in self.nli:
            if n.premise not in refs or n.hypothesis not in refs:
                raise ValueError(f"NLI evidence {n.premise} ⇒ {n.hypothesis} is not in evidence")
        object.__setattr__(self, "evidence", evidence)
        object.__setattr__(
            self, "nli", tuple(sorted(self.nli, key=lambda n: (n.premise, n.hypothesis)))
        )
        object.__setattr__(self, "versions", tuple(sorted(self.versions)))
        object.__setattr__(self, "key", finding_key(self.check, self.kind, evidence))


def finding_key(check: Check, kind: FindingKind, evidence: tuple[Evidence, ...]) -> str:
    """sha256 of the check, the kind and where each side is in the docs and what it quotes.

    A quote is compared as the citation check normalizes it (whitespace, markup, typographic
    quotes), so reformatting the docs keeps the key. Evidence without a quote uses its ref.
    Two findings with one key are the same problem in the docs. Sides that quote the same text
    count once: whether one extractor or both made a claim from that sentence does not change
    the key. Full stops, commas, semicolons, colons and spaces at the end of a quote are
    ignored, so a sentence quoted with or without its final punctuation is the same side.
    """
    sides = sorted(
        {
            (e.section_id or "", e.pointer or "", e.kind, _quoted(e.quote) if e.quote else e.ref)
            for e in evidence
        }
    )
    return content_hash({"check": check, "kind": kind, "sides": sides})


def _quoted(quote: str) -> str:
    return normalize(quote).rstrip(" .,;:")


def _place(e: Evidence) -> tuple[str, str, str, tuple[int, int], str]:
    return (e.section_id or "", e.pointer or "", e.chunk_id or "", e.span or (-1, -1), e.ref)
