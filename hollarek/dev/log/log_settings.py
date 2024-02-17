from __future__ import annotations

import logging
from dataclasses import dataclass
from enum import Enum
from typing import Optional



class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


@dataclass
class LogSettings:
    display_log_level: LogLevel = LogLevel.INFO
    default_logfile_path: Optional[str] = None
    use_timestamp: bool = False
    include_call_location : bool = True
    include_ms_in_timestamp : bool = False

    def set_default_log_file(self, log_file: str):
        self.default_logfile_path = log_file

    def use_timestamps(self, enable_timestamps: bool):
        self.use_timestamp = enable_timestamps

    def set_log_file(self, log_file_path : str):
        self.default_logfile_path = log_file_path

    def set_display_level(self, display_log_level: LogLevel):
        self.display_log_level = display_log_level

