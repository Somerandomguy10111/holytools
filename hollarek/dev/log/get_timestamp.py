from __future__ import annotations

import logging
from datetime import datetime
from typing import Optional
from abc import ABC, abstractmethod

class LoggerTemplate(ABC):
    @abstractmethod
    def log(self):
        pass


class Logger:
    _instance : Optional[Logger] = None
    _is_initialized : bool = False

    def __new__(cls, *args, **kwargs):
        if not Logger._is_initialized:
            return super().__new__(cls)
        return Logger._instance

    def __init__(self, use_timestamp : bool = True,
                       log_file_path : Optional[str]  = None,
                       console_log_function : callable = logging.log):
        if Logger._is_initialized:
            return

        self.console_log_function : callable = console_log_function
        self.log_file_path : Optional[str] = log_file_path
        self.use_timestamp : bool = use_timestamp

    @classmethod
    def get_is_initialized(cls):
        return cls._is_initialized

    def log(self, msg : str, log_file_override : Optional[str] = None):
        log_file_path = self.log_file_path if not log_file_override else log_file_override
        if log_file_path:
            self.try_log_to_file(msg= msg)

    def try_log_to_file(self, msg : str):
        try:
            with open(self.log_file_path, 'a') as file:
                file.write(msg + '\n')
        except Exception as e:
            print(f'Error while trying to log to file: {e}')


def log(msg : str):
    was_uninitialized = Logger.get_is_initialized()
    logger = Logger()
    if was_uninitialized:
        logger.log(f'Logger was initialized with default values')
    logger.log(msg=msg)




def get_timestamp(use_subscores : bool = True, date_only : bool = False) -> str:
    fomat_str = '%Y-%m-%d'

    if not date_only:
        time_of_day_str = ' %H_%M_%S' if use_subscores else ' %H:%M:%S'
        fomat_str += time_of_day_str

    return datetime.now().strftime(fomat_str)



# if __name__ == "__main__":

#     tf = [True, False]
#     for (_use_subscore, _date_only) in [(x, y) for x in tf for y in tf]:
#         print(f"use_subscore, date_onyl = {_use_subscore}, {_date_only}: timestamp: {get_timestamp(_use_subscore, _date_only)}")
#


if __name__ == "__main__":
    Logger()