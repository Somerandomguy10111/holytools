# -import time
# -
# -from holytools.devtools import Unittest
# -from holytools.events import Timer
# -from unittest.mock import patch
# -
# -
# -def set_success(*args, **kwargs):
# -    TestTimer.msg = args[0]
# -
# -class TestTimer(Unittest):
# -    msg: bool = False
# -
# -    @patch('builtins.print', set_success)
# -    def test_measure_time(self):
# -        wait_time = 1
# -        @Timer.measure_time
# -        def wait():
# -            time.sleep(wait_time)
# -
# -        wait()
# -        self.assertTrue('1' in TestTimer.msg)
# -
# -    def tearDown(self):
# -        print(f'Test time msg = {TestTimer.msg}')
# -
# -if __name__ == '__main__':
# -    TestTimer.execute_all()
# \ No newline at end of file
