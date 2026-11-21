"""Running one extractor over chunks (SPEC §6.4 step 1). Grounding comes after this.

One request per chunk that has prose; a chunk without prose has nothing to claim and is not
sent. Each chunk is read whole. A failure of one chunk is recorded and the run goes on, except
when the model is gone, the budget is used up or a request timed out again after its one retry:
then the remaining chunks are recorded as not asked, and a later run continues where this one
stopped (the store has the finished chunks).
"""

from collections.abc import Callable, Sequence
from dataclasses import asdict
from datetime import UTC, datetime

from notinspec.chunking import Chunk, prose_sentences
from notinspec.claims.model import (
    ExtractedClaim,
    ExtractionCause,
    ExtractionFailure,
    ExtractionProblem,
    ExtractionResult,
    ExtractorSpec,
)
from notinspec.claims.parse import PARSER_VERSION, ParsedClaims, parse_claims
from notinspec.claims.prompt import build_request
from notinspec.claims.store import CallLog, ClaimStore, LlmCall, ReuseKey, StoredAnswer
from notinspec.runner import (
    ChatRequest,
    ModelClient,
    ModelUnavailable,
    ProviderError,
    QuotaExhausted,
    RequestTimeout,
)

ROLE = "claim-extractor"


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def extract_claims(
    chunks: Sequence[Chunk],
    spec: ExtractorSpec,
    client: ModelClient,
    run_id: str,
    calls: CallLog,
    *,
    store: ClaimStore | None = None,
    reuse: bool = True,
    clock: Callable[[], str] = _now,
) -> ExtractionResult:
    """`reuse=False` asks again for every chunk and replaces its stored answer."""
    claims: list[ExtractedClaim] = []
    failures: list[ExtractionFailure] = []
    problems: list[ExtractionProblem] = []
    asked = reused = without_prose = 0
    stopped: ExtractionCause | None = None
    # two chunks with the same prompt get one answer, logged once
    answers: dict[str, tuple[ParsedClaims, StoredAnswer]] = {}

    for chunk in chunks:
        if not prose_sentences(chunk):
            without_prose += 1
            continue
        key = ReuseKey(
            chunk.content_hash,
            chunk.breadcrumb,
            spec.name,
            spec.model,
            spec.prompt_version,
            spec.reasoning_effort,
            PARSER_VERSION,
            spec.thinking,
        )
        if reuse and store is not None and (stored := store.get(key)) is not None:
            claims.extend(_bind(chunk, spec, stored))
            problems.extend(ExtractionProblem(chunk.id, spec.name, p) for p in stored.problems)
            reused += 1
            continue
        if stopped is not None:
            failures.append(ExtractionFailure(chunk.id, spec.name, stopped, "not asked"))
            continue

        request = build_request(chunk, spec)
        known = answers.get(request.prompt_hash())
        if known is None:
            asked += 1
            try:
                completion = client.ask(run_id, request)
            except ProviderError as e:
                cause: ExtractionCause = "provider-error"
                if isinstance(e, QuotaExhausted):
                    cause = stopped = "quota-exhausted"
                elif isinstance(e, ModelUnavailable):
                    cause = stopped = "model-unavailable"
                elif isinstance(e, RequestTimeout):
                    cause = stopped = "timed-out"
                calls.append(
                    _call(run_id, spec, chunk, request, None, f"{type(e).__name__}: {e}", clock)
                )
                failures.append(ExtractionFailure(chunk.id, spec.name, cause, str(e)[:300]))
                continue
            calls.append(_call(run_id, spec, chunk, request, completion.raw, None, clock))
            parsed = parse_claims(
                completion.content,
                refusal=completion.refusal,
                finish_reason=completion.finish_reason,
            )
            answer = StoredAnswer(
                parsed.claims, parsed.problems, run_id, request.prompt_hash(), completion.model
            )
            answers[request.prompt_hash()] = parsed, answer
        else:
            parsed, answer = known

        if parsed.cause is not None:
            failures.append(ExtractionFailure(chunk.id, spec.name, parsed.cause, parsed.detail))
            continue
        claims.extend(_bind(chunk, spec, answer))
        problems.extend(ExtractionProblem(chunk.id, spec.name, p) for p in answer.problems)
        if store is not None:
            store.put(key, answer)

    return ExtractionResult(
        extractor=spec,
        claims=tuple(claims),
        failures=tuple(failures),
        problems=tuple(problems),
        asked=asked,
        reused=reused,
        without_prose=without_prose,
        stopped=stopped,
    )


def _bind(chunk: Chunk, spec: ExtractorSpec, answer: StoredAnswer) -> list[ExtractedClaim]:
    return [
        ExtractedClaim(
            chunk.id,
            spec.name,
            c.local_id,
            c.text,
            c.citation,
            c.type,
            run_id=answer.run_id,
            prompt_hash=answer.prompt_hash,
            model=answer.model,
        )
        for c in answer.claims
    ]


def _call(
    run_id: str,
    spec: ExtractorSpec,
    chunk: Chunk,
    request: ChatRequest,
    response: dict[str, object] | None,
    error: str | None,
    clock: Callable[[], str],
) -> LlmCall:
    return LlmCall(
        run_id=run_id,
        role=ROLE,
        extractor=spec.name,
        chunk_id=chunk.id,
        model=request.model,
        prompt_hash=request.prompt_hash(),
        request=asdict(request),
        response=response,
        error=error,
        time=clock(),
    )
