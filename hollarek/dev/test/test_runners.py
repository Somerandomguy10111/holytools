import logging
import unittest
from enum import Enum

from hollarek.dev import log


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
        test_name = '.'.join(last_parts)[:CustomTestResult.test_spaces]

        log(f'{test_name:<{self.test_spaces}}| {reason:<{self.status_spaces}}', log_level)


class CustomTestRunner(unittest.TextTestRunner):
    def run(self, test):
        result = CustomTestResult(self.stream, self.descriptions, self.verbosity)
        test(result)
        result.printErrors()

        return result
