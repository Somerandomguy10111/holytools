from datetime import datetime

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

