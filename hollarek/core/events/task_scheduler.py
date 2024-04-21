import sched
import threading
import time
from typing import Callable, Optional


import time
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Callable



class TaskScheduler:
    def submit_once(self, task: Callable, delay: float):
        self._schedule_task(task=task, delay=delay)

    def submit_periodic(self, task: Callable, interval: float):
        def periodic():
            threading.Thread(target=task).start()
            self.submit_periodic(task, interval)
        self._schedule_task(task=periodic, delay=interval)

    # ---------------------------------------------------------

    @staticmethod
    def _schedule_task(task : Callable, delay : float):
        def do_delayed():
            time.sleep(delay)
            task()

        threading.Thread(target=do_delayed).start()


# Example usage
if __name__ == "__main__":
    def my_task():
        print(f"Task executed at {time.ctime()}. Now sleeping for 2 seconds")
        time.sleep(2)
        print(f'I work up at {time.ctime()}')

    scheduler = TaskScheduler()
    # scheduler.submit_once(my_task, delay=2)
    scheduler.submit_periodic(my_task, interval=1)

    print(f'Sleepting at {time.ctime()}')
    time.sleep(15)