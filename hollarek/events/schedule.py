import logging
from apscheduler.schedulers.background import BackgroundScheduler

logging.getLogger('apscheduler').setLevel(logging.ERROR)
scheduler = BackgroundScheduler()

def schedule(callback: callable, interval_in_sec: int):
    scheduler.add_job(callback, 'interval', seconds=interval_in_sec)
    if not scheduler.running:
        scheduler.start()


def enable_schedule_logging():
    set_schedule_logging_level(level=logging.INFO)


def disable_schedule_logging():
    set_schedule_logging_level(level=logging.CRITICAL)


def set_schedule_logging_level(level):
    logging.getLogger('apscheduler').setLevel(level)

