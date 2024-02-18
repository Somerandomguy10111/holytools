from __future__ import annotations
import logging
from hollarek.dev.log.log_settings import LogSettings


class LogTarget:
    FILE = "FILE"
    CONSOLE = "CONSOLE"


class Formatter(logging.Formatter):
    custom_file_name = 'custom_file_name'
    custom_line_no = 'custom_lineno'


    colors: dict = {
        logging.DEBUG: '\033[20m',
        logging.INFO: '\033[20m',
        logging.WARNING: '\033[93m',
        logging.ERROR: '\033[91m',
        logging.CRITICAL: '\x1b[31;1m'  # Bold Red
    }

    def __init__(self, settings : LogSettings, log_target : LogTarget):
        self.settings : LogSettings = settings
        self.log_target : LogTarget = log_target
        super().__init__()


    def format(self, record):
        log_fmt = "%(message)s"

        if self.settings.use_timestamp:
            custom_time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
            conditional_millis = f" {int(record.msecs)}ms" if self.settings.include_ms_in_timestamp else ""
            timestamp = f"[{custom_time}{conditional_millis}]"
            log_fmt = f"{timestamp}: {log_fmt}"

        if self.settings.include_call_location:
            filename = getattr(record, Formatter.custom_file_name, record.filename)
            lineno = getattr(record, Formatter.custom_line_no, record.lineno)
            log_fmt += f" {filename}:{lineno}"

        if self.log_target == LogTarget.CONSOLE:
            color_prefix = Formatter.colors.get(record.levelno, "")
            color_suffix = "\033[0m"
            log_fmt = color_prefix + log_fmt + color_suffix

        self._style._fmt = log_fmt
        return super().format(record)