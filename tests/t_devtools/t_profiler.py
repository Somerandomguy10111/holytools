import time

from holytools.devtools import Unittest
from holytools.devtools import Profiler

class TestProfiler(Unittest):
    def test_timed_scope(self):
        profiler = Profiler()

        with profiler.timed_scope(name=f'Test Scope'):
            time.sleep(1)

        report = profiler.make_report()
        self.assertIn('Test Scope', report)
        self.assertIn('Total Time', report)
        self.assertIn(f'1.0', report)

        print(report)

if __name__ == "__main__":
    TestProfiler.execute_all()