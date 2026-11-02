from notinspec_worker.main import build_scheduler


def test_nightly_job_registered() -> None:
    assert build_scheduler().get_job("nightly_runs") is not None
