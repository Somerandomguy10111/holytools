from typing import Optional
import inspect
from .logger import Logger
from .settings import LogSettings, LogLevel
from .logger import LoggerFactory

# ---------------------------------------------------------

class Loggable:
    _default_logger : Optional[Logger] = None

    def __init__(self, settings : LogSettings = LogSettings()):
        self.logger = get_logger(settings, name = self.__class__.__name__)

    def log(self,msg : str, level : LogLevel = LogLevel.INFO):
        self.logger.log(msg=msg, level=level)

    @classmethod
    def cls_log(cls, msg : str, level : LogLevel = LogLevel.INFO):
        logger = cls._get_default_logger()
        logger.log(msg=msg, level=level)

    @classmethod
    def _get_default_logger(cls):
        if not cls._default_logger:
            cls._default_logger = get_logger(settings=LogSettings(), name=cls.__name__)
        return cls._default_logger


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
