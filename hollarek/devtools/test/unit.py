import logging
from typing import Optional
import unittest

from hollarek.logging import get_logger, LogSettings, Logger
from abc import abstractmethod

from .test_runners import UnittestResult, CustomTestRunner
# ---------------------------------------------------------

class Unittest(unittest.TestCase):
    _logger : Optional[Logger] = None


    def run(self, result=None):
        super().run(result)

    @classmethod
    def execute_all(cls, show_run_times: bool = False, show_details : bool = True):
        cls._print_header()

        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = CustomTestRunner(logger=cls.get_logger(), show_run_times=show_run_times, show_details=show_details)
        results =  runner.run(suite)

        cls._print_header(msg=f' Summary ')
        results.print_summary()
        cls._print_header(msg=f'')


    @classmethod
    def _print_header(cls, msg : Optional[str] = None):
        if msg is None:
            msg = f'  Test suite for \"{cls.__name__}\"  '
        line_len = max(UnittestResult.test_spaces + UnittestResult.status_spaces - len(msg), 0)
        lines = '=' * int(line_len/2.)
        cls.log(f'{lines}{msg}{lines}')



    @classmethod
    def get_logger(cls) -> Logger:
        if not cls._logger:
            cls._logger = get_logger(settings=LogSettings(include_call_location=False, use_timestamp=False), name=cls.__name__)
        return cls._logger

    @classmethod
    def log(cls,msg : str):
        logger = cls.get_logger()
        logger.log(msg=msg,level=logging.INFO)


    def assertEqual(self, first, second, *args, **kwargs):
        if not first == second:
            first_str = str(first).__repr__()
            second_str =str(second).__repr__()
            raise AssertionError(f'{first_str} != {second_str}')

    def assertIn(self, member, container, msg = None):
        if not member in container:
            member_str = str(member).__repr__()
            container_str = str(container).__repr__()
            raise AssertionError(f'{member_str} not in {container_str}')