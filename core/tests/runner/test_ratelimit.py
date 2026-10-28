import pytest

from notinspec.runner import QuotaExhausted, RateLimiter

DAY = 86_400.0


class Clock:
    def __init__(self, now: float = 10 * DAY) -> None:
        self.now = now
        self.slept: list[float] = []

    def __call__(self) -> float:
        return self.now

    def sleep(self, seconds: float) -> None:
        self.slept.append(seconds)
        self.now += seconds


def limiter(clock: Clock, per_minute: int = 20, per_day: int = 50) -> RateLimiter:
    return RateLimiter(per_minute, per_day, clock=clock, sleep=clock.sleep)


def test_paces_to_per_minute() -> None:
    clock = Clock()
    limit = limiter(clock, per_minute=3)
    for _ in range(3):
        limit.acquire()
        clock.now += 1
    assert clock.slept == []
    limit.acquire()  # 4th within the minute waits until the 1st is 60 s old
    assert clock.slept == [57.0]


def test_stops_at_daily_budget() -> None:
    clock = Clock()
    limit = limiter(clock, per_minute=100, per_day=2)
    limit.acquire()
    limit.acquire()
    with pytest.raises(QuotaExhausted, match="daily budget of 2"):
        limit.acquire()


def test_budget_resets_at_utc_midnight() -> None:
    clock = Clock(now=10 * DAY + DAY - 1)  # 23:59:59 UTC
    limit = limiter(clock, per_minute=100, per_day=1)
    limit.acquire()
    with pytest.raises(QuotaExhausted):
        limit.acquire()
    clock.now += 1
    limit.acquire()
