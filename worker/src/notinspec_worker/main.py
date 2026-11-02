import logging

from apscheduler.schedulers.blocking import BlockingScheduler

log = logging.getLogger("notinspec.worker")


def nightly_runs() -> None:
    log.info("nightly run: nothing to do yet")


def build_scheduler() -> BlockingScheduler:
    # shortcut: in-memory job store, move to SQLAlchemyJobStore once the Postgres schema exists
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(nightly_runs, "cron", hour=3, id="nightly_runs")
    return scheduler


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    log.info("worker started")
    build_scheduler().start()
