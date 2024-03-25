import unittest

from typing import Optional
from hollarek.core.logging import get_logger, LogSettings, Logger, LogLevel
from .configurable_unit import  ConfigurableTest
from .results import Results, DisplayOptions

# ---------------------------------------------------------


class Runner(unittest.TextTestRunner):
    def __init__(self, logger : Logger, settings : DisplayOptions, is_manual : bool = False):
        super().__init__(resultclass=None)
        self.logger : Logger = logger
        self.display_options : DisplayOptions = settings
        self.manual_mode : bool = is_manual

    def run(self, test) -> Results:
        result = Results(logger=self.logger,
                         stream=self.stream,
                         settings=self.display_options,
                         descriptions=self.descriptions,
                         verbosity=2,
                         manual_mode=self.manual_mode)
        test(result)
        result.printErrors()

        return result


class Unittest(ConfigurableTest):
    _logger : Logger = None

    @classmethod
    def execute_all(cls, manual_mode : bool = True, settings : DisplayOptions = DisplayOptions()):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = Runner(logger=cls.get_logger(), settings=settings, is_manual=manual_mode)
        results =  runner.run(suite)
        results.print_summary()
        return results

    @classmethod
    def get_logger(cls) -> Logger:
        if not cls._logger:
            cls._logger = get_logger(settings=LogSettings(include_call_location=False, timestamp=False), name=cls.__name__)
        return cls._logger

    @classmethod
    def log(cls, msg : str, level : LogLevel = LogLevel.INFO):
        cls.get_logger().log(msg, level=level)

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

    def assertFalse(self, expr : bool, msg : Optional[str] = None):
        if expr:
            if msg is None:
                msg = f'Tested expression should be false'
            raise AssertionError(msg)




