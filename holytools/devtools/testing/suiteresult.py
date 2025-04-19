from __future__ import annotations

import linecache
import logging
import os
import time
import traceback
import unittest
from typing import Optional
from unittest import TestCase, TestResult

from holytools.devtools.testing.case import UnitTestCase, CaseReport


# ---------------------------------------------------------

class SuiteResuult(TestResult):
    test_spaces = 50
    status_spaces = 10
    runtime_space = 10

    def __init__(self, logger : logging.Logger, testsuite_name: str, manual_mode : bool = False, mute : bool = False, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logger = logger
        self.case_reports : list[CaseReport] = []
        self.start_times : dict[str, float] = {}
        self.is_manual : bool = manual_mode
        self.testsuite_name = testsuite_name
        self.mute : bool = mute
    #
    # def startTestRun(self):
    #     super().startTestRun()
    #     self.log_header(f'  Test suite: \"{self.testsuite_name}\"  ')
    #
    def startTest(self, case : UnitTestCase):
        super().startTest(case)
        self.on_case_start(case=case)

    def stopTestRun(self):
        self.log_summary()
        super().stopTestRun()

    # noinspection PyTypeChecker
    def addSuccess(self, case : UnitTestCase):
        super().addSuccess(case)
        self.on_case_finish(case, CaseReport.SUCCESS)

    # noinspection PyTypeChecker
    def addError(self, case : UnitTestCase, err):
        super().addError(case, err)
        self.on_case_finish(case, CaseReport.ERROR, err)

    # noinspection PyTypeChecker
    def addFailure(self, case : UnitTestCase, err):
        super().addFailure(case, err)
        self.on_case_finish(case, CaseReport.FAIL, err)

    # noinspection
    def addSkip(self, case : UnitTestCase, reason):
        super().addSkip(case, reason)
        self.on_case_finish(case, CaseReport.SKIPPED)

    # ---------------------------------------------------------
    # case reports

    def on_case_start(self, case : UnitTestCase):
        if self.is_manual:
            case.set_is_manual()
        self.log_test_start(case=case)
        self.start_times[case.id()] = time.time()

    def on_case_finish(self, case : UnitTestCase, status: str, err : Optional[tuple] = None):
        report = CaseReport(name=case.get_name(), status=status, runtime=self._get_runtime(case))
        self.case_reports.append(report)

        conditional_err_msg = f'\n{self._get_err_details(err)}' if err else ''
        finish_log_msg = f'Status: {status}{conditional_err_msg}\n'
        self.log(msg=finish_log_msg, level=report.get_log_level())


    def _get_runtime(self, test : TestCase) -> Optional[float]:
        test_id = test.id()
        if test_id in self.start_times:
            time_in_sec =  time.time() - self.start_times[test_id]
            return round(time_in_sec, 3)
        else:
            self.log(msg=f'Couldnt find start time of test {test_id}. Current start_times : {self.start_times}',
                     level=logging.ERROR)

    @staticmethod
    def _get_err_details(err) -> str:
        err_class, err_instance, err_traceback = err
        tb_list = traceback.extract_tb(err_traceback)

        def is_relevant(tb):
            not_unittest = not os.path.dirname(unittest.__file__) in tb.filename
            not_custom_unittest = not os.path.dirname(__file__) in tb.filename
            return not_unittest and not_custom_unittest

        user_tb = [tb for tb in tb_list if is_relevant(tb)]

        result = ''
        relevant_tb = user_tb if not len(user_tb) == 0 else tb_list
        for frame in relevant_tb:
            file_path = frame.filename
            line_number = frame.lineno
            tb_str = (f'File "{file_path}", line {line_number}, in {frame.name}\n'
                      f'    {linecache.getline(file_path, line_number).strip()}')
            result += f'{err_class.__name__}: {err_instance}\n{tb_str}'
        return result

    # ---------------------------------------------------------
    # logging


    def log_summary(self):
        self.get_header(msg=' Summary ', seperator='-')
        for case in self.case_reports:
            level = case.get_log_level()
            name_msg = f'{case.name[:self.test_spaces - 4]:<{self.test_spaces}}'
            status_msg = f'{case.status:<{self.status_spaces}}'
            runtime_str = f'{case.runtime_sec}s'
            runtime_msg = f'{runtime_str:^{self.runtime_space}}'

            self.log(msg=f'{name_msg}{status_msg}{runtime_msg}', level=level)
        self.log(self.get_final_status())
        self.log(self.get_header(msg=''))


    def get_header(self, msg: str, seperator : str = '=') -> str:
        total_len = self.test_spaces + self.status_spaces
        total_len += self.runtime_space
        line_len = max(total_len- len(msg), 0)
        lines = seperator * int(line_len / 2.)
        return f'{lines}{msg}{lines}'


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

    def log_test_start(self, case : UnitTestCase):
        self.log(msg=f'------> {case.get_name()[:self.test_spaces]} ', level=logging.INFO)

    def log(self, msg : str, level : int = logging.INFO):
        if not self.mute:
            self.logger.log(msg=msg, level=level)