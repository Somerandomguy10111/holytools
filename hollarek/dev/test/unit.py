import unittest
import json
from hollarek.misc import get_salvaged_json
from hollarek.dev import log
from enum import Enum
import logging

from hollarek.dev.log import get_logger, update_default_log_settings, LogSettings
# ---------------------------------------------------------

class TestStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"


class CustomTestResult(unittest.TestResult):
    test_spaces = 60
    status_spaces = 20

    def addSuccess(self, test):
        super().addSuccess(test)
        self.log(test, "SUCCESS", TestStatus.SUCCESS)

    def addError(self, test, err):
        super().addError(test, err)
        self.log(test, "ERROR", TestStatus.ERROR)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.log(test, "FAIL", TestStatus.FAIL)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.log(test, "SKIPPED", TestStatus.SKIPPED)

    def log(self, test, reason : str, test_status: TestStatus):
        status_to_logging = {
            TestStatus.SUCCESS: logging.INFO,
            TestStatus.ERROR: logging.CRITICAL,
            TestStatus.FAIL: logging.ERROR,
            TestStatus.SKIPPED: logging.INFO
        }
        log_level = status_to_logging[test_status]
        full_test_name = test.id()
        parts = full_test_name.split('.')
        last_parts = parts[-2:]
        test_name = '.'.join(last_parts)


        log(f'{test_name:<{self.test_spaces}}{reason:<{self.status_spaces}}', log_level)


class Unittest(unittest.TestCase):
    def setUp(self):
        self.valid_str = '{"key": "value"}'
        self.broken_str_newline = '{"key": "value with a new\nline"}'
        self.broken_str_tab = '{"key": "value with a tab\t"}'
        self.broken_str_multiple = '{"key": "new\nline and\ttab"}'

    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            self.fail(f"Test failed with error: {e}")

    def test_no_control_characters(self):
        repaired_str = get_salvaged_json(self.valid_str)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['key'], "value")

    def test_single_newline(self):
        repaired_str = get_salvaged_json(self.broken_str_newline)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['key'], "value with a new\nline")

    def test_tab_and_backslash(self):
        repaired_str = get_salvaged_json(self.broken_str_tab)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['key'], "value with a tab\t")

    def test_multiple_control_characters(self):
        repaired_str = get_salvaged_json(self.broken_str_multiple)
        parsed_json = json.loads(repaired_str)
        self.assertEqual(parsed_json['keyy'], "new\nline and\ttab")

    @classmethod
    def execute_tests(cls):
        lines = '-' * 30
        log(f'{lines}  Test suite for {cls.__name__}  {lines}')
        module_header, status_header = 'Test module', 'Status'
        log(f'{module_header:^{CustomTestResult.test_spaces}}{status_header:<{CustomTestResult.status_spaces}}\n')
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = unittest.TextTestRunner(resultclass=CustomTestResult, verbosity=2)
        runner.run(suite)


if __name__ == "__main__":
    update_default_log_settings(new_settings=LogSettings(include_call_location=False))
    Unittest.execute_tests()


    log_func = get_logger()