import time
from tabulate import tabulate


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

class TimedScope:
    def __init__(self, name: str, storage : dict):
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

class Profiler:
    def __init__(self):
        self._execution_profiles : dict[str, ExecutionProfile] = {}

    def make_report(self) -> str:
        headers = ["Section", "Total Time (s)", "Average Time (s)", "Calls"]
        table = []
        for section, profile in self._execution_profiles.items():
            table.append([section, f"{profile.total_time:.6f}", f"{profile.average_time:.6f}", profile.num_calls])
        return tabulate(table, headers=headers, tablefmt="psql")

    def timed_scope(self, name : str) -> TimedScope:
        return TimedScope(name, self._execution_profiles)


if __name__ == "__main__":
    class ExampleClass(Profiler):
        def some_method(self):
            with self.timed_scope(name='being_work'):
                time.sleep(0.1)

            with self.timed_scope(name='phase2'):
                time.sleep(0.1)
                self.subroutine()
            with self.timed_scope(name='phase3'):
                time.sleep(0.1)

        def subroutine(self):
            with self.timed_scope(name='subroutine'):
                time.sleep(0.2)

    instance = ExampleClass()
    instance.some_method()  # Execute the profiled method multiple times to see accumulation
    instance.some_method()
    print(instance.make_report())  # Output the profiling report


