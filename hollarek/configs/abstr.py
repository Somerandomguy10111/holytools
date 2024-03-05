from __future__ import annotations

from abc import abstractmethod
import json
from hollarek.templates import Singleton
from hollarek.logging import LogLevel, get_logger


class StrMap(dict[str,str]):
    @staticmethod
    def from_str(json_str : str) -> StrMap:
        return StrMap(json.loads(json_str))

    def to_str(self) -> str:
        return json.dumps(self)

    def is_empty(self):
        return len(self) == 0


class Configs(Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._map: StrMap = StrMap()
        self.is_setup: bool = False
        self.log = get_logger(name=self.__class__.__name__).log

    def get(self, key : str) -> str:
        if not self.is_setup:
            self._map  = self._retrieve_map()

        if self._map.is_empty():
            self.log(msg=f'No settings found', level=LogLevel.WARNING)
        try:
            value = self._map.get(key)
            if not value:
                raise KeyError
        except:
            self.log(f'Could not find key {key} in settings: Please set it manually', level=LogLevel.WARNING)
            value = input()
            value = self.set(key=key, value=value)
        return value


    @abstractmethod
    def _retrieve_map(self) -> StrMap:
        pass


    @abstractmethod
    def set(self, key : str, value : str):
        pass


if __name__ == '__main__':
    sts = { 'abc' : 'value'}
    the_settings = StrMap(sts)
    print(the_settings.to_str())
