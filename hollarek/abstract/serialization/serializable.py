from __future__ import annotations
import os
from abc import abstractmethod
from typing import TypeVar


class Serializable:
    @abstractmethod
    def to_str(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_str(cls, s: str):
        pass

    def save(self, fpath : str, force_overwrite : bool = False):
        fpath = os.path.abspath(path=fpath)
        dirpath = os.path.dirname(fpath)
        os.makedirs(dirpath, exist_ok=True)
        if os.path.isfile(fpath) and not force_overwrite:
            raise ValueError(f'File {fpath} already exists')
        with open(fpath, 'w') as f:
            f.write(self.to_str())

    @classmethod
    def load(cls, fpath : str) -> SerializableType:
        with open(fpath, 'r') as f:
            str_data = f.read()
        return cls.from_str(str_data)


SerializableType = TypeVar(name='SerializableType', bound=Serializable)