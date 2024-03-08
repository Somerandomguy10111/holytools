import time
import unittest
from hollarek.logging import get_logger, LogSettings, Logger
from .runner import Runner
from .settings import TestSettings
from abc import abstractmethod
from typing import Optional
# ---------------------------------------------------------

class Unittest(unittest.TestCase):
    @classmethod
    @abstractmethod
    def setUpClass(cls):
        pass

    @classmethod
    def execute_all(cls, settings : TestSettings = TestSettings()):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = Runner(logger=cls.get_logger(),settings=settings)
        results =  runner.run(suite)
        results.print_summary()

    @classmethod
    def get_logger(cls) -> Logger:
        return get_logger(settings=LogSettings(call_location=False, timestamp=False), name=cls.__name__)

    # ---------------------------------------------------------
    # assertions

    def assertEqual(self, first : object, second : object, msg : Optional[str] = None):
        if not first == second:
            first_str = str(first).__repr__()
            second_str =str(second).__repr__()
            if msg is None:
                msg = f'{first_str} != {second_str}'
            raise AssertionError(msg)


    def assertIn(self, member : object, container, msg : Optional[str] = None):
        if not member in container:
            member_str = str(member).__repr__()
            container_str = str(container).__repr__()
            if msg is None:
                msg = f'{member_str} not in {container_str}'
            raise AssertionError(msg)


    def assertIsInstance(self, obj : object, cls : type, msg : Optional[str] = None):
        if not isinstance(obj, cls):
            obj_str = str(obj).__repr__()
            cls_str = str(cls).__repr__()
            if msg is None:
                msg = f'{obj_str} not an instance of {cls_str}'
            raise AssertionError(msg)


    def assertTrue(self, expr : bool, msg : Optional[str] = None):
        if not expr:
            if msg is None:
                msg = f'Tested expression should be true'
            raise AssertionError(msg)
