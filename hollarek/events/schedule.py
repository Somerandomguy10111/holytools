import logging
from apscheduler.schedulers.background import BackgroundScheduler
from hollarek.templates import Singleton
from typing import Optional
from typing import Callable

class ScheduleHandler(Singleton):
    scheduler : Optional[BackgroundScheduler]= None
    logging.getLogger('apscheduler').setLevel(logging.ERROR)

    @classmethod
    def get_scheduler(cls):
        if not cls.scheduler:
            cls.scheduler = BackgroundScheduler()
            cls.scheduler.start()
        return cls.scheduler


def schedule(callback: Callable, interval_in_sec: int):
    scheduler = ScheduleHandler.get_scheduler()
    scheduler.add_job(callback, 'interval', seconds=interval_in_sec)