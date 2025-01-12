from __future__ import annotations

import atexit
import time

from tabulate import tabulate


# ----------------------------------------

class Profiler:
    def __init__(self, print_on_exit : bool = False):
        self.print_on_exit : bool = print_on_exit
        self.scopes : dict[str, TimedScope] = {}

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
        for name, scope in self.scopes.items():
            row = [name, f"{scope.total_time:.6f}"]
            if print_average_times:
                row.append(f"{scope.average_time:.6f}")
            if print_num_calls:
                row.append(scope.num_calls)
            table.append(row)

        return tabulate(table, headers=headers, tablefmt="psql")

    def call_report(self):
        pass

    def profiled_scope(self, name : str) -> TimedScope:
        if name in self.scopes:
            ts = self.scopes[name]
        else:
            ts = TimedScope()
            self.scopes[name] = ts
        return ts


class TimedScope:
    def __init__(self):
        self.execution_times : list[float] = []

    def __enter__(self):
        self.start_time = time.time()

    def __exit__(self, exc_type, exc_val, exc_tb):
        end_time = time.time()
        elapsed = end_time - self.start_time
        self.execution_times.append(elapsed)

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

