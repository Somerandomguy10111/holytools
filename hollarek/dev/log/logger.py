from __future__ import annotations
import logging
import inspect
import os
from typing import Optional, Callable
from copy import copy

from hollarek.dev.log.formatter import Formatter, LogTarget
from hollarek.dev.log.log_settings import LogLevel, LogSettings

# ---------------------------------------------------------


def log(msg : str, level : LogLevel = LogLevel.INFO):
    log_func  = LogFactory.get_default_log_func()
    log_func(msg=msg,level=level.value)


def get_log_func(settings: Optional[LogSettings] = None) -> Callable[[str, LogLevel], None]:
    if not settings:
        return copy(LogFactory.get_default_log_func())

    return LogFactory.get_log_func(settings=settings)


class LogFactory:
    _default_log_func : Optional[callable] = None
    _default_settings : LogSettings = LogSettings()

    @classmethod
    def get_default_log_func(cls) -> callable:
        if not cls._default_log_func:
            cls._default_log_func = get_log_func(settings=cls._default_settings)
        
        return cls._default_log_func

    @classmethod
    def update_default_settings(cls, settings : LogSettings):
        cls._default_settings = settings
        cls._default_log_func = get_log_func(settings=cls._default_settings)


    @classmethod
    def get_log_func(cls, settings : LogSettings) -> callable:
        logger = cls.make_logger(settings=settings)

        def log_func(msg : str, *args, **kwargs):
            if settings.include_call_location:
                caller_frame = inspect.currentframe().f_back.f_back
                info = inspect.getframeinfo(caller_frame)
                fname = os.path.basename(info.filename)
                caller_datails = f"{fname}:{info.lineno} in {info.function}"
                msg = f"{msg}{caller_datails}"

            logger.log(msg=msg, *args, **kwargs)

        cls._log_func = log_func
        return log_func


    @classmethod
    def make_logger(cls, settings: LogSettings):
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