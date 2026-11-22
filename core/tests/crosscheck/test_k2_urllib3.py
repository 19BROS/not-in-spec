"""K2 on real claims of run 009 (6 urllib3 API descriptions) with their real, recorded NLI
scores, and the type check on the whole urllib3 docs."""

from collections import Counter

import pytest

from notinspec.chunking import Chunk
from notinspec.claims import GroundedClaim
from notinspec.crosscheck import (
    K2Result,
    check_claims_against_signatures,
    check_documented_types,
)
from notinspec.inventory import Inventory
from notinspec.nli import RecordedNli


@pytest.fixture
def result(
    run009_k2_claims: list[GroundedClaim],
    urllib3_chunks: list[Chunk],
    urllib3_inventory: Inventory,
    run009_k2_nli: RecordedNli,
) -> K2Result:
    return check_claims_against_signatures(
        run009_k2_claims, urllib3_chunks, urllib3_inventory, run009_k2_nli
    )


def test_counts(run009_k2_claims: list[GroundedClaim], result: K2Result) -> None:
    assert len(run009_k2_claims) == 89
    assert sum(c.status == "kept" for c in run009_k2_claims) == 87
    assert len(result.pairs) == 91
    assert sum(p.contradiction for p in result.pairs) == 6
    assert len(result.contradicted) == 6
    assert {f.confidence for f in result.findings} == {"low"}
    assert Counter(f.subject for f in result.findings) == {
        "urllib3.util.is_connection_dropped": 1,  # an error in the docs (issue #42)
        "urllib3.util.Timeout.connect_timeout": 1,  # `int` in the prose, not in the annotation
        "urllib3.util.create_urllib3_context": 1,  # false: "specifies OpenSSL options"
        "urllib3.util.Timeout.get_connect_duration": 1,  # false: "elapsed time in seconds"
    }


def test_the_error_in_the_docs_is_found_from_claim_to_fact(result: K2Result) -> None:
    """The prose says `urllib3.connection.HTTPConnection`, the parameter entry
    `BaseHTTPConnection`. NLI sees it only one way, which is why one direction is enough."""
    (finding,) = [f for f in result.findings if f.subject.endswith("is_connection_dropped")]
    fact, *claims = finding.evidence
    assert (fact.kind, fact.ref, fact.quote) == (
        "parameter",
        "urllib3.util.is_connection_dropped(conn).type",
        "conn (BaseHTTPConnection)",
    )
    # qwen and gemma quote the sentence differently; their citations overlap, so one finding
    assert {c.ref.split("/")[1] for c in claims} == {"qwen3.8-flash-next", "gemma4-26b-a4b-hpc"}
    labels = {(n.premise == fact.ref, n.scores.label) for n in finding.nli}
    assert labels == {(True, "neutral"), (False, "contradiction")}


def test_none_defaults_are_no_facts(result: K2Result) -> None:
    """create_urllib3_context's signature has `cert_reqs=None`, `options=None`, ...; its prose
    names the effective defaults ("defaults to `ssl.CERT_REQUIRED`"). That is no contradiction,
    and before this rule it gave most false findings on run 009."""
    context = [f for f in result.facts if f.symbol == "urllib3.util.create_urllib3_context"]
    assert {f.kind for f in context} == {"type", "returns"}
    defaults = [f for f in result.facts if f.kind == "default"]
    assert defaults and all(f.value != "None" for f in defaults)


def test_overloads_that_disagree_give_no_fact(result: K2Result) -> None:
    wrap = {f.ref for f in result.facts if f.symbol == "urllib3.util.ssl_wrap_socket"}
    assert "urllib3.util.ssl_wrap_socket(tls_in_tls).default" in wrap
    assert "urllib3.util.ssl_wrap_socket(tls_in_tls).type" not in wrap  # Literal[False] / bool
    assert "urllib3.util.ssl_wrap_socket.returns" not in wrap  # one return type per overload


def test_documented_types_on_all_of_urllib3(urllib3_chunks: list[Chunk]) -> None:
    """Both are errors in the docs: the annotation has no `int`, the `Return type` has.
    `ssl_wrap_socket` (`socket` vs `socket.socket`, `Literal[False]` / `bool` vs `bool`, two
    overloads vs one `Return type`) is not reported."""
    findings = check_documented_types(urllib3_chunks)
    assert {f.subject: f.message for f in findings} == {
        "urllib3.util.Timeout.read_timeout": (
            "urllib3.util.Timeout.read_timeout: the signature gives the type as "
            "`float | None`, the docs text as `int, float or None`"
        ),
        "urllib3.util.Timeout.connect_timeout": (
            "urllib3.util.Timeout.connect_timeout: the signature gives the type as "
            "`float | _TYPE_DEFAULT | None`, the docs text as "
            "`int, float, Timeout.DEFAULT_TIMEOUT or None`"
        ),
    }
    assert {(f.check, f.kind, f.confidence) for f in findings} == {
        ("K2", "type-mismatch", "medium")
    }


def test_same_input_same_result(
    run009_k2_claims: list[GroundedClaim],
    urllib3_chunks: list[Chunk],
    urllib3_inventory: Inventory,
    run009_k2_nli: RecordedNli,
    result: K2Result,
) -> None:
    again = check_claims_against_signatures(
        list(reversed(run009_k2_claims)), urllib3_chunks, urllib3_inventory, run009_k2_nli
    )
    assert again.findings == result.findings
    assert again.contradicted == result.contradicted
