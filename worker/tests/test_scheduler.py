from notinspec_worker.main import build_scheduler


def test_weekly_job_registered() -> None:
    assert build_scheduler().get_job("weekly_runs") is not None
