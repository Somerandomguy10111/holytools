import unittest
import time
from hollarek.devtools import Unittest
from hollarek.events import TaskScheduler, Task, InvalidCallableException  # Adjust import as necessary

class TestTaskScheduler(Unittest):
    def setUp(self):
        self.scheduler = TaskScheduler()

    def test_submit_once_runs_correctly(self):
        output = []
        def task():
            output.append('task run')

        self.scheduler.submit_once(task, delay=1)
        time.sleep(1.5)  # Allow some time for the task to run
        self.assertEqual(output, ['task run'])

    def test_submit_periodic_runs_multiple_times(self):
        output = []
        def task():
            output.append('periodic task run')
            if len(output) > 2:
                self.scheduler.cancel_all()

        self.scheduler.submit_periodic(task, interval=1)
        time.sleep(3.5)  # Allow enough time for the periodic task to run multiple times
        self.assertTrue(len(output) > 2)

    def test_cancel_all_tasks(self):
        output = []
        def task():
            output.append('should not run')

        t = self.scheduler.submit_once(task, delay=1)
        self.scheduler.cancel_all()
        time.sleep(1.5)  # Wait to see if the task runs
        self.assertEqual(output, [])

    def test_submit_with_invalid_callable(self):
        def task_with_args(x):
            pass

        with self.assertRaises(InvalidCallableException):
            self.scheduler.submit_once(task_with_args, delay=1)

    def test_task_cancellation(self):
        output = []
        def task():
            output.append('should run')

        t = self.scheduler.submit_once(task, delay=0.5)
        time.sleep(0.1)
        t.is_canceled = True
        time.sleep(0.6)  # Allow more time than the task delay
        self.assertEqual(output, [])  # Output should be empty as the task was canceled

    def test_scheduler_activity(self):
        self.assertFalse(self.scheduler.is_active())
        self.scheduler.submit_once(lambda: time.sleep(0.1), delay=0.1)
        time.sleep(0.2)  # Allow time for the task to be scheduled and finish
        self.assertFalse(self.scheduler.is_active())

if __name__ == '__main__':
    TestTaskScheduler.execute_all()