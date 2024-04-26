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
        """ Test that countdown starts correctly. """
        self.countdown.start()
        self.assertTrue(self.countdown.is_active())

    def test_restart(self):
        """ Test that countdown can be restarted. """
        import io
        sys.stderr = io.StringIO()  # Redirect stdout to a StringIO object

        self.countdown.start()
        self.countdown.restart()
        self.assertTrue(self.countdown.is_active())

        time.sleep(1)
        logs = sys.stderr.getvalue()
        self.assertNotIn('KeyError',logs)


    def test_is_active(self):
        """ Test is_active returns the correct status. """
        self.assertFalse(self.countdown.is_active())
        self.countdown.start()
        self.assertTrue(self.countdown.is_active())

    def test_finish(self):
        """ Test that finish waits for the countdown to complete. """
        self.countdown.start()
        self.countdown.finish()
        self.assertFalse(self.countdown.is_active())

    def test_get_output(self):
        """ Test getting the output after countdown. """
        self.countdown.start()
        self.countdown.finish()  # Ensure countdown has finished
        output = self.countdown.get_output()
        self.assertEqual(output, 'expired')

    def test_expiration_function_called(self):
        """ Test that the on_expiration function is called correctly. """
        self.countdown.start()
        self.countdown.finish()  # Wait for the countdown to finish
        self.on_expiration.assert_called_once()

    def tearDown(self):
        sys.stderr = default_stderr

if __name__ == '__main__':
    TestCountdown.execute_all()
    time.sleep(2)