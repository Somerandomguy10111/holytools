import os
from typing import Optional


class TreeGenerator:
    @classmethod
    def dict_to_tree(cls, fsys_dict: dict, desc_map : Optional[dict[str, str]] = None, path_to_fileID : Optional[dict[str, int]] = None,
                     indent: int = 0, parent_dirpath : str = '/', max_children: int = 10) -> str:
        if desc_map is None:
            desc_map = {}
        if path_to_fileID is None:
            path_to_fileID = {}

        total_str = ''
        if not fsys_dict:
            return total_str

        items = fsys_dict.items()
        for n, (k, v) in enumerate(items):
            indentation = '\t' * indent

            if n == max_children:
                total_str += f'{indentation}... (Max folder elements displayed = {max_children})\n'
                break

            fpath = os.path.join(f'{parent_dirpath}', k)
            is_file = os.path.isfile(fpath)
            symbol = f'🗎' if is_file else '🗀'
            conditional_backslash = '' if is_file else '/'
            conditional_description = f'{indentation}{desc_map[fpath]}\n' if fpath in desc_map else ''
            conditional_fileID = f' | FileID = {path_to_fileID[fpath]}' if fpath in path_to_fileID else ''

            total_str += (f'{indentation}{symbol} {k}{conditional_backslash}{conditional_fileID}\n'
                          f'{conditional_description}'
                          f'{cls.dict_to_tree(v, indent=indent + 1, parent_dirpath=fpath, desc_map=desc_map, path_to_fileID=path_to_fileID)}')
        if indent == 0:
            total_str = total_str.rstrip()
        return total_str

    @staticmethod
    def to_dict(paths: list[str]) -> dict:
        tree_dict = {}
        for fp in paths:
            parts = fp.split('/')
            node = tree_dict
            for k, p in enumerate(parts):
                item = TreeGenerator.read_file(fpath=fp) if k == len(parts)-1 and os.path.isfile(fp) else {}
                if not p in node:
                    node[p] = item
                node = node[p]
        return tree_dict

    @staticmethod
    def read_file(fpath : str) -> str:
        with open(fpath, 'r') as f:
            content = f.read()
        return content