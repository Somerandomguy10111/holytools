import logging
import unittest
from enum import Enum
from logging import Logger


class TestStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"


class CustomTestResult(unittest.TestResult):
    test_spaces = 50
    status_spaces = 20

    def __init__(self, logger : Logger, stream, descriptions, verbosity):
        super().__init__(stream=stream, descriptions=descriptions, verbosity=verbosity)
        self.logger = logger

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

        self.logger.log(msg=f'{test_name:<{self.test_spaces}}:  {reason:<{self.status_spaces}}',level=log_level)


class CustomTestRunner(unittest.TextTestRunner):
    def __init__(self, logger : Logger):
        super().__init__(resultclass=None)
        self.logger : Logger = logger


    def run(self, test):
        result = CustomTestResult(logger=self.logger,
                                  stream=self.stream,
                                  descriptions=self.descriptions,
                                  verbosity=2)
        test(result)
        result.printErrors()

        return result
