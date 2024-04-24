from __future__ import annotations
from typing import Optional
from pathlib import Path as PathWrapper
import tempfile, shutil
import os, stat
# -------------------------------------------

class FsysNode(TreeNode):
    def __init__(self, path : str, parent : Optional[FsysNode] = None):
        super().__init__()
        self._path_wrapper : PathWrapper = PathWrapper(path)
        self._cached_children : Optional[list[FsysNode]] = None
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


    def get_tree(self, max_depth : Optional[int] = None,
                 max_size : Optional[int] = None,
                 exclude_hidden : bool = False) -> Tree:
        return super().get_tree(max_depth=max_depth, max_size=max_size, exclude_hidden=exclude_hidden)


    def get_file_subnodes(self, select_formats: Optional[list[str]] = None) -> list[FsysNode]:
        file_subnodes = [des for des in self.get_subnodes() if des.is_file()]
        if select_formats is not None:
            fmts_without_dots = [fmt.replace('.', '') for fmt in select_formats]
            file_subnodes = [node for node in file_subnodes if node.get_suffix() in fmts_without_dots]
        return file_subnodes


    def get_subnodes(self, follow_symlinks: bool = True) -> list[FsysNode]:
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


    def get_child_nodes(self, exclude_hidden : bool = False) -> list[FsysNode]:
        if not self._cached_children is None:
            return self._cached_children
        self._cached_children = []
        if not self.is_dir():
            return self._cached_children

        child_paths = [os.path.join(self.get_path(), name) for name in os.listdir(path=self.get_path())]
        for path in child_paths:
            # print(f'Filepath {path} is hidden: {is_hidden(path)}')
            if exclude_hidden and is_hidden(path):
                continue
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

    def is_hidden(self) -> bool:
        return is_hidden(self.get_path())

    def get_name(self) -> str:
        return self._path_wrapper.name

    def get_path(self) -> str:
        return str(self._path_wrapper.absolute())

    def get_suffix(self) -> Optional[str]:
        parts = self.get_name().split('.')
        if len(parts) == 1:
            return None
        else:
            return parts[-1]


    def get_epochtime_last_modified(self) -> float:
        return os.path.getmtime(self.get_path())

    def get_size_in_MB(self) -> float:
        return os.path.getsize(self.get_path()) / (1024 * 1024)

    def is_file(self) -> bool:
        return self._path_wrapper.is_file()

    def is_dir(self) -> bool:
        return self._path_wrapper.is_dir()


def is_hidden(filepath: str) -> bool:
    if os.name == 'posix':
        return os.path.basename(filepath).startswith('.')
    elif os.name == 'nt':
        return bool(os.stat(filepath).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
    else:
        raise NotImplementedError(f'Unsupported OS: {os.name}, {FsysNode.is_hidden.__name__} is only supported '
                                  f'on Windows and Unix systems')