"""extract_claims on recorded real Groq answers (conftest.py), plus provider failures."""

from collections.abc import Callable
from dataclasses import replace
from pathlib import Path

import pytest

from notinspec.chunking import Chunk
from notinspec.claims import (
    DEFAULT_EXTRACTORS,
    ExtractorSpec,
    MemoryCallLog,
    MemoryClaimStore,
    extract_claims,
)
from notinspec.runner import (
    ChatRequest,
    Completion,
    FakeProvider,
    ModelClient,
    ModelUnavailable,
    ProviderError,
    QuotaExhausted,
)

FIXTURES = Path(__file__).parent / "fixtures"
GUIDE_RECORDING = FIXTURES / "groq-fixturelib-guide.json"
URLLIB3_RECORDING = FIXTURES / "groq-urllib3-demo.json"
QWEN, GPT_OSS = DEFAULT_EXTRACTORS
# gpt-oss-20b as first recorded, without a completion limit
GPT_OSS_UNLIMITED = ExtractorSpec("openai/gpt-oss-20b", "openai/gpt-oss-20b")


def _client(provider: object) -> ModelClient:
    return ModelClient(provider, max_attempts=1, sleep=lambda _: None)  # type: ignore[arg-type]


def test_recorded_guide_both_extractors(guide_chunks: list[Chunk]) -> None:
    fake = FakeProvider.load(GUIDE_RECORDING)
    log = MemoryCallLog()
    results = [extract_claims(guide_chunks, s, _client(fake), "r", log) for s in (QWEN, GPT_OSS)]
    qwen, gpt = results
    assert (qwen.asked, qwen.reused, qwen.without_prose) == (8, 0, 0)
    assert not qwen.failures and not gpt.failures
    assert len(qwen.claims) == 6 and len(gpt.claims) == 20
    limit = next(c for c in qwen.claims if "100" in c.text)
    assert limit.citation == "At most `100` connections."
    assert limit.extractor == "qwen/qwen3.8-27b"
    assert {c.chunk_id for c in qwen.claims} <= {c.id for c in guide_chunks}
    # one logged call per request, with the raw body
    assert len(log.calls) == 16
    assert all(c.response is not None and c.error is None for c in log.calls)
    assert {c.role for c in log.calls} == {"claim-extractor"}


def test_recorded_schema_failures_without_a_completion_limit(guide_chunks: list[Chunk]) -> None:
    result = extract_claims(
        guide_chunks,
        GPT_OSS_UNLIMITED,
        _client(FakeProvider.load(GUIDE_RECORDING)),
        "r",
        MemoryCallLog(),
    )
    causes = sorted((f.cause, f.detail) for f in result.failures)
    assert causes == [
        ("malformed-output", "json_validate_failed: empty"),
        (
            "truncated",
            "json_validate_failed: max completion tokens reached before generating a valid "
            "document",
        ),
    ]
    assert len(result.claims) == 10


def test_recorded_urllib3_demo_chunks(
    urllib3_chunks: list[Chunk], golden: Callable[..., None]
) -> None:
    fake = FakeProvider.load(URLLIB3_RECORDING)
    results = [
        extract_claims(urllib3_chunks, s, _client(fake), "r", MemoryCallLog())
        for s in DEFAULT_EXTRACTORS
    ]
    assert not any(r.failures for r in results)
    golden("urllib3-demo-claims", [c for r in results for c in r.claims])


def test_reuse_asks_nothing(guide_chunks: list[Chunk]) -> None:
    store = MemoryClaimStore()
    fake = FakeProvider.load(GUIDE_RECORDING)
    first = extract_claims(guide_chunks, QWEN, _client(fake), "r1", MemoryCallLog(), store=store)
    log = MemoryCallLog()
    second = extract_claims(
        guide_chunks, QWEN, _client(_Raising(ProviderError("no"))), "r2", log, store=store
    )
    assert (second.asked, second.reused) == (0, 8)
    assert second.claims == first.claims
    assert log.calls == []


def test_reuse_needs_the_same_breadcrumb(guide_chunks: list[Chunk]) -> None:
    store = MemoryClaimStore()
    extract_claims(
        guide_chunks,
        QWEN,
        _client(FakeProvider.load(GUIDE_RECORDING)),
        "r",
        MemoryCallLog(),
        store=store,
    )
    moved = [
        replace(c, breadcrumb=c.breadcrumb.replace("User Guide", "Guide")) for c in guide_chunks
    ]
    result = extract_claims(
        moved, QWEN, _client(_Raising(ProviderError("x"))), "r", MemoryCallLog(), store=store
    )
    assert result.reused == 0 and len(result.failures) == 8


class _Raising:
    def __init__(self, error: Exception) -> None:
        self.error = error
        self.calls = 0

    def complete(self, request: ChatRequest) -> Completion:
        self.calls += 1
        raise self.error


@pytest.mark.parametrize(
    ("error", "cause"),
    [
        (QuotaExhausted("budget"), "quota-exhausted"),
        (ModelUnavailable("gone"), "model-unavailable"),
    ],
)
def test_stop_leaves_the_rest_unasked(
    guide_chunks: list[Chunk], error: Exception, cause: str
) -> None:
    provider = _Raising(error)
    log = MemoryCallLog()
    result = extract_claims(guide_chunks, QWEN, _client(provider), "r", log)
    assert result.stopped == cause
    assert provider.calls == 1 and result.asked == 1
    assert [f.cause for f in result.failures] == [cause] * 8
    assert [f.detail for f in result.failures[1:]] == ["not asked"] * 7
    assert len(log.calls) == 1 and log.calls[0].response is None
    assert log.calls[0].error is not None and type(error).__name__ in log.calls[0].error


def test_provider_error_fails_one_chunk_and_goes_on(guide_chunks: list[Chunk]) -> None:
    provider = _Raising(ProviderError("HTTP 400: bad"))
    result = extract_claims(guide_chunks, QWEN, _client(provider), "r", MemoryCallLog())
    assert result.stopped is None
    assert provider.calls == 8
    assert {f.cause for f in result.failures} == {"provider-error"}


def test_same_prompt_is_asked_once(guide_chunks: list[Chunk]) -> None:
    chunk = next(c for c in guide_chunks if "100" in c.text)
    twin = replace(chunk, id="0123456789abcdef")
    log = MemoryCallLog()
    result = extract_claims(
        [chunk, twin], QWEN, _client(FakeProvider.load(GUIDE_RECORDING)), "r", log
    )
    assert result.asked == 1 and len(log.calls) == 1
    assert {c.chunk_id for c in result.claims} == {chunk.id, twin.id}


def test_chunks_without_prose_are_not_sent(guide_chunks: list[Chunk]) -> None:
    code_only = replace(
        guide_chunks[0], blocks=tuple(b for b in guide_chunks[0].blocks if b.kind == "heading")
    )
    provider = _Raising(ProviderError("must not be called"))
    result = extract_claims([code_only], QWEN, _client(provider), "r", MemoryCallLog())
    assert (result.without_prose, provider.calls) == (1, 0)
