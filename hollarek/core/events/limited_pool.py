import time
import threading
from queue import Queue
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from typing import Callable

# ---------------------------------------------------------

@dataclass
class FunctionTask:
    function: Callable
    args: tuple = field(default_factory=tuple)
    kwargs: dict = field(default_factory=dict)


class RateLimitedPool:
    def __init__(self, tasks_per_second : int, max_workers=10):
        super().__init__()
        self.max_rate = tasks_per_second
        self.executor = ThreadPoolExecutor(max_workers=max_workers)
        self.task_queue : Queue[FunctionTask] = Queue()
        self.is_running = False

    def start(self):
        if not self.is_running:
            self.is_running = True
            threading.Thread(target=self._release_tasks).start()

    def stop(self):
        self.is_running = False

    def _release_tasks(self):
        while self.is_running:
            if not self.task_queue.empty():
                task = self.task_queue.get()
                self.executor.submit(task.function, *task.args, **task.kwargs)
            time.sleep(1 / self.max_rate)

    def submit(self, task):
        self.task_queue.put(task)


if __name__ == "__main__":
    def func(n):
        print(f"Executing task {n}")
        print(f'Current time is {time.time()}')
        return n * 2

    pool = RateLimitedPool(tasks_per_second=5)
    pool.start()

    # Submit tasks
    for i in range(10):
        pool.submit(FunctionTask(function=func, kwargs={'n' : i}))

    time.sleep(10)
    pool.stop()
