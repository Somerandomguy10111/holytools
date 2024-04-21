from datetime import datetime
from typing import Optional


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
