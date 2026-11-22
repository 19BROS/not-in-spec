"""K5a with hand-made NLI scores: every row of the SPEC §6.4 table, prefilter, resolution."""

from dataclasses import replace

import pytest

from notinspec.chunking import Chunk, Document, chunk_document
from notinspec.claims import ExtractedClaim, GroundedClaim
from notinspec.crosscheck import (
    K5A_VERSION,
    PREFILTER_RULE,
    check_claims_within_chunks,
    relation,
)
from notinspec.nli import MODEL_ID, REVISION, NliScores, RecordedNli

E = NliScores(0.9, 0.08, 0.02)
N = NliScores(0.1, 0.8, 0.1)
C = NliScores(0.02, 0.08, 0.9)

CHUNK = chunk_document(Document("docs/a.md", "# Retries\n\nSome text.\n"), project="acme")[0]
OTHER = chunk_document(Document("docs/b.md", "# Pools\n\nOther text.\n"), project="acme")[0]


def _claim(
    extractor: str,
    local_id: str,
    text: str,
    premise: tuple[int, int] = (0, 100),
    *,
    chunk: Chunk = CHUNK,
    status: str = "kept",
) -> GroundedClaim:
    return GroundedClaim(
        claim=ExtractedClaim(chunk.id, extractor, local_id, text, text, "fact", "r", "h", "m"),
        prompt_version=1,
        status=status,  # type: ignore[arg-type]
        citation_span=(premise[0], premise[0] + 5),
        citation_matches=1,
        premise_candidates=1,
        premise="premise",
        premise_span=premise,
        nli=E,
        missing=(),
    )


def _nli(scores: dict[tuple[str, str], NliScores]) -> RecordedNli:
    """Replays exactly these pairs; any other pair raises, so a pair outside the prefilter shows."""
    return RecordedNli({(MODEL_ID, REVISION, p, h): s for (p, h), s in scores.items()})


def _both(a: str, b: str, a_to_b: NliScores, b_to_a: NliScores) -> dict[tuple[str, str], NliScores]:
    return {(a, b): a_to_b, (b, a): b_to_a}


def _statuses(claims: list[GroundedClaim], nli: RecordedNli) -> dict[str, tuple[str, str | None]]:
    result = check_claims_within_chunks(claims, [CHUNK, OTHER], nli)
    return {
        c.ref.split("/", 1)[1]: (c.status, c.into and c.into.split("/", 1)[1])
        for c in result.claims
    }


@pytest.mark.parametrize(
    ("a_to_b", "b_to_a", "expected"),
    [
        (E, E, "duplicate"),
        (E, N, "a_more_specific"),
        (N, E, "b_more_specific"),
        (N, N, "different"),
        (C, C, "contradiction"),
        # a contradiction needs both directions (run 009: one direction alone was never real)
        (C, N, "different"),
        (N, C, "different"),
        (C, E, "b_more_specific"),
    ],
)
def test_relation_table(a_to_b: NliScores, b_to_a: NliScores, expected: str) -> None:
    assert relation(a_to_b, b_to_a) == expected


def test_duplicate_keeps_the_first_extractors_claim() -> None:
    a = _claim("qwen", "c1", "Retries default to 3.")
    b = _claim("gemma", "c1", "By default there are 3 retries.")
    result = check_claims_within_chunks(
        [a, b], [CHUNK], _nli(_both(a.claim.text, b.claim.text, E, E))
    )
    kept, merged = result.claims
    assert (kept.status, kept.into, kept.confirmed_by) == ("kept", None, ("qwen", "gemma"))
    assert (merged.status, merged.into, merged.confirmed_by) == ("merged", kept.ref, ())
    assert result.findings == ()
    assert result.versions.check == K5A_VERSION and result.versions.prefilter == PREFILTER_RULE
    assert (result.versions.nli_model, result.versions.decision_rule) == (MODEL_ID, "argmax")


def test_extractor_rank_beats_position_in_the_chunk() -> None:
    # gemma's claim comes first in the input only for its own chunk; qwen is the first extractor
    q1 = _claim("qwen", "c1", "Pools are cached.", chunk=OTHER)
    g1 = _claim("gemma", "c1", "Retries default to 3.")
    q2 = _claim("qwen", "c2", "By default there are 3 retries.")
    out = _statuses([q1, g1, q2], _nli(_both(g1.claim.text, q2.claim.text, E, E)))
    assert out["gemma/c1"] == ("merged", "qwen/c2")
    assert out["qwen/c2"] == ("kept", None)


def test_less_specific_claim_is_covered() -> None:
    a = _claim("qwen", "c1", "The total parameter of Retry caps all retries.")
    b = _claim("gemma", "c1", "The total parameter caps all retries.")
    out = _statuses([a, b], _nli(_both(a.claim.text, b.claim.text, E, N)))
    assert out == {"qwen/c1": ("kept", None), "gemma/c1": ("covered", "qwen/c1")}


def test_contradiction_blocks_both_claims_and_is_a_finding() -> None:
    a = _claim("qwen", "c1", "Retries default to 3.")
    b = _claim("gemma", "c1", "Retries default to 5.")
    result = check_claims_within_chunks(
        [a, b], [CHUNK], _nli(_both(a.claim.text, b.claim.text, C, C))
    )
    assert [c.status for c in result.claims] == ["contradicted", "contradicted"]
    (finding,) = result.findings
    assert (finding.check, finding.kind, finding.confidence) == ("K5a", "contradiction", "low")
    assert finding.subject == CHUNK.breadcrumb
    assert [e.ref for e in finding.evidence] == sorted(c.ref for c in result.claims)
    assert {e.section_id for e in finding.evidence} == {CHUNK.section_id}
    assert [(n.premise, n.hypothesis, n.scores) for n in finding.nli] == sorted(
        [
            (result.claims[0].ref, result.claims[1].ref, C),
            (result.claims[1].ref, result.claims[0].ref, C),
        ]
    )
    assert "“Retries default to 3.” vs “Retries default to 5.”" in finding.message
    assert dict(finding.versions)["k5a"] == str(K5A_VERSION)


def test_parts_of_one_section_keep_their_own_chunk_in_a_merged_finding() -> None:
    """A long section is split into parts with one section_id; a docstring sentence repeated in
    both parts gives two contradiction pairs with one key, so one finding. Each claim's
    evidence keeps the chunk its citation span is in."""
    part = replace(CHUNK, id=CHUNK.id + "-part2")
    a = _claim("qwen", "c1", "Retries default to 3.")
    b = _claim("gemma", "c1", "Retries default to 5.")
    c = _claim("qwen", "c1", "Retries default to 3.", chunk=part)
    d = _claim("gemma", "c1", "Retries default to 5.", chunk=part)
    result = check_claims_within_chunks(
        [a, b, c, d], [CHUNK, part], _nli(_both(a.claim.text, b.claim.text, C, C))
    )
    (finding,) = result.findings
    assert {(e.ref.split("/", 1)[0], e.chunk_id) for e in finding.evidence} == {
        (CHUNK.id, CHUNK.id),
        (part.id, part.id),
    }
    assert finding.subject == CHUNK.breadcrumb


def test_a_contradicted_claim_is_never_a_representative() -> None:
    # qwen/c1 is a duplicate of gemma/c1 but contradicts gemma/c2: gemma/c1 stays kept alone
    q = _claim("qwen", "c1", "Retries default to 3.")
    g1 = _claim("gemma", "c1", "There are 3 retries by default.")
    g2 = _claim("gemma", "c2", "Retries default to 5.")
    scores = _both(q.claim.text, g1.claim.text, E, E) | _both(q.claim.text, g2.claim.text, C, C)
    out = _statuses([q, g1, g2], _nli(scores))
    assert out == {
        "qwen/c1": ("contradicted", None),
        "gemma/c1": ("kept", None),
        "gemma/c2": ("contradicted", None),
    }


def test_duplicates_group_transitively() -> None:
    q1 = _claim("qwen", "c1", "Retries default to 3.")
    q2 = _claim("qwen", "c2", "The default number of retries is 3.")
    g = _claim("gemma", "c1", "By default there are 3 retries.")
    scores = _both(q1.claim.text, g.claim.text, E, E) | _both(q2.claim.text, g.claim.text, E, E)
    result = check_claims_within_chunks([q1, q2, g], [CHUNK], _nli(scores))
    out = {c.ref.split("/", 1)[1]: (c.status, c.confirmed_by) for c in result.claims}
    assert out == {
        "qwen/c1": ("kept", ("qwen", "gemma")),
        "qwen/c2": ("merged", ()),
        "gemma/c1": ("merged", ()),
    }


def test_a_cycle_of_one_way_entailments_is_one_group_and_loses_no_fact() -> None:
    # q1 ⇒ g1 ⇒ q2 ⇒ g2 ⇒ q1, never both ways: equivalent claims, so one of them stays
    q1, q2 = _claim("qwen", "c1", "q one."), _claim("qwen", "c2", "q two.")
    g1, g2 = _claim("gemma", "c1", "g one."), _claim("gemma", "c2", "g two.")
    t = {c: c.claim.text for c in (q1, q2, g1, g2)}
    scores = (
        _both(t[q1], t[g1], E, N) | _both(t[q2], t[g1], N, E)
        | _both(t[q2], t[g2], E, N) | _both(t[q1], t[g2], N, E)
    )  # fmt: skip
    out = _statuses([q1, q2, g1, g2], _nli(scores))
    assert out == {
        "qwen/c1": ("kept", None),
        "qwen/c2": ("merged", "qwen/c1"),
        "gemma/c1": ("merged", "qwen/c1"),
        "gemma/c2": ("merged", "qwen/c1"),
    }


def test_chain_of_more_specific_claims_keeps_the_top() -> None:
    q1 = _claim("qwen", "c1", "Retry(total=3) on urllib3 retries three times.")
    g = _claim("gemma", "c1", "Retry(total=3) retries three times.")
    q2 = _claim("qwen", "c2", "Retry can retry.")
    scores = _both(q1.claim.text, g.claim.text, E, N) | _both(q2.claim.text, g.claim.text, N, E)
    out = _statuses([q1, q2, g], _nli(scores))
    assert out == {
        "qwen/c1": ("kept", None),
        "qwen/c2": ("covered", "gemma/c1"),
        "gemma/c1": ("covered", "qwen/c1"),
    }


def test_prefilter_compares_only_other_extractors_with_overlapping_premises() -> None:
    claims = [
        _claim("qwen", "c1", "A.", (0, 50)),
        _claim("qwen", "c2", "B.", (40, 90)),  # same extractor as c1: never compared
        _claim("gemma", "c1", "C.", (45, 60)),  # overlaps both qwen claims
        _claim("gemma", "c2", "D.", (90, 120)),  # touches qwen/c2 at 90 but does not overlap
        _claim("gemma", "c3", "E.", (0, 50), chunk=OTHER),  # other chunk
        _claim("gemma", "c4", "F.", (0, 50), status="nli_neutral"),  # not kept
    ]
    nli = _nli(_both("A.", "C.", N, N) | _both("B.", "C.", N, N))
    result = check_claims_within_chunks(claims, [CHUNK, OTHER], nli)
    assert [(p.a.split("/", 1)[1], p.b.split("/", 1)[1]) for p in result.pairs] == [
        ("qwen/c1", "gemma/c1"),
        ("qwen/c2", "gemma/c1"),
    ]
    assert len(result.claims) == 5  # the dropped claim is not in the result
    assert {c.status for c in result.claims} == {"kept"}
    assert sorted(nli.calls) == sorted([("A.", "C."), ("C.", "A."), ("B.", "C."), ("C.", "B.")])


def test_no_pairs_no_nli_call() -> None:
    nli = _nli({})
    result = check_claims_within_chunks([_claim("qwen", "c1", "A.")], [CHUNK], nli)
    assert (result.pairs, result.findings, nli.calls) == ((), (), [])
    assert result.claims[0].confirmed_by == ("qwen",)


def test_bad_input_is_rejected() -> None:
    a = _claim("qwen", "c1", "A.")
    with pytest.raises(ValueError, match="same chunk, extractor and local id"):
        check_claims_within_chunks([a, a], [CHUNK], _nli({}))
    with pytest.raises(ValueError, match="not in `chunks`"):
        check_claims_within_chunks([a], [OTHER], _nli({}))
    no_premise = replace(a, premise_span=None)
    with pytest.raises(ValueError, match="no premise"):
        check_claims_within_chunks([no_premise], [CHUNK], _nli({}))
