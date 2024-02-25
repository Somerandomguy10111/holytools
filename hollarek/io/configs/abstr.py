from __future__ import annotations

from abc import abstractmethod
import json
from hollarek.tmpl import Singleton
from hollarek.dev import LogLevel


class Settings(dict[str,str]):
    @staticmethod
    def from_str(json_str : str) -> Settings:
        return Settings(json.loads(json_str))

    def to_str(self) -> str:
        return json.dumps(self)

    def is_empty(self):
        return len(self) == 0


class Configs(Singleton):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._settings: Settings = Settings()
        self.is_setup: bool = False


    def get(self, key : str) -> str:
        if not self.is_setup:
            self._settings  = self._retrieve_settings()

        if self._settings.is_empty():
            self.log(msg=f'No settings found', level=LogLevel.WARNING)
        try:
            value = self._settings.get(key)
            if not value:
                raise KeyError
        except:
            self.log(f'Could not find key {key} in settings: Please set it manually', level=LogLevel.WARNING)
            value = input()
            value = self.set(key=key, value=value)
        return value


    @abstractmethod
    def _retrieve_settings(self) -> Settings:
        pass


    @abstractmethod
    def set(self, key : str, value : str):
        pass


if __name__ == '__main__':
    sts = { 'abc' : 'value'}
    the_settings = Settings(sts)
    print(the_settings.to_str())
