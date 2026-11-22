"""K5a · claim vs. claim within a chunk (SPEC §6.4 step 3, §6.5).

The two extractors read the same chunk, so many of their claims say the same thing. K5a
compares the kept claims of different extractors in one chunk with NLI in both directions
(premise = one claim, hypothesis = the other) and decides by argmax, as grounding does:

| A ⇒ B         | B ⇒ A         | relation          | status                        |
|---------------|---------------|-------------------|-------------------------------|
| contradiction | contradiction | contradiction     | both `contradicted`, `Finding`|
| entailment    | entailment    | duplicate         | one kept, the others `merged` |
| entailment    | other         | A is more specific| B `covered` by A              |
| other         | other         | different         | both kept                     |

A contradiction needs both directions. On urllib3 (run 009, 853 kept claims) NLI labelled 264
of 6 835 claim pairs a contradiction in at least one direction and 34 in both. One reader went
through all 34 and about 60 of the one-way ones (not labels): none was a contradiction in the
docs. They were items of one list ("targets CPython 3.10+" vs "targets PyPy v7.3.20+") or
before and after ("Previously … a PoolManager" vs "added a top-level function"). The only real
error among them was one way: gemma's "compatible with CPython 3.11" (the docs say it of PyPy),
an extraction error, not one in the docs. So a K5a finding has `low` confidence and goes to
review.

**Prefilter:** only claims whose NLI premises overlap in the chunk are compared (the cited
sentence ±1, SPEC §6.1). On run 009 that is 1 385 of 6 835 pairs, and it missed 8 of 135
duplicates. A whole section can yield 60 claims per extractor, which is 3 600 pairs. K5b
(across chunks) needs embeddings instead; K5a may move to them when they exist.

**Resolution**, in this order, so the result never depends on the order of the pairs:

1. a claim in a contradiction is `contradicted`: no tasks are made from it (SPEC §6.4);
2. the other claims are grouped by duplicate pairs (transitively). A chain of one-way
   entailments that leads back to its start (A ⇒ B ⇒ C ⇒ A) says the claims are equivalent,
   so it joins one group too. The group's representative is the claim of the earliest
   extractor, then the earliest in the input; the rest are `merged` into it;
3. a group is `covered` when a claim of another group entails one of its claims and not the
   other way round (the more specific claim keeps the fact). Groups at the top of these chains
   are never covered, so no fact is lost. `into` names a more specific representative.

**Findings:** one per problem in the docs, not per pair. Contradiction pairs that share a
claim, whose claims are duplicates of each other, or that quote the same docs text are one
`Finding`: qwen and gemma both split `PoolManager`'s "handles all of the details of connection
pooling and thread safety" into two claims, which gives two contradiction pairs and one finding.

Only `kept` claims become test material. A `merged` or `covered` claim points to its
representative or to the more specific claim with `into` (follow it to reach a kept claim).
"""

from collections import defaultdict
from collections.abc import Sequence
from dataclasses import dataclass
from typing import Literal

from notinspec.chunking import Chunk
from notinspec.claims import GroundedClaim
from notinspec.findings import Evidence, Finding, NliEvidence, finding_key
from notinspec.nli import DECISION_RULE, NliModel, NliScores

# bump when a result can change for the same claims and scores (rule, prefilter, resolution)
K5A_VERSION = 1
PREFILTER_RULE = "premise-overlap"

type Relation = Literal[
    "duplicate", "a_more_specific", "b_more_specific", "different", "contradiction"
]
type K5aStatus = Literal["kept", "merged", "covered", "contradicted"]


@dataclass(frozen=True)
class ClaimPair:
    """Two claims of different extractors in one chunk; `a` comes earlier in the input."""

    a: str  # claim_ref
    b: str
    a_to_b: NliScores  # premise a, hypothesis b
    b_to_a: NliScores
    relation: Relation


@dataclass(frozen=True)
class CheckedClaim:
    claim: GroundedClaim
    ref: str  # claim_ref(claim)
    status: K5aStatus
    # merged: the representative of its group; covered: the representative of a more specific
    # group; None for kept and contradicted
    into: str | None
    # kept: the extractors whose claims merged into this one, its own first; () otherwise
    confirmed_by: tuple[str, ...]


@dataclass(frozen=True)
class K5aVersions:
    check: int  # K5A_VERSION
    prefilter: str
    nli_model: str
    nli_revision: str
    decision_rule: str

    def pairs(self) -> tuple[tuple[str, str], ...]:
        return (
            ("decision_rule", self.decision_rule),
            ("k5a", str(self.check)),
            ("nli_model", self.nli_model),
            ("nli_revision", self.nli_revision),
            ("prefilter", self.prefilter),
        )


@dataclass(frozen=True)
class K5aResult:
    claims: tuple[CheckedClaim, ...]  # the kept claims of the input, in input order
    pairs: tuple[ClaimPair, ...]  # chunk order, then the input order of `a`, then of `b`
    findings: tuple[Finding, ...]  # sorted by key
    versions: K5aVersions


def claim_ref(claim: GroundedClaim) -> str:
    c = claim.claim
    return f"{c.chunk_id}/{c.extractor}/{c.local_id}"


def relation(a_to_b: NliScores, b_to_a: NliScores) -> Relation:
    """The relation of two claims from the NLI scores of both directions (argmax)."""
    ab, ba = a_to_b.label, b_to_a.label
    if ab == ba == "contradiction":
        return "contradiction"
    if ab == ba == "entailment":
        return "duplicate"
    if ab == "entailment":
        return "a_more_specific"
    if ba == "entailment":
        return "b_more_specific"
    return "different"


def check_claims_within_chunks(
    claims: Sequence[GroundedClaim], chunks: Sequence[Chunk], nli: NliModel
) -> K5aResult:
    """K5a on the `kept` claims of `claims` (other statuses are ignored).

    `chunks` must contain the chunk of every kept claim. Extractors rank in the order they
    first appear in `claims` (`ClaimsRun.claims` is in extractor order).
    """
    kept = [c for c in claims if c.status == "kept"]
    refs = [claim_ref(c) for c in kept]
    if len(set(refs)) != len(refs):
        raise ValueError("two kept claims have the same chunk, extractor and local id")
    by_id = {c.id: c for c in chunks}
    rank = {e: i for i, e in enumerate(dict.fromkeys(c.claim.extractor for c in kept))}

    by_chunk: dict[str, list[int]] = defaultdict(list)
    for i, c in enumerate(kept):
        if c.claim.chunk_id not in by_id:
            raise ValueError(f"claim {refs[i]} is in chunk {c.claim.chunk_id}, not in `chunks`")
        if c.premise_span is None:
            raise ValueError(f"kept claim {refs[i]} has no premise")
        by_chunk[c.claim.chunk_id].append(i)

    candidates = [
        (i, j)
        for members in by_chunk.values()
        for x, i in enumerate(members)
        for j in members[x + 1 :]
        if kept[i].claim.extractor != kept[j].claim.extractor
        and _overlap(kept[i].premise_span, kept[j].premise_span)
    ]
    texts: list[tuple[str, str]] = []
    for i, j in candidates:
        a, b = kept[i].claim.text, kept[j].claim.text
        texts += [(a, b), (b, a)]
    texts = list(dict.fromkeys(texts))  # one batch, each ordered pair once
    scores = dict(zip(texts, nli.score(texts), strict=True)) if texts else {}
    pairs = [
        _pair(refs[i], refs[j], scores[(a, b)], scores[(b, a)])
        for i, j in candidates
        for a, b in [(kept[i].claim.text, kept[j].claim.text)]
    ]

    statuses = _resolve(kept, refs, rank, candidates, pairs)
    versions = K5aVersions(K5A_VERSION, PREFILTER_RULE, nli.model_id, nli.revision, DECISION_RULE)
    findings = _findings(kept, refs, by_id, candidates, pairs, versions)
    return K5aResult(statuses, tuple(pairs), findings, versions)


def _overlap(a: tuple[int, int] | None, b: tuple[int, int] | None) -> bool:
    return a is not None and b is not None and a[0] < b[1] and b[0] < a[1]


def _pair(a: str, b: str, a_to_b: NliScores, b_to_a: NliScores) -> ClaimPair:
    return ClaimPair(a, b, a_to_b, b_to_a, relation(a_to_b, b_to_a))


def _resolve(
    kept: Sequence[GroundedClaim],
    refs: Sequence[str],
    rank: dict[str, int],
    candidates: Sequence[tuple[int, int]],
    pairs: Sequence[ClaimPair],
) -> tuple[CheckedClaim, ...]:
    contradicted = {
        k
        for (i, j), p in zip(candidates, pairs, strict=True)
        if p.relation == "contradiction"
        for k in (i, j)
    }
    parent = list(range(len(kept)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        parent[find(x)] = find(y)

    specific: list[tuple[int, int]] = []  # (more specific, covered)
    for (i, j), p in zip(candidates, pairs, strict=True):
        if i in contradicted or j in contradicted:
            continue
        if p.relation == "duplicate":
            union(i, j)
        elif p.relation == "a_more_specific":
            specific.append((i, j))
        elif p.relation == "b_more_specific":
            specific.append((j, i))

    # a cycle of one-way entailments between groups means they are equivalent: one group
    reach = _reachability({(find(s), find(c)) for s, c in specific if find(s) != find(c)})
    for g, targets in reach.items():
        for t in targets:
            if g in reach.get(t, set()):
                union(g, t)
    edges = {(find(s), find(c)) for s, c in specific if find(s) != find(c)}

    order = sorted(range(len(kept)), key=lambda i: (rank[kept[i].claim.extractor], i))
    position = {i: n for n, i in enumerate(order)}
    representative: dict[int, int] = {}
    for i in order:
        if i not in contradicted:
            representative.setdefault(find(i), i)
    covering: dict[int, int] = {}  # covered group → representative of a more specific group
    for s, c in sorted(
        edges, key=lambda e: (position[representative[e[0]]], position[representative[e[1]]])
    ):
        covering.setdefault(c, representative[s])
    members: dict[int, list[str]] = defaultdict(list)
    for i in order:
        if i not in contradicted:
            members[find(i)].append(kept[i].claim.extractor)

    out: list[CheckedClaim] = []
    for i, claim in enumerate(kept):
        if i in contradicted:
            out.append(CheckedClaim(claim, refs[i], "contradicted", None, ()))
            continue
        group = find(i)
        if representative[group] != i:
            out.append(CheckedClaim(claim, refs[i], "merged", refs[representative[group]], ()))
        elif group in covering:
            out.append(CheckedClaim(claim, refs[i], "covered", refs[covering[group]], ()))
        else:
            confirmed = tuple(dict.fromkeys(members[group]))
            out.append(CheckedClaim(claim, refs[i], "kept", None, confirmed))
    return tuple(out)


def _reachability(edges: set[tuple[int, int]]) -> dict[int, set[int]]:
    graph: dict[int, set[int]] = defaultdict(set)
    for s, t in edges:
        graph[s].add(t)
    reach: dict[int, set[int]] = {}
    for start in graph:
        seen: set[int] = set()
        stack = list(graph[start])
        while stack:
            node = stack.pop()
            if node not in seen:
                seen.add(node)
                stack.extend(graph.get(node, ()))
        reach[start] = seen
    return reach


def _findings(
    kept: Sequence[GroundedClaim],
    refs: Sequence[str],
    by_id: dict[str, Chunk],
    candidates: Sequence[tuple[int, int]],
    pairs: Sequence[ClaimPair],
    versions: K5aVersions,
) -> tuple[Finding, ...]:
    """One finding per problem in the docs, not per pair of claims.

    Contradiction pairs join one finding when they share a claim, when their claims are
    duplicates of each other (qwen and gemma both write "handles thread safety" and "handles
    connection pooling"), or when they quote the same docs text (the same `Finding.key`).
    """
    contradictions = [
        (i, j, p) for (i, j), p in zip(candidates, pairs, strict=True)
        if p.relation == "contradiction"
    ]  # fmt: skip
    involved = {k for i, j, _ in contradictions for k in (i, j)}
    parent = {k: k for k in involved}

    def find(x: int) -> int:
        while parent[x] != x:
            x = parent[x]
        return x

    def union(x: int, y: int) -> None:
        a, b = find(x), find(y)
        if a != b:
            parent[max(a, b)] = min(a, b)

    by_key: dict[str, int] = {}

    def evidence(k: int) -> Evidence:
        return _evidence(kept[k], refs[k], by_id[kept[k].claim.chunk_id])

    for i, j, _ in contradictions:
        union(i, j)
        key = finding_key("K5a", "contradiction", (evidence(i), evidence(j)))
        union(i, by_key.setdefault(key, i))
    for (i, j), p in zip(candidates, pairs, strict=True):
        if p.relation == "duplicate" and i in involved and j in involved:
            union(i, j)

    components: dict[int, list[tuple[int, int, ClaimPair]]] = defaultdict(list)
    for i, j, p in contradictions:
        components[find(i)].append((i, j, p))
    findings = []
    for root, members in components.items():
        # parts of one section share its breadcrumb, so the root's chunk names the subject
        chunk = by_id[kept[root].claim.chunk_id]
        claims = sorted(k for k in involved if find(k) == root)
        first = members[0][2]
        more = len(claims) - 2
        texts = {refs[k]: kept[k].claim.text for k in claims}
        findings.append(
            Finding(
                check="K5a",
                kind="contradiction",
                subject=chunk.breadcrumb,
                message=(
                    f"claims of this section contradict each other: “{texts[first.a]}” vs "
                    f"“{texts[first.b]}”" + (f" (+{more} more claims)" if more > 0 else "")
                ),
                confidence="low",
                evidence=tuple(evidence(k) for k in claims),
                nli=tuple(
                    n
                    for _, _, p in members
                    for n in (NliEvidence(p.a, p.b, p.a_to_b), NliEvidence(p.b, p.a, p.b_to_a))
                ),  # fmt: skip
                versions=versions.pairs(),
            )
        )
    return tuple(sorted(findings, key=lambda f: f.key))


def _evidence(claim: GroundedClaim, ref: str, chunk: Chunk) -> Evidence:
    return Evidence(
        kind="claim",
        ref=ref,
        text=claim.claim.text,
        section_id=chunk.section_id,
        chunk_id=chunk.id,
        quote=claim.claim.citation,
        span=claim.citation_span,
    )
