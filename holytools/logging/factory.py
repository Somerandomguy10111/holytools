from __future__ import annotations

import logging
import sys
from dataclasses import dataclass
from enum import Enum
from logging import Logger
from typing import Optional


# ---------------------------------------------------------


class LoggerFactory:
    @classmethod
    def make_logger(cls, name : str,
                    log_fpath : Optional[str] = None,
                    include_timestamp : bool = True,
                    include_location : bool = False,
                    threshold : int = logging.INFO) -> Logger:
        logger = logging.getLogger(name=name)
        logger.setLevel(threshold)
        formatting = Formatting(print_timestamp=include_timestamp, print_location=include_location)

        console_handler = logging.StreamHandler(sys.stdout)
        console_formatter = Formatter(log_target=LogTarget.CONSOLE, formatting=formatting)
        console_handler.setFormatter(console_formatter)
        logger.addHandler(console_handler)

        if log_fpath:
            file_handler = logging.FileHandler(log_fpath)
            file_formatter = Formatter(log_target=LogTarget.FILE, formatting=formatting)
            file_handler.setFormatter(file_formatter)
            logger.addHandler(file_handler)

        return logger


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

    def __init__(self, log_target : LogTarget, formatting : Formatting):
        self.formatting : Formatting = formatting
        self.log_target : LogTarget = log_target
        super().__init__()


    def format(self, record):
        log_fmt = "%(message)s"

        if self.formatting.print_timestamp:
            custom_time = self.formatTime(record, "%Y-%m-%d %H:%M:%S")
            timestamp = f"[{custom_time}]"
            log_fmt = f"{timestamp}: {log_fmt}"

        if self.formatting.print_location:
            log_fmt += f'\t\t| Location: File "{record.pathname}:{record.lineno}"'

        if self.log_target == LogTarget.CONSOLE:
            color_prefix = Formatter.colors.get(record.levelno, "")
            color_suffix = "\033[0m"
            log_fmt = color_prefix + log_fmt + color_suffix

        self._style._fmt = log_fmt
        return super().format(record)



class Loggable:
    def __init__(self):
        self.logger = LoggerFactory.make_logger(name=self.__class__.__name__)

    def log(self, msg : str, level : int = logging.INFO):
        self.logger.log(level=level, msg=msg)

    def warning(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.WARNING
        self.logger.log(msg=msg, *args, **kwargs)

    def error(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.ERROR
        self.logger.log(msg=msg, *args, **kwargs)

    def critical(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.CRITICAL
        self.logger.log(msg=msg, *args, **kwargs)

    def info(self, msg : str, *args, **kwargs):
        kwargs['level'] = logging.INFO
        self.logger.log(msg=msg, *args, **kwargs)


class LogTarget(Enum):
    FILE = "FILE"
    CONSOLE = "CONSOLE"

@dataclass
class Formatting:
    print_timestamp : bool
    print_location : bool
