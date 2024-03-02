from __future__ import annotations
import os
from pathvalidate import sanitize_filepath
# -------------------------------------------

class PathChecker:
    @staticmethod
    def get_path_is_valid(path : str) -> bool:
        if os.path.exists(path):
            return True
        if path == sanitize_filepath(path):
            return True
        return False


    @staticmethod
    def get_sanitized_path(path : str) -> str:
        path = path.strip()
        path = sanitize_filepath(file_path=path)
        return path


    @staticmethod
    def get_free_path(basepath : str) -> str:
        counter = 0
        while os.path.exists(basepath):
            unique_suffix = '' if counter == 0 else f'_{counter}'
            basepath = f'{basepath}{unique_suffix}'
            counter += 1
        return basepath




