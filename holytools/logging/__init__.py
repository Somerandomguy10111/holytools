

from .factory import Loggable, LoggerFactory
from .modifier import LoggingModifier

from datetime import datetime
def get_timestamp():
    return datetime.now().strftime("%Y-%m-%d_%H%M")

import logging
class LogLevel:
    INFO = logging.INFO
    DEBUG = logging.DEBUG
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL