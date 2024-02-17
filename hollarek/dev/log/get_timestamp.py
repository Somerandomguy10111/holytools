from datetime import datetime


def get_timestamp(use_subscores: bool = True, date_only: bool = False) -> str:
    format_str = '%Y-%m-%d'

    if not date_only:
        time_of_day_str = ' %H_%M_%S' if use_subscores else ' %H:%M:%S'
        format_str += time_of_day_str

    return datetime.now().strftime(format_str)
