from __future__ import annotations
from typing import Optional
from pathlib import Path as PathWrapper
import os
import tempfile, shutil
import yaml
# -------------------------------------------

class FsysNode:
    def __init__(self, path : str):
        self._path_wrapper : PathWrapper = PathWrapper(path)
        self._subnodes : Optional[list[FsysNode]] = None
        if not (self.is_dir() or self.is_file()):
            raise FileNotFoundError(f'Path {path} is not a file/folder')

    # -------------------------------------------
    # sub

    def select_file_subnodes(self, allowed_formats : list[str]) -> list[FsysNode]:
        file_subnodes = self.get_file_subnodes()
        fmts_without_dots = [fmt.replace('.','') for fmt in allowed_formats]

        return [node for node in file_subnodes if node.get_suffix() in fmts_without_dots]


    def get_file_subnodes(self) -> list[FsysNode]:
        return [des for des in self.get_subnodes() if des.is_file()]


    def get_subnodes(self, follow_symlinks : bool = False) -> list[FsysNode]:
        if not self.is_dir():
            return []

        if not self._subnodes is None:
            return self._subnodes

        self._subnodes = []
        if follow_symlinks:
            child_nodes = self.get_child_nodes()
            for child in child_nodes:
                self._subnodes.append(child)
                self._subnodes += child.get_subnodes(follow_symlinks=True)
        else:
            path_list = list(self._path_wrapper.rglob('*'))
            self._subnodes: list[FsysNode] = [FsysNode(str(path)) for path in path_list]

        return self._subnodes

    # -------------------------------------------
    # repr

    def get_yaml_tree(self, skip_null : bool = True) -> str:
        the_yaml = yaml.dump(data=self.get_dict())
        if skip_null:
            the_yaml = the_yaml.replace(f': null', '')

        return the_yaml


    def get_dict(self) -> Optional[dict]:
        if not self.is_dir():
            return None

        return {child.get_name() : child.get_dict() for child in self.get_child_nodes()}


    def get_child_nodes(self) -> list[FsysNode]:
        potential_nodes = [self.try_make_child(name=name) for name in os.listdir(path=self.get_path())]
        return [node for node in potential_nodes if node]


    def try_make_child(self, name : str) -> Optional[FsysNode]:
        try:
            return FsysNode(path=os.path.join(self.get_path(), name))
        except:
            return None

    # -------------------------------------------
    # get data

    def get_zip(self) -> bytes:
        with tempfile.TemporaryDirectory() as write_dir:
            zip_basepath = os.path.join(write_dir,'zipfile')
            if self.is_dir():
                shutil.make_archive(base_name=zip_basepath, format='zip', root_dir=self.get_path())
            else:
                containing_dir_path = os.path.join(write_dir, 'dir')
                os.makedirs(containing_dir_path, exist_ok=True)
                shutil.copy(src=self.get_path(), dst=os.path.join(containing_dir_path, self.get_name()))
                shutil.make_archive(base_name=zip_basepath, format='zip', root_dir=containing_dir_path)

            with open(f'{zip_basepath}.zip', 'rb') as file:
                zip_bytes = file.read()

        return zip_bytes

    # -------------------------------------------
    # resource info

    def get_path(self) -> str:
        return str(self._path_wrapper)

    def get_name(self) -> str:
        return os.path.basename(self.get_path())

    def get_suffix(self) -> Optional[str]:
        try:
            suffix = self.get_name().split('.')[-1]
        except:
            suffix = None
        return suffix

    def get_epochtime_last_modified(self) -> float:
        return os.path.getmtime(self.get_path())

    def get_size_in_MB(self) -> float:
        return os.path.getsize(self.get_path()) / (1024 * 1024)

    def is_file(self) -> bool:
        return os.path.isfile(self.get_path())

    def is_dir(self) -> bool:
        return os.path.isdir(self.get_path())

    def get_parent(self) -> FsysNode:
        return FsysNode(path=str(self._path_wrapper.parent))


