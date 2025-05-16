import os
from dataclasses import dataclass, field
from typing import Optional

@dataclass
class TreeDecorator:
    desc_map : dict[str, str] = field(default_factory=dict)
    path_to_fileID : dict[str, int] = field(default_factory=dict)


class TreeGenerator:
    @classmethod
    def dict_to_tree(cls, fsys_dict: dict, decorator : Optional[TreeDecorator] = None, max_children: int = 10,
                          indent: int = 0, parent_dirpath : str = '/') -> str:
        total_str = ''
        items = fsys_dict.items()
        desc_map, path_to_fileID = decorator.desc_map, decorator.path_to_fileID
        for n, (k, v) in enumerate(items):
            indentation = '\t' * indent

            if n == max_children:
                total_str += f'{indentation}... (Max folder elements displayed = {max_children})\n'
                break

            fpath = os.path.join(f'{parent_dirpath}', k)
            is_file = os.path.isfile(fpath)

            symbol = f'🗎' if is_file else '🗀'
            cond_backslash = '' if is_file else '/'
            cond_desc = f'{indentation}{desc_map[fpath]}\n' if fpath in desc_map else ''
            cond_fileID = f' | FileID = {path_to_fileID[fpath]}' if fpath in path_to_fileID else ''

            total_str += (f'{indentation}{symbol} {k}{cond_backslash}{cond_fileID}\n'
                          f'{cond_desc}'
                          f'{cls.dict_to_tree(v, indent=indent + 1, parent_dirpath=fpath, decorator=decorator)}')
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