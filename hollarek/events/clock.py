import time
from datetime import datetime, timedelta
from threading import Event
from typing import Callable, Optional
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.job import Job
import inspect

from hollarek.logging import Loggable
from devtools import Timer as DevtoolsTimer


class InvalidCallableException(Exception):
    """Exception raised when a callable with arguments is passed where none are expected."""
    pass


class Countdown:
    def __init__(self, duration: float = 0.25, on_expiration: Callable = lambda *args, **kwargs: None):
        if inspect.signature(on_expiration).parameters:
            raise InvalidCallableException("on_expiration should not take any arguments")

        self.initial_time = duration
        self.scheduler = BackgroundScheduler()
        self.job: Optional[Job] = None
        self.on_expiration = on_expiration

        self.one_time_lock = Event()
        self.scheduler.start()

    def restart(self):
        try:
            self.job.remove()
        except:
            pass  # Ideally, log this exception

        self.start()

    def start(self):
        self.one_time_lock.clear()
        run_time = datetime.now() + timedelta(seconds=self.initial_time)
        self.job = self.scheduler.add_job(func=self._release, trigger='date', next_run_time=run_time)

    def finish(self):
        self.one_time_lock.wait()

    def _release(self):
        self.one_time_lock.set()
        self.on_expiration()


# Usage examples
class Timer(DevtoolsTimer):
    pass


class Clock(Loggable):
    pass


def say_hi():  # This function has no parameters
    print(f'sup mah man')

def transmit(msg : str):
    print(msg)

# This will work as expected
countdown = Countdown(duration=3, on_expiration=say_hi)
# new = Countdown(duration=3, on_expiration=transmit)
countdown.start()

# This will wait for 4 seconds to allow for the countdown to expire
time.sleep(4)