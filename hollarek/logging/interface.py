from typing import Optional
import inspect
from .logger import Logger
from .log_settings import LogSettings
from .logger import LoggerFactory
import devtools as externalDevtools
from enum import *
# ---------------------------------------------------------

class Loggable:
    _default_logger : Optional[Logger] = None

    def __init__(self, settings : LogSettings = LogSettings()):
        self.logger = get_logger(settings, name = self.__class__.__name__)
        self.log = self.logger.log


def get_logger(settings: LogSettings = LogSettings(), name : Optional[str] = None) -> Logger:
    if name is None:
        frame = inspect.currentframe().f_back
        module = inspect.getmodule(frame)
        if module:
            name = module.__name__
        else:
            name = "unnamed_logger"

    return LoggerFactory.make_logger(name=name,settings=settings)


def update_defaults(settings : LogSettings):
    LoggerFactory.set_defaults(settings=settings)


def debug(obj):
    externalDevtools.debug(obj)


class Color(Enum):
    BLACK = '\033[30m'
    RED = '\033[31m'
    GREEN = '\033[32m'
    YELLOW = '\033[33m'
    BLUE = '\033[34m'
    MAGENTA = '\033[35m'
    CYAN = '\033[36m'
    WHITE = '\033[37m'

def add_color(msg : str, color : Color) -> str:
    return f"{color.value}{msg}\033[0m"


