from dataclasses import dataclass
from enum import Enum
from unittest import TestCase
from hollarek.logging import LogLevel


class CaseStatus(Enum):
    SUCCESS = "SUCCESS"
    ERROR = "ERROR"
    FAIL = "FAIL"
    SKIPPED = "SKIPPED"

    def get_log_level(self) -> LogLevel:
        status_to_logging = {
            CaseStatus.SUCCESS: LogLevel.INFO,
            CaseStatus.ERROR: LogLevel.CRITICAL,
            CaseStatus.FAIL: LogLevel.ERROR,
            CaseStatus.SKIPPED: LogLevel.INFO
        }
        return status_to_logging[self]


@dataclass
class CaseResult:
    runtime_sec : float
    name : str
    status : CaseStatus



def get_case_name(test : TestCase) -> str:
    full_test_name = test.id()
    parts = full_test_name.split('.')
    last_parts = parts[-2:]
    test_name = '.'.join(last_parts)
    return test_name