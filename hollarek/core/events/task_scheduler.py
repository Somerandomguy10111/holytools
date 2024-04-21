import time
import threading
from typing import Callable
import inspect


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
        parameters = inspect.signature(task).parameters.values()
        for param in parameters:
            not_args_or_kwargs = (param.kind not in [param.VAR_POSITIONAL, param.VAR_KEYWORD])
            has_no_defaults = (param.default is param.empty)
            if has_no_defaults and not_args_or_kwargs:
                raise InvalidCallableException("Cannot schedule task that requires arguments")

        def do_delayed():
            time.sleep(delay)
            task()

        threading.Thread(target=do_delayed).start()

    def submit_at_rate(self, tasks : list[Callable], rate_per_second : float):
        for task in tasks:
            time.sleep(1/rate_per_second)
            self._schedule_task(task, delay=0)




class InvalidCallableException(Exception):
    """Exception raised when a callable with arguments is passed where none are expected."""
    pass





# Example usage
if __name__ == "__main__":
    def my_task():
        print(f"Task executed at {time.ctime()}. Now sleeping for 2 seconds")
        time.sleep(2)
        print(f'I work up at {time.ctime()}')

    def get_print_function(num : int):
        def print_num():
            print(num)
        return print_num


    def invalid_task(num : int):
        print(num)


    scheduler = TaskScheduler()
    # scheduler.submit_once(my_task, delay=2)
    # scheduler.submit_periodic(my_task, interval=1)
    scheduler.submit_once(task=invalid_task, delay=0)

    # scheduler.submit_at_rate(tasks=[get_print_function(i) for i in range(10)], rate_per_second=5)
    #
    # print(f'Sleepting at {time.ctime()}')
    # time.sleep(15)
