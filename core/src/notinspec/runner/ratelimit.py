"""Client-side request budget for OpenRouter free models (SPEC §3.1)."""

import time
from collections import deque
from collections.abc import Callable
from datetime import UTC, datetime

from notinspec.runner.provider import QuotaExhausted


class RateLimiter:
    """Paces requests to `per_minute` and stops at `per_day` (the day is UTC).

    OpenRouter counts per account, not per key, so everything sharing a key must share one limiter.
    Every attempt counts, retries included.
    """

    def __init__(
        self,
        per_minute: int = 20,
        per_day: int = 50,
        *,
        clock: Callable[[], float] = time.time,
        sleep: Callable[[float], None] = time.sleep,
    ) -> None:
        self.per_minute = per_minute
        self.per_day = per_day
        self._clock = clock
        self._sleep = sleep
        self._recent: deque[float] = deque()
        self._day = ""
        self._used_today = 0

    def acquire(self) -> None:
        now = self._clock()
        day = datetime.fromtimestamp(now, UTC).date().isoformat()
        if day != self._day:
            self._day, self._used_today = day, 0
        if self._used_today >= self.per_day:
            raise QuotaExhausted(f"daily budget of {self.per_day} requests used ({day} UTC)")
        while True:
            while self._recent and self._recent[0] <= now - 60:
                self._recent.popleft()
            if len(self._recent) < self.per_minute:
                break
            self._sleep(self._recent[0] + 60 - now)
            now = self._clock()
        self._recent.append(now)
        self._used_today += 1
