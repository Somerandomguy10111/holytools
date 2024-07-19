from __future__ import annotations

from abc import abstractmethod, ABC
from typing import TypeVar, Optional

from holytools.logging import Loggable, LogLevel

DictType = TypeVar(name='DictType', bound=dict)

# ---------------------------------------------------------

class BaseConfigs(Loggable, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._map : DictType = self._retrieve_map()

    @abstractmethod
    def _retrieve_map(self) -> DictType:
        pass

    # ---------------------------------------------------------

    def get(self, key : str, section : Optional[str] = None) -> Optional[str]:
        if len(key.split()) > 1:
            raise ValueError(f'Key must not contain whitespaces, got : \"{key}\"')

        try:
            the_dict = self._map
            if section:
                the_dict = the_dict[section]
            config_value = the_dict[key]
        except KeyError:
            self.log(msg=f'Could not find key \"{key}\" under section {section} in configs', level=LogLevel.WARNING)
            config_value = None

        return config_value

    def set(self, key : str, value : str, section : Optional[str] = None):
        if key in self._map:
            raise ValueError(f'Key \"{key}\" already exists in settings')
        if not section is None:
            self._map[section] = {}
        the_dict = self._map if section is None else self._map[section]
        the_dict[key] = value
        self.update_config_resouce(key=key, value=str(value), section=section)


    @abstractmethod
    def update_config_resouce(self, key : str, value : str, section : Optional[str] = None):
        pass



