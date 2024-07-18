import os
import sys
from typing import Callable

from .factory import Loggable, LoggerFactory
from .modifier import LoggingModifier

from datetime import datetime
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H%M")


def mute(func : Callable) -> Callable:
    def muted_func(*args, **kwargs):
        stdout, stderr = sys.stdout, sys.stderr
        sys.stdout = open(os.devnull, 'w')
        sys.stderr = open(os.devnull, 'w')
        result = func(*args, **kwargs)
        sys.stdout, sys.stderr = stdout, stderr
        return result
    return muted_func


import logging
class LogLevel:
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL