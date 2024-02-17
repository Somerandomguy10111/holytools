from datetime import datetime
from typing import Optional

#
# class Logger:
#
#
#     def __init__(self, use_timestamp : bool = True,
#                        log_file_path : Optional[str]  = None):
#         self.log_file_path : Optional[str] = log_file_path
#         self.use_timestamp
#
#
#
#
# def log():



def get_timestamp(use_subscores : bool = True, date_only : bool = False) -> str:
    fomat_str = '%Y-%m-%d'

    if not date_only:
        time_of_day_str = ' %H_%M_%S' if use_subscores else ' %H:%M:%S'
        fomat_str += time_of_day_str

    return datetime.now().strftime(fomat_str)



if __name__ == "__main__":
    tf = [True, False]
    for (_use_subscore, _date_only) in [(x, y) for x in tf for y in tf]:
        print(f"use_subscore, date_onyl = {_use_subscore}, {_date_only}: timestamp: {get_timestamp(_use_subscore, _date_only)}")

