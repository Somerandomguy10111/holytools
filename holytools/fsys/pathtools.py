import os
from typing import Optional

from pathvalidate import sanitize_filename


class PathTools:
    @staticmethod
    def to_valid_filename(name : str) -> str:
        name = name.strip()
        name = name.replace(' ', '_')
        name = sanitize_filename(name)
    
        return name

    @staticmethod
    def increment_idx_until_free(initial_dirpath : str) -> str:
        idx = 0
        dirpath = initial_dirpath
        while os.path.isdir(dirpath):
            idx += 1
            dirpath = f'{initial_dirpath}_{idx}'
        return dirpath

    @staticmethod
    def prune_suffix(fpath : str) -> str:
        fname = os.path.basename(fpath)
        parts = fname.split('.')

        new_fname = fname
        is_hidden = fname.startswith('.')
        if len(parts) > 1 and not is_hidden:
            new_fname = parts[0]
        if len(parts) > 2 and is_hidden:
            new_fname = ".".join(parts[:-1])

        dirpath = os.path.dirname(fpath)
        return os.path.join(dirpath, new_fname)

    @staticmethod
    def ensure_suffix(fpath: str, suffix : str) -> str:
        parts = fpath.split('.')
        if len(parts) < 2:
            fpath = f'{fpath}.{suffix}'
        elif parts[-1] != f'.{suffix}':
            fpath = f'{parts[0]}.{suffix}'
        return fpath

    @staticmethod
    def get_suffix(fpath: str) -> Optional[str]:
        parts = fpath.split('.')
        if len(parts) > 1:
            return parts[-1]
        else:
            return None
