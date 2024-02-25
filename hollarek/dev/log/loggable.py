from .logger import get_logger, LogSettings, LogLevel, Logger
from typing import Optional

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