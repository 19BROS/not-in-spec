"""Cross-checks K1–K7 (SPEC §6.5): comparisons of two sources; a contradiction is a `Finding`.

So far K2 (claim vs. signature, `k2`) and K5a (claim vs. claim within a chunk, `k5a`). The
others go here too and report in the same `notinspec.findings.Finding` shape.
"""

from notinspec.crosscheck.k2 import (
    K2_VERSION,
    FactKind,
    FactPair,
    K2Result,
    K2Versions,
    SignatureFact,
    check_claims_against_signatures,
    check_documented_types,
    names_parameter,
    signature_facts,
    type_names,
)
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
    "K2_VERSION",
    "K5A_VERSION",
    "PREFILTER_RULE",
    "CheckedClaim",
    "ClaimPair",
    "FactKind",
    "FactPair",
    "K2Result",
    "K2Versions",
    "K5aResult",
    "K5aStatus",
    "K5aVersions",
    "Relation",
    "SignatureFact",
    "check_claims_against_signatures",
    "check_claims_within_chunks",
    "check_documented_types",
    "claim_ref",
    "names_parameter",
    "relation",
    "signature_facts",
    "type_names",
]
