import time

from holytools.devtools import Unittest
from holytools.devtools import Profiler
p = Profiler(print_on_exit=True)

# -------------------------------------

class TestProfiler(Unittest):
    def test_timed_scope(self):
        profiler = Profiler()

        with profiler.profiled_scope(name=f'Test Scope'):
            time.sleep(1)

        report = profiler.scope_report()
        self.assertIn('Test Scope', report)
        self.assertIn('Total Time', report)
        self.assertIn(f'1.0', report)

        print(report)

class ExampleClass:
    def some_method(self):
        with p.profiled_scope(name='phase1'):
            time.sleep(0.1)

        with p.profiled_scope(name='phase2'):
            time.sleep(0.1)
            self.subroutine()
        with p.profiled_scope(name='phase3'):
            time.sleep(0.1)

    @staticmethod
    def subroutine():
        with p.profiled_scope(name='phase2_subroutine'):
            time.sleep(0.05)



if __name__ == "__main__":
    TestProfiler.execute_all()

    instance = ExampleClass()
    instance.some_method()
    instance.some_method()
    instance.subroutine()
