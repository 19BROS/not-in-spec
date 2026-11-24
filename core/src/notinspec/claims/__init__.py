"""Claims from prose and changelog (SPEC §6.4): the LLM claim extractor and the pipeline.

`extract_claims` extracts claims with their citations. `ground_claims` grounds them (citation
check, NLI premise, NLI, identifier check, from `notinspec.grounding` and `notinspec.nli`), and
`run_claims` does both. `changes_from_claims` turns kept *change* claims into `Change`
candidates for review (SPEC §6.3).
"""

from notinspec.claims.changes import (
    CHANGE_RULES_VERSION,
    ChangeCandidate,
    ChangeClaims,
    ClaimRef,
    SkippedChangeClaim,
    changes_from_claims,
)
from notinspec.claims.extract import ROLE, extract_claims
from notinspec.claims.model import (
    DEFAULT_EXTRACTORS,
    GROQ_EXTRACTORS,
    PROMPT_VERSION,
    ClaimType,
    ExtractedClaim,
    ExtractionCause,
    ExtractionFailure,
    ExtractionProblem,
    ExtractionResult,
    ExtractorSpec,
    RawClaim,
    extractor_for,
)
from notinspec.claims.parse import ParsedClaims, parse_claims
from notinspec.claims.pipeline import (
    STATUSES,
    ClaimsRun,
    GroundedClaim,
    GroundingStatus,
    GroundingVersions,
    ground_claims,
    run_claims,
)
from notinspec.claims.prompt import CLAIMS_SCHEMA, build_request, render_prompt
from notinspec.claims.store import (
    CallLog,
    ClaimStore,
    JsonlCallLog,
    JsonlClaimStore,
    LlmCall,
    MemoryCallLog,
    MemoryClaimStore,
    ReuseKey,
    StoredAnswer,
)

__all__ = [
    "CHANGE_RULES_VERSION",
    "CLAIMS_SCHEMA",
    "DEFAULT_EXTRACTORS",
    "GROQ_EXTRACTORS",
    "PROMPT_VERSION",
    "ROLE",
    "STATUSES",
    "CallLog",
    "ChangeCandidate",
    "ChangeClaims",
    "ClaimRef",
    "ClaimStore",
    "SkippedChangeClaim",
    "changes_from_claims",
    "ClaimsRun",
    "ClaimType",
    "ExtractedClaim",
    "ExtractionCause",
    "ExtractionFailure",
    "ExtractionProblem",
    "ExtractionResult",
    "ExtractorSpec",
    "GroundedClaim",
    "GroundingStatus",
    "GroundingVersions",
    "JsonlCallLog",
    "JsonlClaimStore",
    "LlmCall",
    "MemoryCallLog",
    "MemoryClaimStore",
    "ParsedClaims",
    "RawClaim",
    "ReuseKey",
    "StoredAnswer",
    "build_request",
    "extract_claims",
    "extractor_for",
    "ground_claims",
    "parse_claims",
    "render_prompt",
    "run_claims",
]
