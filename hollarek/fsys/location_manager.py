from __future__ import annotations
import os
from typing import Optional
# -------------------------------------------

class LocationManager:
    _root_dirpath : Optional[str] = None
    
    def __init__(self):
        raise ValueError(f'Cannot initialize {self.__class__.__name__}, it is used as a class only')
        
    @classmethod
    def set_root(cls, root_dirpath : str):
        if not cls._root_dirpath is None:
            raise ValueError(f'Root directory already set to {cls._root_dirpath}')
        
        if root_dirpath is None:
            raise ValueError(f'Failed to initialize {cls.get_name()}: Root directory is None')

        if not os.path.isdir(root_dirpath):
            raise ValueError(f'Failed to initialize {cls.get_name()}: Root directory {root_dirpath} does not exist')

        cls._root_dirpath = root_dirpath

    def get_root_dirpath(self) -> str:
        if self._root_dirpath is None:
            raise ValueError(f'Root directory not set for {self.get_name()}')
        return self._root_dirpath

    @classmethod
    def relative_dir(cls, relative_path : str) -> str:
        if cls._root_dirpath is None:
            raise ValueError(f'Root directory not set for {cls.get_name()}')

        dirpath = os.path.join(cls._root_dirpath, relative_path)
        os.makedirs(dirpath, exist_ok=True)
        return dirpath

    @classmethod
    def get_name(cls) -> str:
        return cls.__name__

