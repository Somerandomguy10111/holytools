from datetime import datetime, timedelta
from threading import Event
from typing import Callable, Optional, Any
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.job import Job
import inspect

from hollarek.logging import Loggable
from .input_waiter import InputWaiter

class InvalidCallableException(Exception):
    """Exception raised when a callable with arguments is passed where none are expected."""
    pass


class Countdown:
    def __init__(self, duration: float, on_expiration: Callable = lambda *args, **kwargs: None):
        parameters = inspect.signature(on_expiration).parameters.values()
        for param in parameters:
            # Check if the parameter is mandatory (i.e., has no default value and is not a *args or **kwargs kind)
            if (param.default is param.empty) and (param.kind not in [param.VAR_POSITIONAL, param.VAR_KEYWORD]):
                raise InvalidCallableException("on_expiration should not take any mandatory arguments")
        self.duration : float = duration
        self.scheduler : BackgroundScheduler = BackgroundScheduler()
        self.job: Optional[Job] = None
        self.on_expiration : Callable = on_expiration
        self.output_waiter : InputWaiter = InputWaiter()

        self.one_time_lock = Lock()
        self.scheduler.start()

    def restart(self):
        try:
            self.job.remove()
        except:
            pass
        self.start()

    def start(self):
        run_time = datetime.now() + timedelta(seconds=self.duration)
        self.job = self.scheduler.add_job(func=self._release, trigger='date', next_run_time=run_time)

    def finish(self) -> Any:
        self.one_time_lock.wait()

    def get_output(self):
        if not self.on_expiration:
            raise ValueError("on_expiration must be set to use this method")
        return self.output_waiter.get()

    def _release(self):
        self.one_time_lock.unlock()
        out = self.on_expiration()
        self.output_waiter.write(out)


class Lock:
    def __init__(self):
        self._event = Event()
        self._event.clear()

    def wait(self):
        self._event.wait()

    def unlock(self):
        self._event.set()


# Usage examples
class Timer:
    def __init__(self):
        self.start_time : Optional[datetime] = None

    def start(self):
        self.start_time = datetime.now()

    def capture(self, verbose : bool = True) -> float:
        now = datetime.now()
        delta = now-self.start_time
        delta_sec = delta.total_seconds()
        if verbose:
            print(f'Time has been running for {delta_sec} seconds')
        return delta_sec


class Clock(Loggable):
    pass
