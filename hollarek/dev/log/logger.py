from __future__ import annotations
import copy
import logging
from logging import Logger
from typing import Optional
import inspect
import os

from hollarek.dev.log.formatter import Formatter, LogTarget
from hollarek.dev.log.log_settings import LogLevel, LogSettings

# ---------------------------------------------------------

def log(msg : str,
        log_level: LogLevel = LogLevel.INFO,
        log_file_path: Optional[str] = None):

    _ = log_file_path

    log_func = LogHandler.get_log_func()
    log_func(msg=msg,
             level=log_level.value)


def update_logger(new_settings : LogSettings):
    LogHandler._settings = new_settings
    LogHandler._logger = LogHandler.make_logger()


class LogHandler:
    _instance : Optional[LogHandler] = None
    _logger : Optional[Logger] = None
    _settings : LogSettings = LogSettings()


    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(LogHandler, cls).__new__(cls)
        return cls._instance


    @classmethod
    def get_log_func(cls) -> callable:
        if not cls._logger:
            cls._logger = cls.make_logger()

        def log_func(msg : str, *args, **kwargs):
            if copy.copy(cls._settings.include_call_location):
                caller_frame = inspect.currentframe().f_back.f_back
                info = inspect.getframeinfo(caller_frame)
                fname = os.path.basename(info.filename)
                caller_datails = f"{fname}:{info.lineno} in {info.function}"
                msg = f" {msg}{caller_datails}"

            cls._logger.log(msg=msg, *args, **kwargs)

        cls._log_func = log_func
        return log_func


    @classmethod
    def make_logger(cls):
        settings = cls._settings
        logger = logging.getLogger(__name__)
        logger.propagate = False
        logger.setLevel(cls._settings.display_log_level.value)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(Formatter(settings=settings, log_target=LogTarget.CONSOLE))
        logger.addHandler(console_handler)

        if cls._settings.log_file_path:
            file_handler = logging.FileHandler(cls._settings.log_file_path)
            file_handler.setFormatter(Formatter(settings=settings, log_target=LogTarget.FILE))
            logger.addHandler(file_handler)

        return logger



if __name__ == "__main__":
    the_settings = LogSettings(use_timestamp=True, include_ms_in_timestamp=True, log_file_path='test')
    update_logger(new_settings=the_settings)

    log("This is a debug message", log_level=LogLevel.DEBUG)
    log("This is an info message", log_level=LogLevel.INFO)
    log("This is an warning message", log_level=LogLevel.WARNING)
    log("This is an error message.", log_level=LogLevel.ERROR)
    log("This is a critical error message!!", log_level=LogLevel.CRITICAL)