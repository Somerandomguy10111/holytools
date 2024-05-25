import linecache
import os
import traceback
import uuid
from typing import Optional
from enum import Enum
import inspect
from .log_settings import LogSettings, LogLevel
from .customlogger import CustomLogger, LoggerFactory
# ---------------------------------------------------------

class Loggable:
    _default_logger : Optional[CustomLogger] = None

    def __init__(self, settings : LogSettings = LogSettings()):
        self.logger = make_logger(settings, name = str(uuid.uuid4()))
        self.log = self.logger.log

    def warning(self, msg : str, *args, **kwargs):
        kwargs['level'] = LogLevel.WARNING
        self.logger.log(msg=msg, *args, **kwargs)

    def error(self, msg : str, *args, **kwargs):
        kwargs['level'] = LogLevel.ERROR
        self.logger.log(msg=msg, *args, **kwargs)

    def critical(self, msg : str, *args, **kwargs):
        kwargs['level'] = LogLevel.CRITICAL
        self.logger.log(msg=msg, *args, **kwargs)

    def info(self, msg : str, *args, **kwargs):
        kwargs['level'] = LogLevel.INFO
        self.logger.log(msg=msg, *args, **kwargs)


def make_logger(settings: LogSettings = LogSettings(), name : Optional[str] = None) -> CustomLogger:
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



import types
def get_limited_stacktrace(err: Exception, excluded_modules : list[types.ModuleType]) -> str:
    err_class, err_instance, err_traceback = err.__class__, err, err.__traceback__
    tb_list = traceback.extract_tb(err_traceback)
    def is_relevant(tb):
        in_exclued_module = any([os.path.dirname(module.__file__) in tb.filename for module in excluded_modules])
        return not in_exclued_module

    err_msg = ''
    relevant_tb = [tb for tb in tb_list if is_relevant(tb)]
    if relevant_tb:
        err_msg = "\nEncountered error during training routine. Relevant stacktrace:"
        for frame in relevant_tb:
            file_path = frame.filename
            line_number = frame.lineno
            tb_str = (f'File "{file_path}", line {line_number}, in {frame.name}\n'
                      f'    {linecache.getline(file_path, line_number).strip()}')
            err_msg += f'\n{err_class.__name__}: {err_instance}\n{tb_str}'

    return err_msg
