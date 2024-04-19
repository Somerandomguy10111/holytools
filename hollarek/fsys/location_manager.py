from __future__ import annotations
import os
from typing import Optional


# -------------------------------------------

class LocationManager:
    _root_dirpath: Optional[str] = None
    _dirs: list[str] = []

    def __init__(self):
        raise ValueError(f'Cannot initialize {self.__class__.__name__}, it is used as a class only')

    @classmethod
    def set_root(cls, root_dirpath: str):
        if not cls._root_dirpath is None:
            raise ValueError(f'Root directory already set to {cls._root_dirpath}')

        if root_dirpath is None:
            raise ValueError(f'Failed to initialize {cls._get_name()}: Root directory is None')

        if not os.path.isdir(root_dirpath):
            raise ValueError(f'Failed to initialize {cls._get_name()}: Root directory {root_dirpath} does not exist')

        cls._root_dirpath = root_dirpath

    @classmethod
    def setup_dirs(cls):
        for dirpath in cls._dirs:
            os.makedirs(dirpath, exist_ok=True)

    @classmethod
    def relative_dir(cls, relative_path: str) -> str:
        dirpath = cls._get_relative_path(relative_path=relative_path)
        cls._dirs.append(dirpath)

        return dirpath

    @classmethod
    def relative_file(cls, relative_path: str) -> str:
        fpath = cls._get_relative_path(relative_path=relative_path)
        return fpath

    @classmethod
    def _get_relative_path(cls, relative_path: str) -> str:
        root_dirpath = cls.get_root_dirpath()
        return os.path.join(root_dirpath, relative_path)

    @classmethod
    def get_root_dirpath(cls) -> str:
        if cls._root_dirpath is None:
            raise ValueError(f'Root directory not set for {cls._get_name()}')
        return cls._root_dirpath

    @classmethod
    def _get_name(cls) -> str:
        return cls.__name__

