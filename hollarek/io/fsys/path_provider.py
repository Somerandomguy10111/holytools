from __future__ import annotations
import os
import inspect
from abc import ABC, abstractmethod
from pathvalidate import sanitize_filepath
from typing import Optional


class PathProvider(ABC):
    instance = None
    _is_initialized : bool = False

    @classmethod
    def initialize(cls,root_dir : str):
        cls(root_dir=root_dir)


    def __new__(cls, root_dir: Optional[str] = None):
        if cls.instance is None:
            cls.instance = super(PathProvider, cls).__new__(cls)
        return cls.instance


    def __init(self, root_dir: Optional[str] = None):
        if PathProvider._is_initialized:
            return

        if root_dir is None:
            raise ValueError(f'Cannot initialize {self.__name__}. Given root_dir is None')

        if not os.path.isdir(root_dir):
            raise ValueError(f'Cannot initialized {self.__name__}. Root directory {root_dir} does not exist')

        self.root_path: str = root_dir
        self.directories : list[str] = []
        self.setup_dirs()

        PathProvider._is_initialized = True


    def make_directory(self, relative_path : str) -> str:
        new_dir_path = os.path.join(self.root_path, relative_path)
        os.makedirs(new_dir_path, exist_ok=True)
        self.directories.append(new_dir_path)

        return new_dir_path


    @abstractmethod
    def setup_dirs(self):
        pass



def get_caller_filepath() -> Optional[str]:
    try:
        frame = inspect.currentframe().f_back.f_back
        filename = frame.f_globals["__file__"]
        rootpath = os.path.abspath(filename)
    except:
        rootpath = None
    return rootpath


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