import unittest
from hollarek.logging import get_logger, LogSettings, Logger
from .runner import Runner
from .settings import TestSettings
# ---------------------------------------------------------

class Unittest(unittest.TestCase):
    @classmethod
    def execute_all(cls, settings : TestSettings = TestSettings()):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = Runner(logger=cls.get_logger(),settings=settings)
        results =  runner.run(suite)
        results.print_summary()

    @classmethod
    def get_logger(cls) -> Logger:
        return get_logger(settings=LogSettings(include_call_location=False, use_timestamp=False), name=cls.__name__)

    # ---------------------------------------------------------
    # assertions

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
