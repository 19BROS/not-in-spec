import logging
import os
from functools import lru_cache
from pathlib import Path

from apscheduler.schedulers.blocking import BlockingScheduler

log = logging.getLogger("notinspec.worker")


@lru_cache
def hosted_worker():
    from notinspec.db import database_url, make_engine
    from notinspec.db.hosted import HostedService
    from notinspec.db.hosted_claims import HostedClaims
    from notinspec.nli import TransformersNli
    from notinspec.runner import FIIT, ModelClient, OpenAICompatProvider

    engine = make_engine(database_url())
    service = HostedService(
        engine,
        Path(os.environ.get("NOTINSPEC_UPLOADS_DIR", "tmp/uploads")),
        Path(os.environ.get("NOTINSPEC_RUNS_DIR", "tmp/runs")),
        os.environ.get("NOTINSPEC_PUBLIC_URL", "https://147-175-151-17.sslip.io"),
    )
    claims = None
    if os.environ.get("NOTINSPEC_HOSTED_CLAIMS") == "1":
        nli = TransformersNli()
        nli.load()
        claims = HostedClaims(
            engine,
            ModelClient(OpenAICompatProvider.from_env(FIIT), limits=FIIT.limiters()),
            nli,
            service.uploads_dir / "calls",
        )
    return service, claims


def queued_runs() -> None:
    if os.environ.get("NOTINSPEC_UPLOADS_ENABLED") != "1":
        return
    try:
        service, claims = hosted_worker()
        run_id = service.work_one(claims)
        if run_id:
            log.info("hosted run finished: %s", run_id)
    except Exception:
        log.exception("hosted worker could not process the queue")


def nightly_runs() -> None:
    log.info("nightly run: nothing to do yet")


def build_scheduler() -> BlockingScheduler:
    # The timer is in memory; queued/running jobs themselves live in PostgreSQL.
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(nightly_runs, "cron", hour=3, id="nightly_runs")
    scheduler.add_job(
        queued_runs, "interval", seconds=10, id="queued_runs", max_instances=1, coalesce=True
    )
    return scheduler


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    log.info("worker started")
    build_scheduler().start()
