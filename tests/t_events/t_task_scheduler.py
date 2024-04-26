import time
from holytools.devtools import Unittest
from holytools.events import TaskScheduler, InvalidCallableException

class TestTaskScheduler(Unittest):
    def setUp(self):
        self.scheduler = TaskScheduler()

    def test_submit_once(self):
        output = []
        def task():
            output.append('task run')

        self.scheduler.submit_once(task, delay=1)
        self.assertNotEqual(output, ['task run'])
        time.sleep(1.1)
        self.assertEqual(output, ['task run'])


    def test_cancel(self):
        output = []
        def task():
            output.append('should not run')

        self.scheduler.submit_once(task, delay=1)
        self.scheduler.cancel_all()
        time.sleep(1.5)
        self.assertEqual(output, [])


    def test_submit_invalid_task(self):
        def task_with_args(x):
            _ = x
            pass

        with self.assertRaises(InvalidCallableException):
            self.scheduler.submit_once(task_with_args, delay=1)


    def test_submit_periodic(self):
        output = []
        def task():
            output.append('periodic task run')

        interval = 0.5
        n = 3
        self.scheduler.submit_periodic(task, interval=interval)
        time.sleep(interval*n+0.1)
        self.assertTrue(len(output) == n)


    def test_scheduler_activity(self):
        self.assertFalse(self.scheduler.is_active())
        self.scheduler.submit_once(lambda: time.sleep(0.1), delay=0.05)
        time.sleep(0.2)
        self.assertFalse(self.scheduler.is_active())


    def tearDown(self):
        self.scheduler.cancel_all()

if __name__ == '__main__':
    TestTaskScheduler.execute_all()