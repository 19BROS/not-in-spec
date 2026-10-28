"""Asks a model once per (run, model, prompt), with caching, pacing and retries."""

import time
from collections.abc import Callable
from dataclasses import dataclass
from typing import Protocol

from notinspec.runner.provider import (
    ChatRequest,
    Completion,
    Provider,
    QuotaExhausted,
    RateLimited,
    TransientError,
)
from notinspec.runner.ratelimit import RateLimiter


@dataclass(frozen=True)
class CacheKey:
    run_id: str
    model: str
    prompt_hash: str


class ResponseCache(Protocol):
    def get(self, key: CacheKey) -> Completion | None: ...
    def put(self, key: CacheKey, completion: Completion) -> None: ...


class MemoryCache:
    def __init__(self) -> None:
        self._items: dict[CacheKey, Completion] = {}

    def get(self, key: CacheKey) -> Completion | None:
        return self._items.get(key)

    def put(self, key: CacheKey, completion: Completion) -> None:
        self._items[key] = completion


class ModelClient:
    """One answer per task, model and mode in a run (FAQ §4).

    A resumed run reuses cached answers. The cache key includes the run ID, so a new run always
    asks again. Only failures that produced no answer are retried; a wrong or malformed answer is a
    result. A rate limit asking to wait longer than `max_wait` pauses the run instead of sleeping.
    """

    def __init__(
        self,
        provider: Provider,
        *,
        limiter: RateLimiter | None = None,
        cache: ResponseCache | None = None,
        max_attempts: int = 5,
        backoff: float = 2.0,
        max_wait: float = 120.0,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self._provider = provider
        self._limiter = limiter
        self._cache = cache if cache is not None else MemoryCache()
        self._max_attempts = max_attempts
        self._backoff = backoff
        self._max_wait = max_wait
        self._sleep = sleep

    def ask(self, run_id: str, request: ChatRequest) -> Completion:
        key = CacheKey(run_id, request.model, request.prompt_hash())
        if (cached := self._cache.get(key)) is not None:
            return cached
        for attempt in range(1, self._max_attempts + 1):
            if self._limiter is not None:
                self._limiter.acquire()
            try:
                completion = self._provider.complete(request)
            except RateLimited as e:
                wait = e.retry_after if e.retry_after is not None else self._delay(attempt)
                if wait > self._max_wait:
                    raise QuotaExhausted(f"rate limited for {wait:.0f}s: {e}") from e
                if attempt == self._max_attempts:
                    raise
            except TransientError:
                if attempt == self._max_attempts:
                    raise
                wait = self._delay(attempt)
            else:
                self._cache.put(key, completion)
                return completion
            self._sleep(wait)
        raise AssertionError("unreachable")

    def _delay(self, attempt: int) -> float:
        return float(self._backoff * 2 ** (attempt - 1))
