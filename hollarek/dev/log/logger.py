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
    _instance : Optional[LogSettings] = None
    _default_log_level: LogLevel = LogLevel.INFO
    _display_log_level: LogLevel = LogLevel.INFO
    _default_logfile_path: Optional[str] = None
    _use_timestamp: bool = False

    _logger : Optional[logging.Logger] = None

    def __post_init__(self):
        self.set_display_level(display_log_level=self._display_log_level)

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LogSettings, cls).__new__(cls)
        return cls._instance

    def set_level(self, log_level: LogLevel):
        self._default_log_level = log_level

    def set_default_log_file(self, log_file: str):
        self._default_logfile_path = log_file

    def use_timestamps(self, enable_timestamps: bool):
        self._use_timestamp = enable_timestamps

    def set_log_file(self, log_file_path : str):
        self._default_logfile_path = log_file_path

    def set_display_level(self, display_log_level: LogLevel):
        self._display_log_level = display_log_level
        logging.basicConfig(level=self._display_log_level.value)


    @classmethod
    def get_log_func(cls, log_level : LogLevel,
                          log_file_path : Optional[str] = None) -> callable:
        if not cls._logger:
            cls._logger = cls.get_logger(log_file_path=log_file_path)

        def log_func(msg : str):
            cls._logger.log(msg=msg,level=log_level.value)
        cls._log_func = log_func

        return log_func

    @classmethod
    def get_logger(cls, log_file_path : str):
        settings = cls._instance
        logger = logging.getLogger(__name__)
        logger.propagate = False
        logger.setLevel(settings._default_log_level.value)

        formatter = ColoredFormatter()
        for h in cls.get_handlers(log_file_path=log_file_path or settings._default_logfile_path):
            h.setLevel(settings._default_log_level.value)
            h.setFormatter(formatter)
            logger.addHandler(h)
        return logger


    @staticmethod
    def get_handlers(log_file_path : str):
        console_handler = logging.StreamHandler()
        handlers = [console_handler]
        if log_file_path:
            handlers.append(logging.FileHandler(log_file_path))
        return handlers


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


def log(msg : str,
        log_level: LogLevel = LogLevel.INFO,
        log_file_path: Optional[str] = None):

    log_func = LogSettings.get_log_func(log_level=log_level,
                                        log_file_path=log_file_path)
    log_func(msg)


# Example usage
if __name__ == "__main__":
    test_settings = LogSettings()
    test_settings.use_timestamps(True)
    test_settings.set_level(LogLevel.DEBUG)
    log("This is a debug message", log_level=LogLevel.DEBUG)
    log("This is an info message", log_level=LogLevel.INFO)
    log("This is an warning message", log_level=LogLevel.WARNING)
    log("This is an error message.", log_level=LogLevel.ERROR)
    log("This is a critical error message!!", log_level=LogLevel.CRITICAL)
