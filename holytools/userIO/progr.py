import time
from typing import Iterable

import progressbar
from progressbar import ProgressBar
# ---------------------------------------------------------

class TrackedInt:
    progressbar.streams.wrap_stderr()
    progressbar.streams.wrap_stdout()

    def __init__(self, start_value : int, max_value : int):
        self._value : int = start_value
        self.iterator : Iterable = iter(range(start_value, max_value))
        self.progressbar = ProgressBar(min_value=start_value, max_value=max_value)

    def update(self, incr : int):
        if self.progressbar.finished():
            return

        new_value = self._value + incr
        if new_value > self.progressbar.max_value:
            self.progressbar.finish()
            return

        self._value += incr
        self.progressbar.update(value=self._value)

    def __iadd__(self, other):
        if not isinstance(other, int):
            raise ValueError("Only integers can be added to a TrackedInt.")
        self.update(incr=other)
        return self

    def __add__(self, other):
        raise NotImplementedError(f'Can only add to tracked integer in place')

