from __future__ import annotations
import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional




@dataclass
class LogSettings:
    log_level_threshold: int = logging.INFO
    log_file_path: Optional[str] = None
    use_timestamp: bool = True
    include_call_location : bool = False
    include_ms_in_timestamp : bool = False


class LogLevel(Enum):
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL
