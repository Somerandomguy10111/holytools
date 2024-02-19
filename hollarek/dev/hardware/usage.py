from dataclasses import dataclass
import psutil
from psutil import Process, NoSuchProcess
import inspect
from pympler import asizeof

# -------------------------------------------

@dataclass
class UsageStatistics:
    cpu_usage : float
    memory_in_bytes : int
    user : str

class ProcessStatistics:
    def __init__(self, pid : int):
        self.pid : int = pid

        init_successful = False
        try:
            self.process : Process = psutil.Process(self.pid)
            init_successful = True
        except NoSuchProcess:
            pass
        if not init_successful:
            raise IOError(f"Process with PID {self.pid} does not exist.")


    def get_memory_usage_in_mb(self) -> float:
        memory_info = self.process.memory_info()
        return memory_info.rss / (1024 ** 2)

    def get_cpu_usage(self) -> float:
        process = psutil.Process(self.pid)
        return process.cpu_percent(interval=1)


class FunctionStatistics:
    @staticmethod
    def get_caller_frame():
        return inspect.currentframe().f_back

    def get_memory_usage_in_bytes(self) -> int:
        caller_frame = self.get_caller_frame()
        try:
            current_locals_size = asizeof.asizeof(caller_frame.f_locals)
            return current_locals_size
        finally:
            del caller_frame


# Example usage
if __name__ == "__main__":
    # ProcessStatistics usage example
    # Replace '1234' with an actual process ID
    process_stats = ProcessStatistics(1234)
    print(f"Memory usage: {process_stats.get_memory_usage_in_mb()} MB")
    print(f"CPU usage: {process_stats.get_cpu_usage()} %")

    # FunctionStatistics usage example
    def sample_function():
        func_stats = FunctionStatistics()
        a = [i for i in range(1000)]
        increase = func_stats.get_memory_usage_in_bytes()
        print(f"Memory usage of function: {increase} bytes")

    sample_function()
