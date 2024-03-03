import os
import time
import traceback
import unittest
from dataclasses import dataclass
from enum import Enum
from typing import Optional
from unittest import TestCase
from hollarek.logging import LogLevel, Logger
# ---------------------------------------------------------

class TestStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"

    def get_log_level(self) -> LogLevel:
        status_to_logging = {
            TestStatus.SUCCESS: LogLevel.INFO,
            TestStatus.ERROR: LogLevel.CRITICAL,
            TestStatus.FAIL: LogLevel.ERROR,
            TestStatus.SKIPPED: LogLevel.INFO
        }
        return status_to_logging[self]


@dataclass
class SingleResult:
    runtime_sec : float
    name : str
    status : TestStatus


class UnittestResult(unittest.TestResult):
    test_spaces = 50
    status_spaces = 10
    runtime_space = 10

    def __init__(self, logger : Logger, show_run_times : bool, show_details : bool, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.log = logger.log
        self.start_times = {}
        self.show_run_times = show_run_times
        self.show_details : bool = show_details
        self.results : list[SingleResult] = []
        self.print_header(f'  Test suite for \"{self.__class__.__name__}\"  ')

    def stopTestRun(self):
        super().stopTestRun()
        self.print_summary()

    def startTest(self, test):
        super().startTest(test)
        self.log(msg = f'------> {self.get_test_name(test=test)} ', level=LogLevel.INFO)
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
        test_result = SingleResult(runtime_sec=self.get_runtime_in_sec(test_id=test.id()), name=self.get_test_name(test), status=test_status)
        self.results.append(test_result)

        conditional_err_msg = f'\n{self.get_err_details(err)}' if err and self.show_details else ''
        finish_log_msg = f'Status: {test_status.value}{conditional_err_msg}\n'
        self.log(msg=finish_log_msg, level=test_status.get_log_level())


    def print_summary(self):
        self.print_header(msg=f' Summary ', seperator='-')
        for result in self.results:
            level = result.status.get_log_level()
            rounded_runtime = f'{round(result.runtime_sec,3)}s'
            conditional_runtime_info = f'{rounded_runtime:^{self.runtime_space}}' if self.show_run_times else ''
            self.log(f'{result.name:<{self.test_spaces}}{result.status.value:<{self.status_spaces}}{conditional_runtime_info}',level=level)
        self.log(self.get_final_status())
        self.print_header(msg=f'')


    def print_header(self, msg: str, seperator : str = '='):
        total_len = UnittestResult.test_spaces + UnittestResult.status_spaces
        total_len += UnittestResult.runtime_space if self.show_run_times else 0
        line_len = max(total_len- len(msg), 0)
        lines = seperator * int(line_len / 2.)
        self.log(f'{lines}{msg}{lines}')


    def get_runtime_in_sec(self, test_id : str) -> Optional[float]:
        if test_id in self.start_times:
            return time.time() - self.start_times[test_id]
        else:
            self.log(f'Couldnt find start time of test {test_id}. Current start_times : {self.start_times}', level=LogLevel.ERROR)


    @staticmethod
    def get_err_details(err) -> str:
        import linecache
        err_class, err_instance, err_traceback = err
        tb_list = traceback.extract_tb(err_traceback)
        project_frames = [frame for frame in tb_list if os.getcwd() in frame.filename]

        relevant_frame = project_frames[-1] if project_frames else tb_list[-1]
        file_path = relevant_frame.filename
        line_number = relevant_frame.lineno
        tb_str = (f'File "{file_path}", line {line_number}, in {relevant_frame.name}\n'
                  f'    {linecache.getline(file_path, line_number).strip()}')
        return f'{err_class.__name__}: {err_instance}\n{tb_str}'


    def get_final_status(self) -> str:
        num_total = self.testsRun
        num_unsuccessful = len(self.errors)+ len(self.failures)

        RED = '\033[91m'
        GREEN = '\033[92m'
        RESET = '\033[0m'
        CHECKMARK = '✓'
        CROSS = '❌'

        if num_unsuccessful == 0:
            final_status = f"{GREEN}\n{CHECKMARK} {num_total}/{num_total} tests ran successfully!{RESET}"
        else:
            final_status = f"{RED}\n{CROSS} {num_unsuccessful}/{num_total} tests had errors or failures!{RESET}"

        return final_status

    @staticmethod
    def get_test_name(test) -> str:
        full_test_name = test.id()
        parts = full_test_name.split('.')
        last_parts = parts[-2:]
        test_name = '.'.join(last_parts)[:UnittestResult.test_spaces]
        return test_name
