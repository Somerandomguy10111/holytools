import time
from functools import wraps
from typing import Callable
from abc import abstractmethod
from tabulate import tabulate

# ---------------------------------------------------------

class Profilable:
    def __init__(self):
        self._execution_times = {}
        self.set_profiling()

    def set_profiling(self):
        methods = self.profiled_methods()
        for method in methods:
            profiled_method = self.profile(method)
            setattr(self, method.__name__, profiled_method)

    def profile(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed_time = time.time() - start_time
            if func.__name__ not in self._execution_times:
                self._execution_times[func.__name__] = {'total_time': 0, 'calls': 0}
            self._execution_times[func.__name__]['total_time'] += elapsed_time
            self._execution_times[func.__name__]['calls'] += 1
            return result

        return wrapper

    def get_report(self):
        table = []
        headers = ["Method", "Average Time", "Total Time", "No. Calls"]
        for method, stats in self._execution_times.items():
            average_time = stats['total_time'] / stats['calls']
            table.append([method, f"{round(average_time,6)}s", f"{round(stats['total_time'],6)}s", stats['calls']])

        return tabulate(table, headers=headers, tablefmt="grid")

    @classmethod
    @abstractmethod
    def profiled_methods(cls) -> list[Callable]:
        pass


class This(Profilable):
    @classmethod
    def profiled_methods(cls) -> list[Callable]:
        return [cls.do_this, cls.another_method]

    @staticmethod
    def do_this():
        print('abc')

    @staticmethod
    def another_method(x):
        print(x)


if __name__ == "__main__":
    a = This()
    a.do_this()
    a.do_this()
    a.another_method(0.1)
    a.another_method(0.2)

    print(a.get_report())