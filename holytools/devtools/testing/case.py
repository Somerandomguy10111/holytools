
from __future__ import annotations

import linecache
import logging
import os
import traceback
import unittest
from dataclasses import dataclass
from typing import Optional


class UnitTestCase(unittest.TestCase):
    def __init__(self, *args):
        super().__init__(*args)
        self.is_manual_mode : bool = False

    def set_is_manual(self):
        self.is_manual_mode = True

    def get_is_manual(self):
        return self.is_manual_mode

    def get_name(self) -> str:
        full_test_name = self.id()
        parts = full_test_name.split('.')
        last_parts = parts[-2:]
        test_name = '.'.join(last_parts)
        return test_name


@dataclass
class Report:
    runtime : float
    name : str
    status : str
    err : Optional[Exception] = None

    def get_log_level(self) -> int:
        status_to_logging : dict[str, int] = {
            CaseStatus.SUCCESS: logging.INFO,
            CaseStatus.ERROR: logging.CRITICAL,
            CaseStatus.FAIL: logging.ERROR,
            CaseStatus.SKIPPED : logging.INFO
        }
        return status_to_logging[self.status]


    def get_view(self) -> str:
        conditional_err_msg = f'\n{self._get_err_details(self.err)}' if self.err else ''
        return f'Status: {self.status}{conditional_err_msg}\n'


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


class CaseStatus:
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    FAIL = 'FAIL'
    SKIPPED = 'SKIPPED'
