from __future__ import annotations

import atexit
import time

from tabulate import tabulate


# ----------------------------------------

class Profiler:
    def __init__(self, print_on_exit : bool = False):
        self._execution_profiles : dict[str, ExecutionProfile] = {}
        self.print_on_exit : bool = print_on_exit

        if self.print_on_exit:
            def print_report():
                print(f'----> Profiler scope report\n')
                print(self.scope_report())
            atexit.register(print_report)


    def scope_report(self, section_name : str = f'Routine', print_average_times=True, print_num_calls=True) -> str:
        headers = [section_name, "Total Time (s)"]
        if print_average_times:
            headers.append("Average Time (s)")
        if print_num_calls:
            headers.append("Calls")

        table = []
        for section, profile in self._execution_profiles.items():
            row = [section, f"{profile.total_time:.6f}"]
            if print_average_times:
                row.append(f"{profile.average_time:.6f}")
            if print_num_calls:
                row.append(profile.num_calls)
            table.append(row)

        return tabulate(table, headers=headers, tablefmt="psql")

    def timed_scope(self, name : str) -> TimedScope:
        return TimedScope(name=name,storage=self._execution_profiles)


    def call_report(self, depth : int):
        pass

    @staticmethod
    def measure(self, func):
        def wrapper(*args, **kwargs):
            with self.timed_scope(name=func.__name__):
                result = func(*args, **kwargs)
            return result

        return wrapper


class TimedScope:
    def __init__(self, name: str, storage : dict[str, ExecutionProfile]):
        self.name : str = name
        self.storage : dict[str, ExecutionProfile] = storage

    def __enter__(self):
        self.start_time = time.time()
        if not self.name in self.storage:
            self.storage[self.name] = ExecutionProfile()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        elapsed = end_time - self.start_time
        if self.name in self.storage:
            self.storage[self.name].register_time(elapsed)
        else:
            raise KeyError(f"Execution profile {self.name} not found in storage")


class ExecutionProfile:
    def __init__(self):
        self.execution_times = []

    def register_time(self, time_in_sec : float):
        self.execution_times.append(time_in_sec)

    @property
    def num_calls(self):
        return len(self.execution_times)

    @property
    def total_time(self):
        return sum(self.execution_times)

    @property
    def average_time(self):
        return self.total_time / self.num_calls


if __name__ == "__main__":
    pass

