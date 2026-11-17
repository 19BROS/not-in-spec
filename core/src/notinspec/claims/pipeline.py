"""The claim pipeline (SPEC §6.4 steps 1-2): extract, then ground every claim.

extract (each extractor) → citation check → NLI premise → NLI → identifier check. Every claim
comes out with a status, the dropped ones too, with what decided it:

- `citation_not_found`: the citation is not in the chunk;
- `not_checkable`: the citation is only outside prose (code, table, signature);
- `nli_neutral` / `nli_contradiction`: NLI did not find the claim in its premise;
- `id_missing`: NLI kept it, but the section never names an identifier, number or version of
  the claim (SPEC §18);
- `kept`: everything passed.

The identifier check runs on every claim that has a premise, also when NLI already dropped it,
so the two checks can be measured separately.

A citation that is in the prose more than once (a docstring repeats sentences across parameter
entries) has one premise per match. Matches inside a parameter entry whose name the claim uses
come first; among the rest, NLI decides: the premise with the highest entailment wins (on a tie,
the earlier one in the chunk). Pairs are scored in one batch.
"""

import re
from collections.abc import Callable, Sequence
from dataclasses import dataclass
from typing import Literal

from notinspec.chunking import CHUNKER_VERSION, WINDOWS_VERSION, Chunk
from notinspec.chunking.chunker import BREADCRUMB_SEPARATOR
from notinspec.claims.extract import extract_claims
from notinspec.claims.model import ExtractedClaim, ExtractionResult, ExtractorSpec
from notinspec.claims.store import CallLog, ClaimStore
from notinspec.grounding import (
    GROUNDING_VERSION,
    PREMISE_RULE,
    Premise,
    check_citation,
    inventory_names,
    missing_identifiers,
    nli_premise,
    section_reference,
)
from notinspec.inventory import Inventory
from notinspec.nli import DECISION_RULE, NliModel, NliScores
from notinspec.runner import ModelClient

type GroundingStatus = Literal[
    "kept",
    "citation_not_found",
    "not_checkable",
    "nli_neutral",
    "nli_contradiction",
    "id_missing",
]
STATUSES: tuple[GroundingStatus, ...] = (
    "kept",
    "citation_not_found",
    "not_checkable",
    "nli_neutral",
    "nli_contradiction",
    "id_missing",
)


@dataclass(frozen=True)
class GroundingVersions:
    """Everything a grounding decision depends on besides its input (SPEC §6.4)."""

    grounding: int  # GROUNDING_VERSION: citation normalization, premise, identifier rules
    premise_rule: str
    windows: int  # WINDOWS_VERSION: the sentence splitter the premise is cut with
    chunker: int  # CHUNKER_VERSION
    nli_model: str
    nli_revision: str
    decision_rule: str  # argmax

    @classmethod
    def of(cls, nli: NliModel) -> "GroundingVersions":
        return cls(
            grounding=GROUNDING_VERSION,
            premise_rule=PREMISE_RULE,
            windows=WINDOWS_VERSION,
            chunker=CHUNKER_VERSION,
            nli_model=nli.model_id,
            nli_revision=nli.revision,
            decision_rule=DECISION_RULE,
        )


@dataclass(frozen=True)
class GroundedClaim:
    claim: ExtractedClaim
    prompt_version: int  # of the extractor that produced the claim
    status: GroundingStatus
    citation_span: tuple[int, int] | None  # the match the premise was built on; offsets in chunk
    citation_matches: int  # matches in prose (found) or outside it (not_checkable: 1)
    premise_candidates: int  # premises NLI chose from; 0 without a premise
    premise: str | None
    premise_span: tuple[int, int] | None
    nli: NliScores | None  # scores of the chosen premise; `truncated` says if it was cut
    missing: tuple[str, ...]  # identifiers, numbers, versions the section lacks; () = passes


@dataclass(frozen=True)
class ClaimsRun:
    results: tuple[ExtractionResult, ...]
    claims: tuple[GroundedClaim, ...]  # extractor order, then chunk order, then answer order
    versions: GroundingVersions


def run_claims(
    chunks: Sequence[Chunk],
    specs: Sequence[ExtractorSpec],
    client: ModelClient,
    nli: NliModel,
    run_id: str,
    calls: CallLog,
    *,
    sections: Sequence[Chunk],
    inventory: Inventory,
    project: str,
    store: ClaimStore | None = None,
    reuse: bool = True,
    on_extracted: Callable[[ExtractionResult], None] | None = None,
) -> ClaimsRun:
    """Extracts claims from `chunks` and grounds them.

    `sections` are all chunks of the docs, so a section split into parts is checked whole by
    the identifier check even when only some of its parts are extracted.
    """
    results: list[ExtractionResult] = []
    for spec in specs:
        result = extract_claims(chunks, spec, client, run_id, calls, store=store, reuse=reuse)
        results.append(result)
        if on_extracted is not None:
            on_extracted(result)
    grounded = ground_claims(results, sections, inventory, nli, project=project)
    return ClaimsRun(tuple(results), grounded, GroundingVersions.of(nli))


@dataclass
class _Pending:
    claim: ExtractedClaim
    prompt_version: int
    chunk: Chunk
    matches: int
    candidates: list[tuple[tuple[int, int], Premise]]  # (citation span, premise)
    missing: tuple[str, ...]


def ground_claims(
    results: Sequence[ExtractionResult],
    chunks: Sequence[Chunk],
    inventory: Inventory,
    nli: NliModel,
    *,
    project: str,
) -> tuple[GroundedClaim, ...]:
    by_id = {c.id: c for c in chunks}
    by_section: dict[str, list[Chunk]] = {}
    for chunk in chunks:
        by_section.setdefault(chunk.section_id, []).append(chunk)
    references: dict[str, str] = {}
    names = inventory_names(inventory)

    out: list[GroundedClaim | _Pending] = []
    for result in results:
        version = result.extractor.prompt_version
        for claim in result.claims:
            chunk = by_id[claim.chunk_id]
            check = check_citation(chunk, claim.citation)
            if check.status != "found":
                status: GroundingStatus = (
                    "not_checkable" if check.status == "not_checkable" else "citation_not_found"
                )
                out.append(_unchecked(claim, version, status, check.span, len(check.spans)))
                continue
            if chunk.section_id not in references:
                references[chunk.section_id] = section_reference(
                    by_section[chunk.section_id], inventory
                )
            missing = missing_identifiers(
                claim.text, references[chunk.section_id], project=project, known_names=names
            )
            candidates = _candidates(chunk, claim.text, check.spans)
            out.append(_Pending(claim, version, chunk, len(check.spans), candidates, missing))

    pairs = list(
        dict.fromkeys(
            (premise.text, p.claim.text)
            for p in out
            if isinstance(p, _Pending)
            for _, premise in p.candidates
        )
    )
    scores = dict(zip(pairs, nli.score(pairs), strict=True)) if pairs else {}
    return tuple(_decide(p, scores) if isinstance(p, _Pending) else p for p in out)


def _unchecked(
    claim: ExtractedClaim,
    version: int,
    status: GroundingStatus,
    span: tuple[int, int] | None,
    matches: int,
) -> GroundedClaim:
    return GroundedClaim(
        claim=claim,
        prompt_version=version,
        status=status,
        citation_span=span,
        citation_matches=matches,
        premise_candidates=0,
        premise=None,
        premise_span=None,
        nli=None,
        missing=(),
    )


def _candidates(
    chunk: Chunk, claim: str, spans: Sequence[tuple[int, int]]
) -> list[tuple[tuple[int, int], Premise]]:
    """One premise per match (the same premise once); parameter entries the claim names first."""
    seen: set[str] = set()
    premises: list[tuple[tuple[int, int], Premise]] = []
    for span in spans:
        premise = nli_premise(chunk, span)
        if premise.text not in seen:
            seen.add(premise.text)
            premises.append((span, premise))
    named = [
        (span, premise)
        for span, premise in premises
        if (param := _parameter(chunk, premise)) is not None
        and re.search(rf"(?<!\w){re.escape(param)}(?!\w)", claim)
    ]
    return named or premises


def _parameter(chunk: Chunk, premise: Premise) -> str | None:
    """The parameter a premise's breadcrumb names (`... > Retry > total: ...`), if any."""
    head = f"{chunk.breadcrumb}{BREADCRUMB_SEPARATOR}"
    if not premise.text.startswith(head):
        return None
    rest = premise.text[len(head) :]
    name, sep, _ = rest.partition(": ")
    return name if sep and name and BREADCRUMB_SEPARATOR not in name else None


def _decide(pending: _Pending, scores: dict[tuple[str, str], NliScores]) -> GroundedClaim:
    best = max(
        pending.candidates,
        key=lambda c: scores[(c[1].text, pending.claim.text)].entailment,
    )  # max keeps the first of equal ones, i.e. the earlier match in the chunk
    span, premise = best
    nli = scores[(premise.text, pending.claim.text)]
    status: GroundingStatus
    if nli.label != "entailment":
        status = "nli_neutral" if nli.label == "neutral" else "nli_contradiction"
    elif pending.missing:
        status = "id_missing"
    else:
        status = "kept"
    return GroundedClaim(
        claim=pending.claim,
        prompt_version=pending.prompt_version,
        status=status,
        citation_span=span,
        citation_matches=pending.matches,
        premise_candidates=len(pending.candidates),
        premise=premise.text,
        premise_span=premise.span,
        nli=nli,
        missing=pending.missing,
    )
