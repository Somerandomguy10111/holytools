import sys
import time
from unittest.mock import MagicMock
from holytools.events import Countdown
from holytools.devtools import Unittest

default_stderr = sys.stderr

class TestCountdown(Unittest):
    def setUp(self):
        self.duration = 0.5  # Duration set for quick tests
        self.on_expiration = MagicMock(return_value='expired')
        self.countdown = Countdown(duration=self.duration, on_expiration=self.on_expiration)

    def test_start(self):
        self.countdown.start()
        self.assertTrue(self.countdown.is_active())

    def test_restart(self):
        import io
        sys.stderr = io.StringIO()  # Redirect stdout to a StringIO object

        self.countdown.start()
        self.countdown.restart()
        self.assertTrue(self.countdown.is_active())

        time.sleep(1)
        logs = sys.stderr.getvalue()
        self.assertNotIn('KeyError',logs)

    def test_is_active(self):
        self.assertFalse(self.countdown.is_active())
        self.countdown.start()
        self.assertTrue(self.countdown.is_active())


    def test_finish(self):
        self.countdown.start()
        self.countdown.wait()
        #It needs little bit of time to release the lock
        time.sleep(0.05)
        self.assertFalse(self.countdown.is_active())


    def test_expiration_function_called(self):
        self.countdown.start()
        self.countdown.wait()  # Wait for the countdown to finish
        self.on_expiration.assert_called_once()

    def tearDown(self):
        sys.stderr = default_stderr

if __name__ == '__main__':
    TestCountdown.execute_all()
    time.sleep(2)
