from __future__ import annotations
import logging
from dataclasses import dataclass, field
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
    instance : Optional[LogSettings] = None
    default_log_level: LogLevel = LogLevel.INFO
    display_log_level: LogLevel = LogLevel.INFO
    default_logfile_path: Optional[str] = None
    use_timestamp: bool = False

    colors: dict = field(default_factory=lambda: {
        LogLevel.DEBUG: '\033[94m',  # Blue
        LogLevel.INFO: '\033[92m',  # Green
        LogLevel.WARNING: '\033[93m',  # Yellow
        LogLevel.ERROR: '\033[91m',  # Red
        LogLevel.CRITICAL: '\033[95m'  # Magenta
    })

    def __post_init__(self):
        self.set_display_level(display_log_level=self.display_log_level)

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(LogSettings, cls).__new__(cls)
        return cls.instance

    def set_level(self, log_level: LogLevel):
        self.default_log_level = log_level

    def set_default_log_file(self, log_file: str):
        self.default_logfile_path = log_file

    def use_timestamps(self, enable_timestamps: bool):
        self.use_timestamp = enable_timestamps

    def set_log_file(self, log_file_path : str):
        self.default_logfile_path = log_file_path

    def set_display_level(self, display_log_level: LogLevel):
        self.display_log_level = display_log_level
        logging.basicConfig(level=self.display_log_level.value)


    @classmethod
    def get_log_func(cls, log_level : LogLevel,
                     log_file_path : Optional[str] = None) -> callable:

        settings = cls.instance
        logger = logging.getLogger(__name__)
        logger.propagate = False
        logger.setLevel(settings.default_log_level.value)

        formatter = ColoredFormatter()
        for h in cls.get_handlers(log_file_path=log_file_path or settings.default_logfile_path):
            h.setLevel(settings.default_log_level.value)
            h.setFormatter(formatter)
            logger.addHandler(h)

        def log_func(msg : str):
            logger.log(msg=msg,level=log_level.value)

        return log_func


    @staticmethod
    def get_handlers(log_file_path : str):
        console_handler = logging.StreamHandler()
        handlers = [console_handler]
        if log_file_path:
            handlers.append(logging.FileHandler(log_file_path))
        return handlers


class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = f"{LogSettings.instance.colors[LogLevel(record.levelno)]}%(levelname)s: %(message)s\033[0m"
        if LogSettings.instance.use_timestamp:
            log_fmt = f"%(asctime)s - {log_fmt}"
        if LogSettings.instance.default_logfile_path:
            log_fmt = f"{log_fmt} (%(filename)s:%(lineno)d)"
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
    log("This is an info message", log_level=LogLevel.WARNING)
