from __future__ import annotations

import logging

from hollarek.dev.log.log_level import LogLevel


class ColoredFormatter(logging.Formatter):
    colors: dict = {
        LogLevel.DEBUG: '\033[20m',
        LogLevel.INFO: '\033[20m',
        LogLevel.WARNING: '\033[93m',
        LogLevel.ERROR: '\033[91m',
        LogLevel.CRITICAL: '\x1b[31;1m'  # Bold Red
    }

    def __init__(self, use_timestamp: bool = True,
                       include_ms_in_timestamp : bool = False,
                       include_call_location : bool = True):
        super().__init__()
        self.print_timestamp : bool = use_timestamp
        self.include_ms_in_timestamp : bool = include_ms_in_timestamp
        self.include_call_location : bool = include_call_location

    def format(self, record):
        log_fmt = "%(message)s"

        if self.print_timestamp:
            custom_time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
            conditional_millis = f"{int(record.msecs)}ms" if self.include_ms_in_timestamp else ""
            timestamp = f"[{custom_time}{conditional_millis}]"
            log_fmt = f"{timestamp}: {log_fmt}"

        if self.include_call_location:
            log_fmt = f"{log_fmt} (%(filename)s:%(lineno)d)"

        color_prefix = ColoredFormatter.colors.get(LogLevel(record.levelno), "")
        color_suffix = "\033[0m"
        log_fmt = color_prefix + log_fmt + color_suffix

        self._style._fmt = log_fmt
        return super().format(record)
