"""Cross-checks K1–K7 (SPEC §6.5): comparisons of two sources; a contradiction is a `Finding`.

Only K5a (claim vs. claim within a chunk) exists so far. The others go here too and report in
the same `notinspec.findings.Finding` shape.
"""

from notinspec.crosscheck.k5a import (
    K5A_VERSION,
    PREFILTER_RULE,
    CheckedClaim,
    ClaimPair,
    K5aResult,
    K5aStatus,
    K5aVersions,
    Relation,
    check_claims_within_chunks,
    claim_ref,
    relation,
)

__all__ = [
    "K5A_VERSION",
    "PREFILTER_RULE",
    "CheckedClaim",
    "ClaimPair",
    "K5aResult",
    "K5aStatus",
    "K5aVersions",
    "Relation",
    "check_claims_within_chunks",
    "claim_ref",
    "relation",
]
