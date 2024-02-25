import unittest
from enum import Enum
import time
from hollarek.dev.log import Logger, LogLevel
from unittest import TestCase

class TestStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"


class CustomTestResult(unittest.TestResult):
    test_spaces = 50
    status_spaces = 20

    def __init__(self, logger : Logger, show_run_times : bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger : Logger = logger
        self.start_times = {}
        self.show_run_times = show_run_times


    def startTest(self, test):
        super().startTest(test)
        self.start_times[test.id()] = time.time()

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


    def log(self, test : TestCase, reason : str, test_status: TestStatus):
        test_name = self.get_test_name(test=test)
        run_time_str = self.get_run_time_str(test.id()) if self.show_run_times else ''

        log_message = f'{test_name:<{self.test_spaces}}: {reason:<{self.status_spaces}} {run_time_str}'
        log_level = self.status_to_level(test_status)
        self.logger.log(msg=log_message, level=log_level)


    def get_run_time_str(self, test_id : str) -> str:
        if test_id in self.start_times:
            run_time = time.time() - self.start_times[test_id]
            base = f'{run_time:.2f}s'
            runtime_str = f'{base:<{self.status_spaces}}'
            return runtime_str
        else:
            self.logger.log(f'Couldnt find start time of test {test_id}. Current start_times : {self.start_times}', level=LogLevel.ERROR)
            return ''


    @staticmethod
    def get_test_name(test) -> str:
        full_test_name = test.id()
        parts = full_test_name.split('.')
        last_parts = parts[-2:]
        test_name = '.'.join(last_parts)[:CustomTestResult.test_spaces]
        return test_name

    @staticmethod
    def status_to_level(test_status : TestStatus) -> LogLevel:
        status_to_logging = {
            TestStatus.SUCCESS: LogLevel.INFO,
            TestStatus.ERROR: LogLevel.CRITICAL,
            TestStatus.FAIL: LogLevel.ERROR,
            TestStatus.SKIPPED: LogLevel.INFO
        }
        return status_to_logging[test_status]


class CustomTestRunner(unittest.TextTestRunner):
    def __init__(self, logger : Logger, show_run_times : bool):
        super().__init__(resultclass=None)
        self.logger : Logger = logger
        self.show_run_times = show_run_times


    def run(self, test):
        result = CustomTestResult(logger=self.logger,
                                  stream=self.stream,
                                  show_run_times=self.show_run_times,
                                  descriptions=self.descriptions,
                                  verbosity=2)
        test(result)
        result.printErrors()

        return result
