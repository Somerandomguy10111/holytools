import logging
from logging import Logger
from typing import Optional
import unittest
from unittest.result import TestResult

from hollarek.dev.log import get_logger, LogSettings
from abc import ABC, abstractmethod

from .test_runners import CustomTestResult, CustomTestRunner
# ---------------------------------------------------------

class Unittest(unittest.TestCase, ABC):
    _logger : Optional[Logger] = None


    @classmethod
    @abstractmethod
    def setUpClass(cls):
        pass


    def run(self, result=None):
        try:
            super().run(result)
        except Exception as e:
            self.fail(f"Test failed with error: {e}")

    @classmethod
    def execute_all(cls, show_run_times: bool = False):
        cls._print_header()
        results = cls._get_test_results(show_run_times=show_run_times)
        summary = cls._get_final_status_msg(result=results)
        cls.log(summary)


    @classmethod
    def _get_test_results(cls, show_run_times : bool) -> TestResult:
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = CustomTestRunner(logger=cls._logger, show_run_times=show_run_times)
        return runner.run(suite)

    @classmethod
    def _print_header(cls):
        name_info = f'  Test suite for \"{cls.__name__}\"  '
        line_len = max(CustomTestResult.test_spaces + CustomTestResult.status_spaces - len(name_info), 0)
        lines = '-' * int(line_len/2.)
        cls.log(f'{lines}{name_info}{lines}\n')


    @staticmethod
    def _get_final_status_msg(result) -> str:
        total_tests = result.testsRun
        errors = len(result.errors)
        failures = len(result.failures)
        successful_tests = total_tests - errors - failures

        RED = '\033[91m'
        GREEN = '\033[92m'
        RESET = '\033[0m'
        CHECKMARK = '✓'
        CROSS = '❌'

        if errors + failures == 0:
            final_status = f"{GREEN}\n{CHECKMARK} {successful_tests}/{total_tests} tests ran successfully!{RESET}"
        else:
            final_status = f"{RED}\n{CROSS} {total_tests - successful_tests}/{total_tests} tests had errors or failures!{RESET}"

        return final_status


    @classmethod
    def get_logger(cls) -> Logger:
        if not cls._logger:
            cls._logger = get_logger(settings=LogSettings(include_call_location=False), name=cls.__name__)
        return cls._logger

    @classmethod
    def log(cls,msg : str):
        logger = cls.get_logger()
        logger.log(msg=msg,level=logging.INFO)


