from __future__ import annotations
import logging
from logging import Logger
from typing import Optional
from copy import copy

from hollarek.dev.log.formatter import Formatter, LogTarget
from hollarek.dev.log.log_settings import LogLevel, LogSettings
import inspect, os
# ---------------------------------------------------------



def log(msg : str, level : LogLevel = LogLevel.INFO):
    frame = inspect.currentframe().f_back
    info = inspect.getframeinfo(frame)
    fname = os.path.basename(info.filename)  # Get just the file name
    lineno = info.lineno  # Get the line number

    logger = LoggerFactory.get_default_logger()
    logger.log(msg=msg, level=level.value, extra={Formatter.custom_file_name: fname,
                                                  Formatter.custom_line_no: lineno})

def get_logger(settings: Optional[LogSettings] = None) -> Logger:
    if not settings:
        return copy(LoggerFactory.get_default_logger())

    return LoggerFactory.make_logger(settings=settings)


def update_default_log_settings(new_settings : LogSettings):
    LoggerFactory.update_default_settings(settings=new_settings)


class LoggerFactory:
    _default_logger : Optional[Logger] = None
    _default_settings : LogSettings = LogSettings()

    @classmethod
    def get_default_logger(cls) -> Logger:
        if not cls._default_logger:
            cls._default_logger = get_logger(settings=cls._default_settings)
        
        return cls._default_logger

    @classmethod
    def update_default_settings(cls, settings : LogSettings):
        cls._default_settings = settings
        cls._default_logger = get_logger(settings=cls._default_settings)


    @classmethod
    def make_logger(cls, settings: LogSettings) -> Logger:
        settings = settings
        logger = logging.getLogger(__name__)
        logger.propagate = False
        logger.setLevel(settings.display_log_level.value)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(Formatter(settings=settings, log_target=LogTarget.CONSOLE))
        logger.addHandler(console_handler)

        if settings.log_file_path:
            file_handler = logging.FileHandler(settings.log_file_path)
            file_handler.setFormatter(Formatter(settings=settings, log_target=LogTarget.FILE))
            logger.addHandler(file_handler)

        return logger



if __name__ == "__main__":
    the_settings = LogSettings(use_timestamp=True, include_ms_in_timestamp=True, log_file_path='test')

    log("This is a debug message", level=LogLevel.DEBUG)
    log("This is an info message", level=LogLevel.INFO)
    log("This is an warning message", level=LogLevel.WARNING)
    log("This is an error message.", level=LogLevel.ERROR)
    log("This is a critical error message!!", level=LogLevel.CRITICAL)