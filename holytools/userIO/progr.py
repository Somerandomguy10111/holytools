import time
import progressbar
from typing import Iterable
from progressbar import ProgressBar

class TrackedInt:
    progressbar.streams.wrap_stderr()
    progressbar.streams.wrap_stdout()

    def __init__(self, start : int, end : int):
        self._value : int = start
        self.iterator : Iterable = iter(range(start, end))
        self.progressbar = ProgressBar(min_value=start, max_value=end)

    def update(self, incr : int):
        self._value += incr
        self.progressbar.update(value=self._value)