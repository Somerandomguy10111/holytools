import os
import time
import traceback
import unittest
from typing import Optional
from unittest import TestCase
import linecache

from hollarek.logging import LogLevel, Logger
from .case import CaseStatus, CaseResult, get_case_name
from .settings import TestSettings
# ---------------------------------------------------------


class Result(unittest.TestResult):
    test_spaces = 50
    status_spaces = 10
    runtime_space = 10

    def __init__(self, logger : Logger, settings : TestSettings, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.test_settings : TestSettings = settings

        self.log = logger.log
        self.start_times : dict[str, float] = {}
        self.case_results : list[CaseResult] = []

        self.print_header(f'  Test suite for \"{self.__class__.__name__}\"  ')

    def stopTestRun(self):
        super().stopTestRun()
        self.print_summary()

    def startTest(self, test):
        super().startTest(test)
        self.log(msg = f'------> {get_case_name(test=test)[:self.test_spaces]} ', level=LogLevel.INFO)
        self.start_times[test.id()] = time.time()

    def addSuccess(self, test):
        super().addSuccess(test)
        self.report(test, CaseStatus.SUCCESS)

    def addError(self, test, err):
        super().addError(test, err)
        self.report(test, CaseStatus.ERROR, err)

    def addFailure(self, test, err):
        super().addFailure(test, err)
        self.report(test, CaseStatus.FAIL, err)

    def addSkip(self, test, reason):
        super().addSkip(test, reason)
        self.report(test, CaseStatus.SKIPPED)

    # ---------------------------------------------------------
    # logging

    def report(self, test : TestCase, status: CaseStatus, err : Optional[tuple] = None):
        case_result = CaseResult(test=test, status=status, runtime=self.get_runtime(test=test))
        self.case_results.append(case_result)

        conditional_err_msg = f'\n{self.get_err_details(err)}' if err and self.test_settings.show_details else ''
        finish_log_msg = f'Status: {status.value}{conditional_err_msg}\n'
        self.log(msg=finish_log_msg, level=status.get_log_level())


    def get_runtime(self, test : TestCase) -> Optional[float]:
        test_id = test.id()
        if test_id in self.start_times:
            time_in_sec =  time.time() - self.start_times[test_id]
            return round(time_in_sec, 3)
        else:
            self.log(f'Couldnt find start time of test {test_id}. Current start_times : {self.start_times}', level=LogLevel.ERROR)


    def print_summary(self):
        self.print_header(msg=f' Summary ', seperator='-')
        for case in self.case_results:
            level = case.status.get_log_level()
            self.log(f'{self.get_name_msg(case)}{self.get_status_msg(case)}{self.get_runtime_msg(case)}', level=level)
        self.log(self.get_final_status())
        self.print_header(msg=f'')

    def get_name_msg(self, result : CaseResult) -> str:
        return f'{result.name[:self.test_spaces-4]:<{self.test_spaces}}'

    def get_status_msg(self, result : CaseResult) -> str:
        return f'{result.status.value:<{self.status_spaces}}'

    def get_runtime_msg(self, result : CaseResult)-> str:
        runtime_str = f'{result.runtime_sec}s'
        return f'{runtime_str:^{self.runtime_space}}' if self.test_settings.show_runtimes else ''

    def print_header(self, msg: str, seperator : str = '='):
        total_len = self.test_spaces + self.status_spaces
        total_len += self.runtime_space if self.test_settings.show_runtimes else 0
        line_len = max(total_len- len(msg), 0)
        lines = seperator * int(line_len / 2.)
        self.log(f'{lines}{msg}{lines}')


    @staticmethod
    def get_err_details(err) -> str:
        err_class, err_instance, err_traceback = err
        tb_list = traceback.extract_tb(err_traceback)
        relevant_tb = [tb for tb in tb_list if not os.path.dirname(unittest.__file__) in tb.filename]

        result = ''
        for frame in relevant_tb:
            file_path = frame.filename
            line_number = frame.lineno
            tb_str = (f'File "{file_path}", line {line_number}, in {frame.name}\n'
                      f'    {linecache.getline(file_path, line_number).strip()}')
            result += f'{err_class.__name__}: {err_instance}\n{tb_str}'
        return result


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