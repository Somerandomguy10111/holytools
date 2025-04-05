from .factory import Loggable, LoggerFactory
from .tools import LoggingTools
from .manager import LoggerManager


import logging
class LogLevel:
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL