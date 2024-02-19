from __future__ import annotations
import os
from abc import ABC, abstractmethod
from typing import Optional

# -------------------------------------------

class LocationManager(ABC):
    instance = None
    _is_initialized : bool = False

    @classmethod
    def initialize(cls,root_dir : str):
        cls(root_dir=root_dir)


    def __new__(cls, root_dir: Optional[str] = None):
        if cls.instance is None:
            cls.instance = super(LocationManager, cls).__new__(cls)
        return cls.instance


    def __init(self, root_dir: Optional[str] = None):
        if LocationManager._is_initialized:
            return

        if root_dir is None:
            raise ValueError(f'Cannot initialize {self.__name__}. Given root_dir is None')

        if not os.path.isdir(root_dir):
            raise ValueError(f'Cannot initialized {self.__name__}. Root directory {root_dir} does not exist')

        self.root_path: str = root_dir
        self._directories : list[str] = []
        self.setup_dirs()

        LocationManager._is_initialized = True


    def add_dir(self, relative_path : str) -> str:
        new_dir_path = os.path.join(self.root_path, relative_path)
        os.makedirs(new_dir_path, exist_ok=True)
        self._directories.append(new_dir_path)

        return new_dir_path


    @abstractmethod
    def setup_dirs(self):
        pass
