from dataclasses import replace

import pytest

from notinspec.runner import (
    ChatRequest,
    Completion,
    MemoryCache,
    ModelClient,
    ModelUnavailable,
    ProviderError,
    QuotaExhausted,
    RateLimited,
    RateLimiter,
    TransientError,
)

ANSWER = Completion("{}", None, "stop", "acme/model-a:free", {"id": "gen-1"})


class Scripted:
    """Returns or raises the scripted outcomes in order."""

    def __init__(self, *outcomes: Completion | ProviderError) -> None:
        self.outcomes = list(outcomes)
        self.calls = 0

    def complete(self, request: ChatRequest) -> Completion:
        self.calls += 1
        outcome = self.outcomes.pop(0)
        if isinstance(outcome, ProviderError):
            raise outcome
        return outcome


def client(provider: Scripted, sleeps: list[float], **kwargs: object) -> ModelClient:
    return ModelClient(provider, sleep=sleeps.append, **kwargs)  # type: ignore[arg-type]


def test_answers_once_per_run(request_: ChatRequest) -> None:
    provider, sleeps = Scripted(ANSWER, ANSWER), []
    models = client(provider, sleeps, cache=MemoryCache())

    assert models.ask("run-1", request_) is ANSWER
    assert models.ask("run-1", request_) is ANSWER  # resumed run: cached, not asked again
    assert provider.calls == 1
    models.ask("run-2", request_)  # next run asks again
    assert provider.calls == 2


def test_changed_prompt_is_not_cached(request_: ChatRequest) -> None:
    provider, sleeps = Scripted(ANSWER, ANSWER), []
    models = client(provider, sleeps)
    models.ask("run-1", request_)
    models.ask("run-1", replace(request_, temperature=0.5))
    assert provider.calls == 2


def test_retries_transient_errors_with_backoff(request_: ChatRequest) -> None:
    provider = Scripted(TransientError("502"), TransientError("timeout"), ANSWER)
    sleeps: list[float] = []
    assert client(provider, sleeps).ask("run-1", request_) is ANSWER
    assert sleeps == [2.0, 4.0]


def test_rate_limit_waits_as_told(request_: ChatRequest) -> None:
    provider = Scripted(RateLimited("429", retry_after=9.0), RateLimited("429"), ANSWER)
    sleeps: list[float] = []
    assert client(provider, sleeps).ask("run-1", request_) is ANSWER
    assert sleeps == [9.0, 4.0]


def test_long_rate_limit_pauses_the_run(request_: ChatRequest) -> None:
    provider = Scripted(RateLimited("free-models-per-day", retry_after=3600.0))
    with pytest.raises(QuotaExhausted, match="3600s"):
        client(provider, []).ask("run-1", request_)


def test_gives_up_after_max_attempts(request_: ChatRequest) -> None:
    provider = Scripted(*[TransientError(f"502 #{i}") for i in range(3)])
    sleeps: list[float] = []
    with pytest.raises(TransientError, match="#2"):
        client(provider, sleeps, max_attempts=3).ask("run-1", request_)
    assert sleeps == [2.0, 4.0]


def test_gives_up_on_repeated_rate_limits(request_: ChatRequest) -> None:
    provider = Scripted(RateLimited("a", 1.0), RateLimited("b", 1.0))
    with pytest.raises(RateLimited, match="b"):
        client(provider, [], max_attempts=2).ask("run-1", request_)


@pytest.mark.parametrize("error", [ModelUnavailable("404"), ProviderError("401")], ids=str)
def test_permanent_errors_are_not_retried(request_: ChatRequest, error: ProviderError) -> None:
    provider, sleeps = Scripted(error), []
    with pytest.raises(type(error)):
        client(provider, sleeps).ask("run-1", request_)
    assert provider.calls == 1 and sleeps == []


def test_failures_are_not_cached(request_: ChatRequest) -> None:
    provider = Scripted(ModelUnavailable("404"), ANSWER)
    models = client(provider, [])
    with pytest.raises(ModelUnavailable):
        models.ask("run-1", request_)
    assert models.ask("run-1", request_) is ANSWER


def test_every_attempt_uses_the_budget(request_: ChatRequest) -> None:
    limiter = RateLimiter(per_minute=100, per_day=2, clock=lambda: 0.0, sleep=lambda _: None)
    provider = Scripted(TransientError("502"), TransientError("502"), ANSWER)
    with pytest.raises(QuotaExhausted):
        client(provider, [], limiter=limiter).ask("run-1", request_)
    assert provider.calls == 2
