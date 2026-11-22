"""K5a on real claims of run 009 (4 urllib3 chunks) with their real, recorded NLI scores."""

from collections import Counter

import pytest

from notinspec.chunking import Chunk
from notinspec.claims import GroundedClaim
from notinspec.crosscheck import K5aResult, check_claims_within_chunks
from notinspec.nli import RecordedNli

QWEN, GEMMA = "qwen3.8-flash-next", "gemma4-26b-a4b-hpc"
MAKING_REQUESTS = "4b106715a267e6e4"


@pytest.fixture
def result(
    run009_claims: list[GroundedClaim], urllib3_chunks: list[Chunk], run009_nli: RecordedNli
) -> K5aResult:
    return check_claims_within_chunks(run009_claims, urllib3_chunks, run009_nli)


def _by_text(result: K5aResult, extractor: str, text: str) -> str:
    (ref,) = [
        c.ref
        for c in result.claims
        if c.claim.claim.extractor == extractor and c.claim.claim.text == text
    ]
    return ref


def test_counts(run009_claims: list[GroundedClaim], result: K5aResult) -> None:
    assert len(run009_claims) == 64
    assert len(result.claims) == sum(c.status == "kept" for c in run009_claims) == 63
    assert Counter(p.relation for p in result.pairs) == {
        "different": 61,
        "duplicate": 22,
        "a_more_specific": 9,
        "contradiction": 7,
        "b_more_specific": 2,
    }
    assert Counter(c.status for c in result.claims) == {
        "kept": 27,
        "merged": 14,
        "contradicted": 14,
        "covered": 8,
    }
    assert len(result.findings) == 4


def test_gemma_duplicates_merge_into_qwen(result: K5aResult) -> None:
    by_ref = {c.ref: c for c in result.claims}
    merged = by_ref[_by_text(result, GEMMA, "The request() method returns a HTTPResponse object.")]
    kept = by_ref[_by_text(result, QWEN, "The request() method returns a HTTPResponse object.")]
    assert (merged.status, merged.into) == ("merged", kept.ref)
    assert (kept.status, kept.confirmed_by) == ("kept", (QWEN, GEMMA))


def test_the_claim_that_names_its_subject_covers_the_other(result: K5aResult) -> None:
    by_ref = {c.ref: c for c in result.claims}
    covered = by_ref[_by_text(result, GEMMA, "System CA certificates are loaded on default.")]
    assert covered.status == "covered"
    assert by_ref[covered.into or ""].claim.claim.text == (
        "System CA certificates are loaded on default for urllib3.request()."
    )


def test_findings_are_false_contradictions_with_low_confidence(result: K5aResult) -> None:
    """What K5a reports on these chunks: items of one list and before / after, no real error."""
    subjects = {f.subject.rsplit(" > ", 1)[1]: f for f in result.findings}
    assert set(subjects) == {
        "Making Requests",
        "Certificate verification via SSLContext",
        "parse_url()",
        "✨ Optimized for Python 3.10+",
    }
    assert {f.confidence for f in result.findings} == {"low"}
    # "handles all of the details of connection pooling and thread safety": both extractors
    # split it in two, which is two contradiction pairs but one finding
    pooling = subjects["Making Requests"]
    assert Counter(e.text for e in pooling.evidence) == {
        "The PoolManager object handles connection pooling details.": 2,
        "The PoolManager object handles thread safety details.": 2,
    }
    assert {e.chunk_id for e in pooling.evidence} == {MAKING_REQUESTS}
    assert len(pooling.nli) == 4 and all(n.scores.label == "contradiction" for n in pooling.nli)
    python = subjects["✨ Optimized for Python 3.10+"]
    assert {e.text for e in python.evidence} == {
        "urllib3 2.x specifically targets CPython 3.10+.",
        "urllib3 2.x specifically targets PyPy v7.3.20+.",
    }


def test_same_input_same_result(
    run009_claims: list[GroundedClaim],
    urllib3_chunks: list[Chunk],
    run009_nli: RecordedNli,
    result: K5aResult,
) -> None:
    again = check_claims_within_chunks(run009_claims, urllib3_chunks, run009_nli)
    assert again == result
    assert [f.key for f in again.findings] == [f.key for f in result.findings]
