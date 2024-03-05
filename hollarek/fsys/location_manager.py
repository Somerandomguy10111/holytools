from __future__ import annotations
import os
from abc import abstractmethod
from typing import Optional
from hollarek.templates import Singleton
# -------------------------------------------

class LocationManager(Singleton):
    def __init__(self, root_dir: Optional[str] = None):
        if self.get_is_initialized():
            return

        super().__init__()
        if root_dir is None:
            raise ValueError(f'Cannot initialize {self.__name__}. Given root_dir is None')

        if not os.path.isdir(root_dir):
            raise ValueError(f'Cannot initialized {self.__name__}. Root directory {root_dir} does not exist')

        self.root_path: str = root_dir
        self._directories : list[str] = []
        self.setup_dirs()




    def add_dir(self, relative_path : str) -> str:
        new_dir_path = os.path.join(self.root_path, relative_path)
        os.makedirs(new_dir_path, exist_ok=True)
        self._directories.append(new_dir_path)

        return new_dir_path


    @abstractmethod
    def setup_dirs(self):
        pass
