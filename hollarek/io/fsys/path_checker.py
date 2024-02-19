from __future__ import annotations

import os

from pathvalidate import sanitize_filepath


class PathChecker:
    @staticmethod
    def get_path_is_valid(path : str) -> bool:
        if os.path.exists(path):
            return True
        if path == sanitize_filepath(path):
            return True
        return False

    @staticmethod
    def get_valid_path(path : str) -> str:
        return sanitize_filepath(file_path=path)
