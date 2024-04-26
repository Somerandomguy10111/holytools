from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TypeVar, Union
from holytools.logging import Loggable, LogLevel

DictType = TypeVar(name='DictType', bound=dict)
ConfigValue = Union[str, int, bool]

# ---------------------------------------------------------

class Configs(ABC, Loggable):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._map : DictType = self._retrieve_map()

    def get(self, key : str) -> str:
        try:
            value = self._map.get(key)
            if not value:
                raise KeyError
        except:
            self.log(f'Could not find key {key} in settings: Please set it manually', level=LogLevel.WARNING)
            value = input()
            self.set(key=key, value=value)
        return value

    def is_empty(self) -> bool:
        return len(self._map) == 0

    @abstractmethod
    def _retrieve_map(self) -> DictType:
        pass


    @abstractmethod
    def set(self, key : str, value : str):
        pass


if __name__ == '__main__':
    pass
    # sts = { 'abc' : 'value'}
    # the_settings = StrMap(sts)
    # print(the_settings.to_str())
