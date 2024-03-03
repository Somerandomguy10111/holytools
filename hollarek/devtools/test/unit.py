import logging
from typing import Optional
import unittest

from hollarek.logging import get_logger, LogSettings, Logger
from .runner import CustomTestRunner

# ---------------------------------------------------------

class Unittest(unittest.TestCase):
    _logger : Optional[Logger] = None

    def run(self, result=None):
        super().run(result)

    @classmethod
    def execute_all(cls, show_run_times: bool = False, show_details : bool = True):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = CustomTestRunner(logger=cls.get_logger(), show_run_times=show_run_times, show_details=show_details)
        results =  runner.run(suite)


        results.print_summary()


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


    def assertIsInstance(self, obj, cls, msg = None):
        if not isinstance(obj, cls):
            obj_str = str(obj).__repr__()
            cls_str = str(cls).__repr__()
            raise AssertionError(f'{obj_str} not an instance of {cls_str}')


    def assertTrue(self, expr, msg = None):
        raise AssertionError(f'Tested expression should be true')
