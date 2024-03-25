from __future__ import annotations
from typing import Optional
from pathlib import Path as PathWrapper
import os
import tempfile, shutil
from hollarek.abstract import TreeNode
# -------------------------------------------

class FsysNode(TreeNode):
    def __init__(self, path : str, parent : Optional[FsysNode] = None):
        super().__init__()
        self._path_wrapper : PathWrapper = PathWrapper(path)
        self._cached_children : Optional[list[FsysNode]] = []
        self._cached_parent : Optional[FsysNode] = parent
        if not (self.is_dir() or self.is_file()):
            raise FileNotFoundError(f'Path {path} is not a file/folder')

    # -------------------------------------------
    # descendants

    def add_child(self, path : str) -> FsysNode:
        if self._cached_children is None:
            self._cached_children = []
        child = FsysNode(path=path, parent=self)
        self._cached_children.append(child)
        return child


    def get_file_subnodes(self, select_formats: Optional[list[str]] = None) -> list[FsysNode]:
        file_subnodes = [des for des in self.get_subnodes() if des.is_file()]
        if select_formats is not None:
            fmts_without_dots = [fmt.replace('.', '') for fmt in select_formats]
            file_subnodes = [node for node in file_subnodes if node.get_suffix() in fmts_without_dots]
        return file_subnodes


    def get_subnodes(self, follow_symlinks: bool = True) -> list['FsysNode']:
        path_to_node = {self.get_path(): self}

        for root, dirs, files in os.walk(self.get_path(), followlinks=follow_symlinks):
            parent_node = path_to_node.get(root)
            for name in dirs+files:
                path = os.path.join(root, name)
                is_resource = os.path.isfile(path) or os.path.isdir(path)
                if path in path_to_node or not is_resource:
                    continue
                try:
                    path_to_node[path] = parent_node.add_child(path)
                except FileNotFoundError:
                    continue

        return list(path_to_node.values())


    def get_child_nodes(self) -> list[FsysNode]:
        if not self._cached_children is None:
            return self._cached_children

        self._cached_children = []
        if not self.is_dir():
            return self._cached_children

        child_paths = [os.path.join(self.get_path(), name) for name in os.listdir(path=self.get_path())]
        for path in child_paths:
            try:
                self.add_child(path=path)
            except:
                continue

        return self._cached_children

    # -------------------------------------------
    # ancestors

    def get_parent(self) -> Optional[FsysNode]:
        if self.is_root():
            return None

        if self._cached_parent is None:
            self._cached_parent = FsysNode(path=str(self._path_wrapper.parent))
        return self._cached_parent

    def is_root(self):
        return self._path_wrapper.parent == self._path_wrapper

    # -------------------------------------------
    # get data

    def get_zip(self) -> bytes:
        with tempfile.TemporaryDirectory() as write_dir:
            zip_base_path = os.path.join(write_dir, 'zipfile')
            args_dir = {
                'base_name': zip_base_path,
                'format': 'zip',
            }
            if self.is_file():
                args_dir['root_dir'] = self.get_parent().get_path()
                args_dir['base_dir'] = self.get_name()

            if self.is_dir():
                args_dir['root_dir'] = self.get_path()

            shutil.make_archive(**args_dir)
            with open(f'{zip_base_path}.zip', 'rb') as file:
                zip_bytes = file.read()

        return zip_bytes

    # -------------------------------------------
    # resource info
    def get_name(self) -> str:
        return self._path_wrapper.name

    def get_path(self) -> str:
        return str(self._path_wrapper.absolute())

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
        return self._path_wrapper.is_file()

    def is_dir(self) -> bool:
        return self._path_wrapper.is_dir()


if __name__ == "__main__":
    test_path = '/home/daniel/OneDrive/Pictures'
    test_node = FsysNode(test_path)
    print(test_node.get_name())
    print(test_node.get_path())
    # print('abc')
    # print(test_path)

    test_childpaths = [node.get_path() for node in test_node.get_child_nodes()]
    test_sub_paths = [node.get_path() for node in test_node.get_subnodes()]
    test_sub_paths2 = [node.get_path() for node in test_node.get_subnodes(follow_symlinks=True)]

    print(f'test childpaths {len(test_childpaths)}')
    print(f'test sub paths {len(test_sub_paths)}')
    print(f'test sub paths {len(test_sub_paths2)}')


