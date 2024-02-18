from __future__ import annotations

import logging
from dataclasses import dataclass
from typing import Optional



@dataclass
class LogSettings:
    display_log_level: int = logging.INFO
    log_file_path: Optional[str] = None
    use_timestamp: bool = False
    include_call_location : bool = True
    include_ms_in_timestamp : bool = False

    def set_default_log_file(self, log_file: str):
        self.log_file_path = log_file

    def use_timestamps(self, enable_timestamps: bool):
        self.use_timestamp = enable_timestamps

    def set_log_file(self, log_file_path : str):
        self.log_file_path = log_file_path

