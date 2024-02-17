from __future__ import annotations

import logging
from typing import Optional

from hollarek.dev.log.formatter import ColoredFormatter
from hollarek.dev.log.log_settings import LogLevel, LogSettings

# ---------------------------------------------------------

def log(msg : str,
        log_level: LogLevel = LogLevel.INFO,
        log_file_path: Optional[str] = None):

    log_func = LogHandler.get_log_func(log_level=log_level,
                                        log_file_path=log_file_path)
    log_func(msg)


class LogHandler:
    _instance : Optional[LogHandler] = None
    _logger : Optional[logging.Logger] = None
    _settings : LogSettings = LogSettings()

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LogHandler, cls).__new__(cls)
        return cls._instance

    @classmethod
    def get_log_func(cls, log_level: LogLevel,
                     log_file_path: Optional[str] = None) -> callable:
        if not cls._logger:
            cls._logger = cls.make_logger(log_file_path=log_file_path)

        def log_func(msg: str):
            cls._logger.log(msg=msg, level=log_level.value)

        cls._log_func = log_func
        return log_func


    @classmethod
    def make_logger(cls):
        settings = cls._settings
        logger = logging.getLogger(__name__)
        logger.propagate = False
        logger.setLevel(cls._settings.display_log_level.value)

        formatter = ColoredFormatter(settings=settings)
        for h in cls.get_handlers():
            h.setFormatter(formatter)
            logger.addHandler(h)
        return logger


    @classmethod
    def update_settings(cls, new_settings : LogSettings):
        cls._settings = new_settings
        cls._logger = cls.make_logger()


    @classmethod
    def get_handlers(cls):
        console_handler = logging.StreamHandler()
        handlers = [console_handler]
        if cls._settings.log_file_path:
            handlers.append(logging.FileHandler(cls._settings.log_file_path))
        return handlers


if __name__ == "__main__":
    test_settings = LogSettings()
    test_settings.use_timestamps(True)
    log("This is a debug message", log_level=LogLevel.DEBUG)
    log("This is an info message", log_level=LogLevel.INFO)
    log("This is an warning message", log_level=LogLevel.WARNING)
    log("This is an error message.", log_level=LogLevel.ERROR)
    log("This is a critical error message!!", log_level=LogLevel.CRITICAL)