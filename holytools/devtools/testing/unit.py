from __future__ import annotations

import inspect
import logging
import time
import unittest
import unittest.mock
from logging import Logger
from typing import Optional, Callable

from holytools.devtools.testing.case import CaseStatus, Report
from holytools.devtools.testing.suiteresult import SuiteResuult
from holytools.logging import LoggerFactory

from .runner import Runner
from .suiteresult import UnitTestCase


# ---------------------------------------------------------

class Unittest(UnitTestCase):
    _logger : Logger = None

    @classmethod
    def ready(cls) -> Unittest:
        instance = cls()
        instance.setUpClass()
        instance.setUp()
        return instance

    @classmethod
    def execute_all(cls, manual_mode : bool = True, trace_resourcewarning : bool = False):
        suite = unittest.TestLoader().loadTestsFromTestCase(cls)
        runner = Runner(logger=cls.get_logger(), is_manual=manual_mode, test_name=cls.__name__)
        tracemalloc_depth = 10 if trace_resourcewarning else 0
        results = runner.run(testsuite=suite, tracemalloc_depth=tracemalloc_depth)

        return results

    @classmethod
    def execute_statistiically(cls, reps : int, min_success_rate : float):
        test_names = unittest.TestLoader().getTestCaseNames(cls)
        case_reports = []

        for tn in test_names:
            current_case = cls(tn)
            start_time = time.time()
            suite_result = cls._run_several(reps=reps, name=tn)
            is_successful = [True if c.status == CaseStatus.SUCCESS else False for c in suite_result.reports]

            first_report = suite_result.reports[0]
            if first_report.status == CaseStatus.ERROR:
                suite_result.mute = False
                suite_result.log_test_start(case=current_case)
                suite_result.log(first_report.get_view(), level=first_report.get_log_level())
                case_reports.append(first_report)
                continue

            num_successful = sum(is_successful)
            total = len(is_successful)
            ratio = sum(is_successful) / len(is_successful)

            suite_result.mute = False
            suite_result.log_test_start(case=current_case)
            spaces = 13
            suite_result.log(f'{"Success rate:":<{spaces}} {num_successful/total*100}%')

            status = CaseStatus.SUCCESS if ratio >= min_success_rate else CaseStatus.FAIL
            statistical_case = Report(name=f'{cls.__name__}.{tn}', status=status, runtime=round(time.time() - start_time,3))
            status_msg = f'{"Status:":<{spaces}} {status}\n'
            suite_result.log(msg=status_msg, level=statistical_case.get_log_level())

            case_reports.append(statistical_case)


        result = SuiteResuult(logger=cls.get_logger(), testsuite_name=cls.__name__)
        result.reports = case_reports
        result.log_summary()


    @classmethod
    def _run_several(cls, name : str, reps : int):
        suite = unittest.TestSuite()
        current_case = cls(name)
        for _ in range(reps):
            suite.addTest(current_case)

        runner = Runner(logger=cls.get_logger(), test_name=cls.__name__)
        results = runner.run(testsuite=suite,mute=True)


        return results

    @classmethod
    def get_logger(cls) -> Logger:
        if not cls._logger:
            cls._logger = LoggerFactory.get_logger(include_location=False, include_timestamp=False, name=cls.__name__, use_stdout=True, log_fpath=cls.log_fpath())
        return cls._logger


    @classmethod
    def log_fpath(cls) -> Optional[str]:
        return None

    @classmethod
    def log(cls, msg : str, level : int = logging.INFO):
        cls.get_logger().log(msg=f'{msg}', level=level)

    def warning(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.WARNING
        self._logger.log(msg=msg, *args, **kwargs)

    def error(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.ERROR
        self._logger.log(msg=msg, *args, **kwargs)

    def critical(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.CRITICAL
        self._logger.log(msg=msg, *args, **kwargs)

    def info(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.INFO
        self._logger.log(msg=msg, *args, **kwargs)


    # ---------------------------------------------------------
    # assertions

    def assertEqual(self, first : object, second : object, msg : Optional[str] = None):
        if not first == second:
            first_str = str(first).__repr__()
            second_str = str(second).__repr__()
            if msg is None:
                msg = (f'Tested expressions should match:'
                       f'\nFirst : {first_str} ({type(first)})'
                       f'\nSecond: {second_str} ({type(second)})')
            raise AssertionError(msg)

    def assertSame(self, first : dict, second : dict, msg : Optional[str] = None):
        """Checks whether contents of dicts first and second are the same"""
        for key in first:
            first_obj = first[key]
            second_obj = second[key]
            self.assertSameElementary(type(first_obj), type(second_obj))
            if isinstance(first_obj, dict):
                self.assertSame(first_obj, second_obj, msg=msg)
            elif isinstance(first_obj, list):
                for i in range(len(first_obj)):
                    self.assertSameElementary(first_obj[i], second_obj[i])
            else:
                self.assertSameElementary(first_obj, second_obj)

    def assertSameElementary(self, first : object, second : object):
        if isinstance(first, float) and isinstance(second, float):
            self.assertSameFloat(first, second)
        else:
            self.assertEqual(first, second)

    @staticmethod
    def assertSameFloat(first : float, second : float, msg : Optional[str] = None):
        if first != first:
            same_float = second != second
        else:
            same_float = first == second
        if not same_float:
            first_str = str(first).__repr__()
            second_str = str(second).__repr__()
            if msg is None:
                msg = (f'Tested floats should match:'
                       f'\nFirst : {first_str} ({type(first)})'
                       f'\nSecond: {second_str} ({type(second)})')
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


    @staticmethod
    def patch_module(original: type | Callable, replacement: type | Callable):
        module_path = inspect.getmodule(original).__name__
        qualified_name = original.__qualname__
        frame = inspect.currentframe().f_back
        caller_module = inspect.getmodule(frame)

        try:
            # corresponds to "from [caller_module] import [original]
            _ = getattr(caller_module, qualified_name)
            full_path = f"{caller_module.__name__}.{qualified_name}"
        except Exception:
            # corresponds to import [caller_module].[original]
            full_path = f"{module_path}.{qualified_name}"

        # print(f'Full path = {full_path}')
        def decorator(func):
            return unittest.mock.patch(full_path, replacement)(func)

        return decorator


