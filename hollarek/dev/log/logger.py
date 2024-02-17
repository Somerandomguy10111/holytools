import logging
from dataclasses import dataclass, field
from enum import Enum
from typing import Optional


# Enum for log levels
class LogLevel(Enum):
    DEBUG = logging.DEBUG
    INFO = logging.INFO
    WARNING = logging.WARNING
    ERROR = logging.ERROR
    CRITICAL = logging.CRITICAL


# Dataclass singleton for log settings
@dataclass
class LogSettings:
    instance = None
    log_level: LogLevel = LogLevel.INFO
    default_logfile_path: Optional[str] = None
    use_timestamp: bool = False

    colors: dict = field(default_factory=lambda: {
        LogLevel.DEBUG: '\033[94m',  # Blue
        LogLevel.INFO: '\033[92m',  # Green
        LogLevel.WARNING: '\033[93m',  # Yellow
        LogLevel.ERROR: '\033[91m',  # Red
        LogLevel.CRITICAL: '\033[95m'  # Magenta
    })

    def __new__(cls, *args, **kwargs):
        if not cls.instance:
            cls.instance = super(LogSettings, cls).__new__(cls)
        return cls.instance

    def set_level(self, log_level: LogLevel):
        self.log_level = log_level

    def set_default_log_file(self, log_file: str):
        self.default_logfile_path = log_file

    def enable_timestamp(self, enable: bool):
        self.use_timestamp = enable

    def set_log_file(self, log_file_path : str):
        self.default_logfile_path = log_file_path


# Custom formatter for colored logs
class ColoredFormatter(logging.Formatter):
    def format(self, record):
        log_fmt = f"{LogSettings.instance.colors[LogLevel(record.levelno)]}%(levelname)s: %(message)s\033[0m"
        if LogSettings.instance.use_timestamp:
            log_fmt = f"%(asctime)s - {log_fmt}"
        if LogSettings.instance.default_logfile_path:
            log_fmt = f"{log_fmt} (%(filename)s:%(lineno)d)"
        self._style._fmt = log_fmt
        return super().format(record)


# Log function
def log(msg : str,
        log_level: LogLevel = LogLevel.INFO,
        log_file: Optional[str] = None):
    settings = LogSettings.instance
    logger = logging.getLogger(__name__)
    logger.setLevel(settings.log_level.value)
    effective_log_file = log_file or settings.log_file

    # Set up file logging only if a log file is specified
    if effective_log_file:
        handler = logging.FileHandler(effective_log_file)
        handler.setLevel(settings.log_level.value)
        handler.setFormatter(ColoredFormatter())
        logger.addHandler(handler)
        logger.addHandler(handler)

    log_method = {
        LogLevel.DEBUG: logger.debug,
        LogLevel.INFO: logger.info,
        LogLevel.WARNING: logger.warning,
        LogLevel.ERROR: logger.error,
        LogLevel.CRITICAL: logger.critical
    }.get(log_level, logger.info)

    log_method(msg)


# Example usage
if __name__ == "__main__":
    test_settings = LogSettings()
    test_settings.enable_timestamp(True)
    test_settings.set_level(LogLevel.DEBUG)
    log("This is a debug message")
    log("This is an info message")
