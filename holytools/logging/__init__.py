import logging

from .log_settings import LogSettings
from .factory import Loggable, LoggerFactory
from .modifier import LoggingModifier

class LogLevel:
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL