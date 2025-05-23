import os
import shutil
import stat
import tempfile
from abc import abstractmethod
from pathlib import Path as PathWrapper
from typing import Optional

# ----------------------------------------------------

class FsysNode:
    def __init__(self, path : str):
        self._path_wrapper : PathWrapper = PathWrapper(path)

    def get_zip(self) -> bytes:
        with tempfile.TemporaryDirectory() as write_dir:
            zip_base_path = os.path.join(write_dir, 'zipfile')
            args_dir = {
                'base_name': zip_base_path,
                'format': 'zip',
            }
            if self._path_wrapper.is_file():
                args_dir['root_dir'] = self.get_parent_dirpath()
                args_dir['base_dir'] = self.get_name()

            if self._path_wrapper.is_dir():
                args_dir['root_dir'] = self.get_path()

            shutil.make_archive(**args_dir)
            with open(f'{zip_base_path}.zip', 'rb') as file:
                zip_bytes = file.read()

        return zip_bytes

    # -------------------------------------------
    # attributes

    def get_path(self) -> str:
        return str(self._path_wrapper.absolute())

    def get_parent_dirpath(self) -> str:
        return str(self._path_wrapper.parent.absolute())

    def get_name(self) -> str:
        return self._path_wrapper.name

    def is_hidden(self) -> bool:
        if os.name == 'posix':
            return os.path.basename(self.get_path()).startswith('.')
        elif os.name == 'nt':
            return bool(os.stat(self.get_path()).st_file_attributes & stat.FILE_ATTRIBUTE_HIDDEN)
        else:
            raise NotImplementedError(f'Unsupported OS: {os.name}, {FsysNode.is_hidden.__name__} is only supported '
                                      f'on Windows and Unix systems')

    def get_last_modified_epochtime(self) -> float:
        return os.path.getmtime(self.get_path())

    def get_size_in_MB(self) -> float:
        return os.path.getsize(self.get_path()) / (1024 * 1024)

    @abstractmethod
    def get_tree(self, *args, **kwargs) -> str:
        pass


class Directory(FsysNode):
    def __init__(self, path : str):
        super().__init__(path=path)
        if not self._path_wrapper.is_dir():
            raise FileNotFoundError(f'Path {path} is not a directory')

    def get_tree(self, indent : int = 0, max_children : int = 10, *args, **kwargs) -> str:
        indentation = '\t' * indent
        total_str = f'{indentation}🗀 {self.get_name()}/'

        subpaths = [os.path.join(self.get_path(),name) for name in os.listdir(self.get_path())]
        files = [File(path=p) for p in subpaths if os.path.isfile(p)]
        directories = [self.__class__(path=p) for p in subpaths if os.path.isdir(p)]

        for node in files+directories:
            total_str += f'\n{node.get_tree(indent=indent+1)}'
        return total_str

    def get_subfile_fpaths(self, absolute : bool = True) -> list[str]:
        subfile_paths = []
        for root, dirs, files in os.walk(self.get_path()):
            for file in files:
                fpath = os.path.join(root, file)
                subfile_paths.append(fpath)
        if not absolute:
            subfile_paths = [os.path.relpath(p, self.get_path()) for p in subfile_paths]
        return subfile_paths

    def get_all_subpaths(self, absolute : bool = True) -> list[str]:
        all_paths = []
        for root, dirs, files in os.walk(self.get_path()):
            for d in dirs:
                dirpath = os.path.join(root, d)
                all_paths.append(dirpath)
            for f in files:
                fpath = os.path.join(root, f)
                all_paths.append(fpath)
        if not absolute:
            all_paths = [os.path.relpath(p, self.get_path()) for p in all_paths]

        return all_paths



class File(FsysNode):
    def __init__(self, path : str):
        super().__init__(path=path)
        if not self._path_wrapper.is_file():
            raise FileNotFoundError(f'Path {path} is not a file')

    def get_suffix(self) -> Optional[str]:
        parts = self.get_name().split('.')
        if len(parts) == 1:
            return None
        else:
            return parts[-1]

    def get_tree(self, indent : int = 0, max_children : int = 10, *args, **kwargs) -> str:
        indentation = '\t' * indent
        return f'{indentation}🗎 {self.get_name()}'


if __name__ == "__main__":
    directory = Directory(path='/home/daniel/misc/holytools', )
    print(directory.get_tree())