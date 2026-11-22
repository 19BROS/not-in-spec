"""`Finding`: order-independent, validated, and a key that survives reformatting of the docs."""

from dataclasses import replace

import pytest

from notinspec.adapters.canonical import canonical_json
from notinspec.findings import Evidence, Finding, NliEvidence
from notinspec.nli import NliScores

A = Evidence(
    kind="claim",
    ref="c/x/c1",
    text="Retries default to 3.",
    section_id="s1",
    chunk_id="c",
    quote="The default is **3** retries.",
    span=(10, 39),
)
B = Evidence(
    kind="claim",
    ref="c/y/c4",
    text="Retries default to 5.",
    section_id="s1",
    chunk_id="c",
    quote="retries default to `5`",
    span=(50, 72),
)
CONTRA = NliScores(0.01, 0.04, 0.95)


def _finding(*evidence: Evidence, nli: tuple[NliEvidence, ...] = ()) -> Finding:
    return Finding(
        check="K5a",
        kind="contradiction",
        subject="acme > Retries",
        message="claims of this section contradict each other",
        confidence="low",
        evidence=evidence,
        nli=nli,
        versions=(("k5a", "1"), ("decision_rule", "argmax")),
    )


def test_order_of_evidence_and_nli_does_not_matter() -> None:
    ab, ba = NliEvidence(A.ref, B.ref, CONTRA), NliEvidence(B.ref, A.ref, CONTRA)
    one = _finding(A, B, nli=(ab, ba))
    other = _finding(B, A, nli=(ba, ab))
    assert one == other
    assert canonical_json(one) == canonical_json(other)
    assert one.evidence == (A, B)  # sorted by place in the docs
    assert one.versions == (("decision_rule", "argmax"), ("k5a", "1"))


def test_key_ignores_claim_ids_wording_and_markup() -> None:
    # an extractor that reads the chunk again writes other IDs and other words, and a
    # reformatted paragraph quotes the same text with other whitespace and markup
    again = replace(
        A, ref="c/x/c7", text="By default there are 3 retries.", quote="The default is 3\nretries."
    )
    assert _finding(again, B).key == _finding(A, B).key


def test_key_counts_claims_that_quote_the_same_text_once() -> None:
    # qwen and gemma both make a claim from one sentence; in the next run only qwen does
    gemma = replace(A, ref="c/z/c2", text="There are 3 retries by default.")
    assert _finding(A, gemma, B).key == _finding(A, B).key
    # the same sentence quoted without its full stop
    assert _finding(replace(A, quote="The default is 3 retries"), B).key == _finding(A, B).key


def test_key_changes_with_the_docs_text_the_section_or_the_check() -> None:
    key = _finding(A, B).key
    assert _finding(replace(A, quote="The default is 4 retries."), B).key != key
    assert _finding(replace(A, section_id="s2"), B).key != key
    assert replace(_finding(A, B), check="K5b").key != key
    assert len(key) == 64


def test_evidence_without_a_quote_is_keyed_by_its_ref() -> None:
    signature = Evidence("signature", "acme.Retry", "Retry(total=10)", section_id="s9")
    assert _finding(A, signature).key != _finding(A, replace(signature, ref="acme.Timeout")).key


def test_invalid_findings_are_rejected() -> None:
    with pytest.raises(ValueError, match="needs evidence"):
        _finding()
    with pytest.raises(ValueError, match="repeat"):
        _finding(A, replace(B, ref=A.ref))
    with pytest.raises(ValueError, match="not in evidence"):
        _finding(A, B, nli=(NliEvidence(A.ref, "c/z/c9", CONTRA),))
    with pytest.raises(ValueError, match="section_id or a pointer"):
        Evidence("signature", "acme.Retry", "Retry()", section_id=None)
    with pytest.raises(ValueError, match="needs a ref"):
        replace(A, ref="")
    # a formal spec fact sits outside any chunk
    assert Evidence("parameter", "POST /orders(id)", "id: int", None, pointer="/paths/~1orders")
