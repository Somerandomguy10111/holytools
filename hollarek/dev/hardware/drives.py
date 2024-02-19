import os
import tempfile, shutil

from hollarek.dev.log import get_logger, LogSettings
import logging
# -------------------------------------------


drive_logger = get_logger(name='drive_logger', settings=LogSettings(include_call_location=False))
def log(msg : str, level : int = logging.INFO):
    drive_logger.log(msg=msg, level=level)


def get_free_space_in_GB(directory : str) -> float:
    total, used, free = shutil.disk_usage(os.path.realpath(directory))
    return free / (1024**3)

def get_total_space_in_GB(directory : str) -> float:
    total, used, free = shutil.disk_usage(os.path.realpath(directory))
    return total / (1024**3)


def print_free_space_info(location_path : str):
    warning_free_space = 250
    critical_free_space_in_GB = 100

    free_space_GB = int(round(get_free_space_in_GB(directory=location_path),0))
    total_space_GB = int(round(get_total_space_in_GB(directory=location_path), 0))
    log(f'Free space at {location_path}: {free_space_GB}/{total_space_GB} GB')

    if free_space_GB < warning_free_space:
        log(f'Warning: Disk space is running low at "{location_path}. Only {free_space_GB} GB left!', level=logging.WARNING)

    elif free_space_GB < critical_free_space_in_GB:
        log(f'Warning: Almost no disk space remaining at {location_path}. Only {free_space_GB} GB left!', level=logging.CRITICAL)


if __name__ == '__main__':
    print_free_space_info(location_path='/home/daniel/OneDrive')