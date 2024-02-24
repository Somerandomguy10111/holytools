from __future__ import annotations
from abc import abstractmethod
from typing import Optional
import json
from hollarek.dev import get_logger, LogSettings


class Settings(dict[str,str]):
    @staticmethod
    def from_str(json_str : str) -> Settings:
        return json.loads(json_str)

    def to_str(self) -> str:
        return json.dumps(self)


class Configs:
    def __init__(self):
        self._settings : Settings = Settings()
        self.is_initialized : bool = False
        logger = get_logger(settings=LogSettings(), name=self.__class__.__name__)
        self.log = logger.log


    def get(self, key : str) -> str:
        if not self.is_initialized:
            self._settings  = self._retrieve_settings()
            self.is_initialized = True
        try:
            value = self._settings.get(key)
            if not value:
                raise KeyError
        except Exception as e:
            value = input(f'Could not find key {key} in settings: \"{e}\" Please set it manually')
            value = self.set(key=key, value=value)
        return value

    @abstractmethod
    def _retrieve_settings(self) -> Optional[Settings]:
        pass


    @abstractmethod
    def set(self, key : str, value : str):
        pass


if __name__ == '__main__':
    sts = { 'abc' : 'value'}
    the_settings = Settings(sts)
    print(the_settings.to_str())
