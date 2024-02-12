from __future__ import annotations
import inspect
import os
from typing import Optional
from pathlib import Path

# -------------------------------------------

def get_caller_filepath() -> Optional[str]:
    try:
        frame = inspect.currentframe().f_back.f_back
        filename = frame.f_globals["__file__"]
        rootpath = os.path.abspath(filename)
    except:
        rootpath = None
    return rootpath


class FsysNode:
    def __init__(self, path : str):
        self.path : str = path
        self.name : str = os.path.basename(path)
        self.is_file : bool = os.path.isfile(path)
        self._descendants : Optional[list[FsysNode]] = None

    def get_descendants(self):
        if self._descendants is None:
            path_list = list(Path(self.path).rglob('*'))
            self._descendants: list[FsysNode] = [FsysNode(str(path)) for path in path_list]
        return self._descendants


    def select_file_nodes(self, allowed_formats : list[str]) -> list[FsysNode]:
        selected_node = []
        file_nodes  = self.get_file_nodes()
        for node in file_nodes:
            suffix = node.get_suffix()
            if suffix in allowed_formats:
                selected_node.append(node)

        return selected_node


    def get_file_nodes(self) -> list[FsysNode]:
        return [des for des in self.get_descendants() if des.is_file]


    def get_suffix(self) -> Optional[str]:
        try:
            suffix = self.name.split('.')[-1]
        except:
            suffix = None
        return suffix


if __name__ == "__main__":
    home_node = FsysNode(path='/home/daniel/OneDrive/Downloads/')
    # print(home_node.get_file_nodes())
    # for node in home_node.select_file_nodes(allowed_formats=['png']):
    #     print(node.name)