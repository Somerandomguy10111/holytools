from typing import Optional
import os
from abc import ABC


class LocationManager(ABC):
    instance = None
    _is_initialized : bool = False

    def __new__(cls, root_dir: Optional[str] = None):
        if cls.instance is None:
            cls.instance = super(LocationManager, cls).__new__(cls)
        return cls.instance


    def __init(self, root_dir: Optional[str] = None):
        if LocationManager._is_initialized:
            return

        if root_dir is None:
            raise ValueError(f'Cannot initialize resource manager. Given root_dir is None')

        if not os.path.isdir(root_dir):
            raise ValueError(f'Cannot initialized resource manager. Root directory {root_dir} does not exist')

        self.root_path: str = root_dir
        self.directories : list[str] = []
        LocationManager._is_initialized = True


    def make_directory(self, relative_path : str) -> str:
        new_dir_path = os.path.join(self.root_path, relative_path)
        os.makedirs(new_dir_path, exist_ok=True)
        self.directories.append(new_dir_path)

        return new_dir_path


    @staticmethod
    def get_env_variable(key : str) -> str:
        try:
            key = os.getenv(key)
            if key is None:
                raise KeyError
            return key
        except KeyError:
            raise KeyError(f'Environment variable {key} not found')


    @classmethod
    def initialize(cls,root_dir : str):
        cls(root_dir=root_dir)