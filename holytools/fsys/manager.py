from __future__ import annotations

import os
from typing import Optional


# -------------------------------------------

class FsysManager:
    def __init__(self, root_dirpath : str):
        if not os.path.isdir(root_dirpath):
            raise ValueError(f'Failed to initialize {self.__class__.__name__}: Root directory {root_dirpath} does not exist')
        self._root_dirpath : str = root_dirpath
        self.dirpaths: list[str] = []
        self.fpaths : list[str] = []

    def add_dir(self, relative_path: str) -> str:
        dirpath = self._get_relative_path(relative_path=relative_path)
        if not os.path.isdir(dirpath):
            os.makedirs(dirpath, exist_ok=True)
        self.dirpaths.append(dirpath)
        return dirpath

    def add_file(self, relative_path: str) -> str:
        fpath = self._get_relative_path(relative_path=relative_path)
        self.fpaths.append(fpath)
        return fpath

    def add_tree(self, tree : dict, root_dirpath : Optional[str] = None):
        if not root_dirpath:
            root_dirpath = self.get_root_dirpath()

        for name, value in tree.items():
            path = os.path.join(root_dirpath, name)
            relpath = os.path.relpath(path=path, start=self._root_dirpath)

            if isinstance(value, dict):
                self.add_dir(relative_path=relpath)
                self.add_tree(root_dirpath=path, tree=value)
            elif isinstance(value, str):
                with open(path,'w') as f:
                    f.write(value)
                self.add_file(relative_path=relpath)
            elif value is None:
                self.add_file(relative_path=relpath)
            else:
                raise ValueError(f"Invalid value: {value}")

    # -------------------------------------------

    def _get_relative_path(self, relative_path: str) -> str:
        root_dirpath = self.get_root_dirpath()
        return os.path.join(root_dirpath, relative_path)

    def get_root_dirpath(self) -> str:
        if self._root_dirpath is None:
            raise ValueError(f'Root directory not set for {self.__class__.__name__}')
        return self._root_dirpath


