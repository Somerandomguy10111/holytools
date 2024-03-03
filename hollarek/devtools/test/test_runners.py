import os
import unittest
from enum import Enum
import time
from hollarek.logging import Logger, LogLevel
from unittest import TestCase
from typing import Optional
import traceback

class TestStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"


class CustomTestResult(unittest.TestResult):
    test_spaces = 50
    status_spaces = 20

    def __init__(self, logger : Logger, show_run_times : bool, show_details : bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logger.log
        self.start_times = {}
        self.show_run_times = show_run_times
        self.show_details : bool = show_details

    def startTest(self, test):
        super().startTest(test)
        test_info = f' {self.get_test_name(test=test)} '
        self.log(msg = f'------>{test_info}', level=LogLevel.INFO)

        self.start_times[test.id()] = time.time()

    def addSuccess(self, test):
        super().addSuccess(test)
        self.report(test, TestStatus.SUCCESS)

    def addError(self, test, err):
        super().addError(test, err)
        self.report(test, TestStatus.ERROR, err)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.report(test, TestStatus.FAIL, err)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.report(test, TestStatus.SKIPPED)

    def report(self, test : TestCase, test_status: TestStatus, err : Optional[tuple] = None):
        run_time_str = self.get_run_time_str(test.id()) if self.show_run_times else ''

        # log_message = f'{test_info:<{self.test_spaces}}: {test_status.value:<{self.status_spaces}} {run_time_str}'
        finish_log_msg = f'Status: {test_status.value}'
        if err and self.show_details:
            finish_log_msg += f'\n{self.get_err_dails(err)}'
        finish_log_msg += '\n'

        log_level = self.status_to_level(test_status)
        self.log(msg=finish_log_msg, level=log_level)


    @staticmethod
    def get_err_dails(err) -> str:
        import linecache

        err_class, err_instance, err_traceback = err
        tb_list = traceback.extract_tb(err_traceback)
        project_frames = [frame for frame in tb_list if os.getcwd() in frame.filename]

        relevant_frame = project_frames[-1] if project_frames else tb_list[-1]
        file_path = relevant_frame.filename
        line_number = relevant_frame.lineno
        function_name = relevant_frame.name
        error_line = linecache.getline(file_path, line_number).strip()

        tb_str = f'File "{file_path}", line {line_number}, in {function_name}\n    {error_line}'

        return f'{err_class.__name__}: {err_instance}\n{tb_str}'


    def get_run_time_str(self, test_id : str) -> str:
        if test_id in self.start_times:
            run_time = time.time() - self.start_times[test_id]
            base = f'{run_time:.2f}s'
            runtime_str = f'{base:<{self.status_spaces}}'
            return runtime_str
        else:
            self.log(f'Couldnt find start time of test {test_id}. Current start_times : {self.start_times}', level=LogLevel.ERROR)
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
    def __init__(self, logger : Logger, show_run_times : bool = True, show_details : bool = True):
        super().__init__(resultclass=None)
        self.logger : Logger = logger
        self.show_run_times = show_run_times
        self.show_details : bool = show_details


    def run(self, test):
        result = CustomTestResult(logger=self.logger,
                                  stream=self.stream,
                                  show_run_times=self.show_run_times,
                                  show_details=self.show_details,
                                  descriptions=self.descriptions,
                                  verbosity=2)
        test(result)
        result.printErrors()

        return result