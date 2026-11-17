"""Claims from prose and changelog (SPEC §6.4): the LLM claim extractor.

This package extracts claims with their citations. Grounding (citation check, NLI premise, NLI,
identifier check) is a separate step that consumes `ExtractedClaim`s.
"""

from notinspec.claims.extract import ROLE, extract_claims
from notinspec.claims.model import (
    DEFAULT_EXTRACTORS,
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
    "CLAIMS_SCHEMA",
    "DEFAULT_EXTRACTORS",
    "PROMPT_VERSION",
    "ROLE",
    "CallLog",
    "ClaimStore",
    "ClaimType",
    "ExtractedClaim",
    "ExtractionCause",
    "ExtractionFailure",
    "ExtractionProblem",
    "ExtractionResult",
    "ExtractorSpec",
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
    "parse_claims",
    "render_prompt",
]
