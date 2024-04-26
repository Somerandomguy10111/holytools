from __future__ import annotations

import ast
from abc import abstractmethod, ABC
from typing import TypeVar, Union
from holytools.logging import Loggable, LogLevel

DictType = TypeVar(name='DictType', bound=dict)
ConfigValue = Union[str, int, bool, float]

# ---------------------------------------------------------

class Configs(Loggable):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._map : DictType = self._retrieve_map()

    @abstractmethod
    def _retrieve_map(self) -> DictType:
        pass

    # ---------------------------------------------------------

    def get(self, key : str) -> ConfigValue:
        if len(key.split()) > 1:
            raise ValueError(f'Key must not contain whitespaces, got : \"{key}\"')

        try:
            value = self._map.get(key)
            if value is None:
                raise KeyError
        except:
            self.log(f'Could not find key {key} in settings: Please set it manually', level=LogLevel.WARNING)
            value = input()
            self.set(key=key, value=value)

        value = self.convert_string(value)
        return value


    def set(self, key : str, value : ConfigValue):
        if not isinstance(value, ConfigValue):
            raise ValueError(f'Value must be of type {ConfigValue} got : \"{value}\"')
        self._map[key] = value
        self.update_config_resouce(key=key, value=str(value))


    @abstractmethod
    def update_config_resouce(self, key : str, value : str):
        pass


    @staticmethod
    def convert_string(value) -> ConfigValue:
        try:
            return ast.literal_eval(value)
        except (ValueError, SyntaxError):
            return value



if __name__ == '__main__':
    pass
    # sts = { 'abc' : 'value'}
    # the_settings = StrMap(sts)
    # print(the_settings.to_str())
