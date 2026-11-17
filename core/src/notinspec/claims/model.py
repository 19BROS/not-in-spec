"""What the claim extractor produces (SPEC §6.4 step 1), before any grounding."""

from dataclasses import dataclass
from typing import Literal

type ClaimType = Literal["fact", "change"]

# why a chunk yielded no claims from one extractor; decided by code, never by a model
type ExtractionCause = Literal[
    "malformed-output",  # not JSON, or not the claims schema
    "truncated",  # the answer was cut off (finish reason `length`) before it was valid JSON
    "refusal",  # the model declined
    "provider-error",  # no answer after the client's retries
    "model-unavailable",  # the model is gone; the rest of this extractor's chunks are not asked
    "quota-exhausted",  # the budget ran out; the rest is not asked, a later run continues
]

# bump when the prompt text, the answer schema or the parsing rules change
PROMPT_VERSION = 1


@dataclass(frozen=True)
class ExtractorSpec:
    """One extractor = one model + one prompt version. `name` is what claims record."""

    name: str
    model: str
    prompt_version: int = PROMPT_VERSION
    max_tokens: int | None = None  # None = the provider's default; part of the prompt hash


# SPEC §6.4: two extractors with different models; Groq limits count per model, so the two
# don't share a budget (SPEC §8). gpt-oss-20b is a reasoning model: with Groq's default
# completion limit it often ran out before the JSON (`json_validate_failed`, "max completion
# tokens reached"; 4 of 11 recorded chunks), with 8192 the same chunk passed (1632 of 1877
# completion tokens were reasoning).
DEFAULT_EXTRACTORS = (
    ExtractorSpec("qwen/qwen3.8-27b", "qwen/qwen3.8-27b"),
    ExtractorSpec("openai/gpt-oss-20b", "openai/gpt-oss-20b", max_tokens=8192),
)
# models whose extractor gets a larger completion limit when only the model ID is given
REASONING_MAX_TOKENS = {"openai/gpt-oss-20b": 8192, "openai/gpt-oss-120b": 8192}


def extractor_for(model: str) -> ExtractorSpec:
    """The extractor for a model ID from the config or the command line."""
    return ExtractorSpec(model, model, max_tokens=REASONING_MAX_TOKENS.get(model))


@dataclass(frozen=True)
class RawClaim:
    """One claim as the model returned it, after validation; not bound to a chunk yet."""

    local_id: str  # "c1" from the answer
    text: str
    citation: str  # exactly as returned; the citation check (grounding) normalizes it
    type: ClaimType


@dataclass(frozen=True)
class ExtractedClaim:
    chunk_id: str
    extractor: str  # ExtractorSpec.name
    local_id: str
    text: str
    citation: str
    type: ClaimType
    # the LLM call that produced the claim, (run_id, prompt_hash) = its `LlmCall`; a reused
    # claim keeps the values of the original call
    run_id: str
    prompt_hash: str
    model: str  # exact model ID that answered, as the provider reported it


@dataclass(frozen=True)
class ExtractionFailure:
    chunk_id: str
    extractor: str
    cause: ExtractionCause
    detail: str


@dataclass(frozen=True)
class ExtractionProblem:
    """A single claim of an otherwise valid answer that was skipped, and why."""

    chunk_id: str
    extractor: str
    detail: str


@dataclass(frozen=True)
class ExtractionResult:
    extractor: ExtractorSpec
    claims: tuple[ExtractedClaim, ...]  # chunk order, then answer order
    failures: tuple[ExtractionFailure, ...]
    problems: tuple[ExtractionProblem, ...]
    asked: int  # chunks sent to the model in this run
    reused: int  # chunks whose claims came from the store
    without_prose: int  # chunks skipped because they have no prose (nothing to claim)
    stopped: ExtractionCause | None = None  # set when the run stopped early
