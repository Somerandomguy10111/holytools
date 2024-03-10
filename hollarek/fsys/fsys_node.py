from __future__ import annotations
from typing import Optional
from pathlib import Path as PathWrapper
import os
import tempfile, shutil
from hollarek.templates import TreeNode
# -------------------------------------------

class FsysNode(TreeNode):
    def __init__(self, path : str, parent : FsysNode = None):
        newpath = os.path.normpath(path)
        super().__init__(name=os.path.basename(newpath), parent=parent)
        self._path_wrapper : PathWrapper = PathWrapper(path)
        if not (self.is_dir() or self.is_file()):
            raise FileNotFoundError(f'Path {path} is not a file/folder')

    # -------------------------------------------
    # descendants

    def get_file_subnodes(self, select_formats: Optional[list[str]] = None) -> list[FsysNode]:
        file_subnodes = [des for des in self.get_subnodes() if des.is_file()]
        if select_formats is not None:
            fmts_without_dots = [fmt.replace('.', '') for fmt in select_formats]
            file_subnodes = [node for node in file_subnodes if node.get_suffix() in fmts_without_dots]
        return file_subnodes


    def get_subnodes(self, follow_symlinks : bool = False) -> list[FsysNode]:
        if follow_symlinks:
            subnodes = super().get_subnodes()
        else:
            path_list = list(self._path_wrapper.rglob('*'))
            subnodes = [FsysNode(str(path)) for path in path_list]

        return subnodes


    def get_child_nodes(self) -> list[FsysNode]:
        if not self._children is None:
            return self._children

        if self._children is None:
            self._children = []
            if not self.is_file():
                child_paths = [os.path.join(self.get_path(), name) for name in os.listdir(path=self.get_path())]
                self._children = [FsysNode(path=path, parent=self) for path in child_paths]

        return self._children

    # -------------------------------------------
    # ancestors

    def get_parent(self) -> Optional[FsysNode]:
        if self.is_root():
            return None

        if self._parent is None:
            self._parent = FsysNode(path=str(self._path_wrapper.parent))
        return self._parent


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
    print(test_node.get_tree(pretty=False))


