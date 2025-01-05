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
    def prune_suffix(fpath : str) -> str:
        parts = fpath.split('.')
        if len(parts) > 1:
            return '.'.join(parts[:-1])
        else:
            return fpath

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