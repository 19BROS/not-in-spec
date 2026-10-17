import logging

from apscheduler.schedulers.blocking import BlockingScheduler

log = logging.getLogger("notinspec.worker")


def weekly_runs() -> None:
    log.info("weekly run: nothing to do yet")


def build_scheduler() -> BlockingScheduler:
    # shortcut: in-memory job store, move to SQLAlchemyJobStore once the Postgres schema exists
    scheduler = BlockingScheduler(timezone="UTC")
    scheduler.add_job(weekly_runs, "cron", day_of_week="mon", hour=3, id="weekly_runs")
    return scheduler


def main() -> None:
    logging.basicConfig(level=logging.INFO)
    log.info("worker started")
    build_scheduler().start()
