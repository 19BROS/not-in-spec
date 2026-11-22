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
    "timed-out",  # no answer in time, also after the retry; after `claims.extract.TIMEOUTS_TO_STOP`
    # such chunks in a row the server counts as stuck: the rest is not asked, a later run continues
]

# bump when the prompt text or the answer schema change; parsing rules have their own version
# (`claims.parse.PARSER_VERSION`)
PROMPT_VERSION = 1


@dataclass(frozen=True)
class ExtractorSpec:
    """One extractor = one model + one prompt version. `name` is what claims record."""

    name: str
    model: str
    prompt_version: int = PROMPT_VERSION
    max_tokens: int | None = None  # None = the provider's default; part of the prompt hash
    # None = the provider's default; part of the prompt hash and of the reuse key
    reasoning_effort: str | None = None
    # False turns a reasoning model's thinking off (`enable_thinking`); None = the default.
    # Part of the prompt hash and of the reuse key
    thinking: bool | None = None


# SPEC §6.4: two extractors with different models, both free local models behind the FIIT
# LiteLLM proxy (SPEC §8). Both are reasoning models. Measured 2026-11-21 on `Retry` (the urllib3
# chunk Groq cut off at 2048 tokens): with thinking off qwen gave 54 claims (21 s of generation)
# and gemma 57 (62 s); with thinking on qwen gave 61 claims in 7.4k tokens, and gemma never
# finished: it thought 5.5k tokens for one claim on a trivial chunk, 16k with effort "low".
# The longest answer was 4.8k tokens, so 16384 leaves room.
FIIT_MAX_TOKENS = 16384
DEFAULT_EXTRACTORS = (
    ExtractorSpec(
        "qwen3.8-flash-next", "qwen3.8-flash-next", max_tokens=FIIT_MAX_TOKENS, thinking=False
    ),
    ExtractorSpec(
        "gemma4-26b-a4b-hpc", "gemma4-26b-a4b-hpc", max_tokens=FIIT_MAX_TOKENS, thinking=False
    ),
)

# The extractors on Groq until 2026-11-21, kept for `--provider groq` and its recordings.
# gpt-oss-20b is a reasoning model: with Groq's default completion limit it often ran out
# before the JSON (`json_validate_failed`, "max completion tokens reached"; 4 of 11 recorded
# chunks), with 8192 the same chunk passed (1632 of 1877 completion tokens were reasoning).
# With Groq's default effort ("medium") it used ~3.5k tokens per chunk, so the urllib3 demo
# pages would not fit one day's 200k tokens; "low" took 2.6k instead of 5.8k tokens on
# User Guide > Using Timeouts (739 vs 4086 reasoning tokens). qwen runs at Groq's default
# completion limit (2048): our free tier allows qwen only 1000 output tokens per minute, and
# Groq rejects a request it expects to answer with more ("Request too large").
GROQ_EXTRACTORS = (
    ExtractorSpec("qwen/qwen3.8-27b", "qwen/qwen3.8-27b"),
    ExtractorSpec(
        "openai/gpt-oss-20b", "openai/gpt-oss-20b", max_tokens=8192, reasoning_effort="low"
    ),
)

# the settings of a model when only its ID is given (`--extractor MODEL`)
KNOWN_EXTRACTORS: dict[str, ExtractorSpec] = {
    s.model: s
    for s in (
        *DEFAULT_EXTRACTORS,
        *GROQ_EXTRACTORS,
        ExtractorSpec("openai/gpt-oss-120b", "openai/gpt-oss-120b", max_tokens=8192),
    )
}


def extractor_for(model: str) -> ExtractorSpec:
    """The extractor for a model ID from the config or the command line."""
    return KNOWN_EXTRACTORS.get(model) or ExtractorSpec(model, model)


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
