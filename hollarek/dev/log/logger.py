from __future__ import annotations
import logging, inspect
from typing import Optional, Union
from logging import Logger as BaseLogger

from hollarek.dev.log.formatter import Formatter, LogTarget
from hollarek.dev.log.log_settings import LogSettings, LogLevel
# ---------------------------------------------------------


def get_logger(settings: Optional[LogSettings] = None,
                          name : Optional[str] = None) -> Logger:
    if name is None:
        frame = inspect.currentframe().f_back
        module = inspect.getmodule(frame)
        if module:
            name = module.__name__
        else:
            name = "unnamed_logger"

    return LoggerFactory.make_logger(name=name,settings=settings)


def update_defaults(new_settings : LogSettings):
    LoggerFactory.set_defaults(settings=new_settings)


class Logger(BaseLogger):
    def log(self, msg : str, level : Union[int, LogLevel] = LogLevel.INFO, *args, **kwargs):
        if isinstance(level, LogLevel):
            level = level.value

        super().log(msg=msg, level=level, *args, **kwargs)


class LoggerFactory:
    _default_settings : LogSettings = LogSettings()

    @classmethod
    def set_defaults(cls, settings : LogSettings):
        cls._default_settings = settings

    @classmethod
    def make_logger(cls, name : str, settings : Optional[LogSettings] = None) -> Logger:
        settings = settings or cls._default_settings

        logger = Logger(name=name)
        logger.propagate = False
        logger.setLevel(settings.log_level_threshold)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(Formatter(settings=settings, log_target=LogTarget.CONSOLE))
        logger.addHandler(console_handler)

        if settings.log_file_path:
            file_handler = logging.FileHandler(settings.log_file_path)
            file_handler.setFormatter(Formatter(settings=settings, log_target=LogTarget.FILE))
            logger.addHandler(file_handler)

        return logger



if __name__ == "__main__":
    the_settings = LogSettings(use_timestamp=True, include_ms_in_timestamp=True, log_file_path='test_suite')
    test_logger = get_logger()
    log = test_logger.log

    log("This is a debug message", level=logging.DEBUG)
    log("This is an info message", level=logging.INFO)
    log("This is a warning message", level=logging.WARNING)
    log("This is an error message.", level=logging.ERROR)
    log("This is a critical error message!!", level=logging.CRITICAL)

