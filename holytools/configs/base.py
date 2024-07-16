from __future__ import annotations

import ast
from abc import abstractmethod, ABC
from typing import TypeVar, Union, Optional, get_origin, get_args
from holytools.logging import Loggable, LogLevel

DictType = TypeVar(name='DictType', bound=dict)
BasicValue = Union[str, int, bool, float]
ConfigValue = Union[BasicValue, list]

# ---------------------------------------------------------

class BaseConfigs(Loggable, ABC):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self._map : DictType = self._retrieve_map()

    @abstractmethod
    def _retrieve_map(self) -> DictType:
        pass

    # ---------------------------------------------------------

    def get(self, key : str, required_dtype : Optional[type]  = None, prompt_if_missing : bool = False) -> Optional[ConfigValue]:
        if len(key.split()) > 1:
            raise ValueError(f'Key must not contain whitespaces, got : \"{key}\"')

        try:
            flatten_dict = flatten(self._map)
            config_value = flatten_dict.get(key)
            if config_value is None:
                raise KeyError
        except:
            if prompt_if_missing:
                self.log(f'Could not find key \"{key}\" in settings: Please set it manually', level=LogLevel.WARNING)
                config_value = input()
                self.set(key=key, value=config_value)
            else:
                self.log(msg=f'Could not find key \"{key}\" in settings', level=LogLevel.WARNING)
                return None

        if isinstance(config_value, str):
            value = self.cast_string(config_value)
        elif isinstance(config_value, list):

            value = [self.cast_string(v) for v in config_value]
        else:
            value =  config_value

        if not required_dtype is None:
            dtype_confirmity = check_dtype_confirmity(obj=value, dtype=required_dtype)
            if not dtype_confirmity:
                raise ValueError(f'Value for key \"{key}\" must be of type {required_dtype} got : \"{value}\" of type {type(value)}')

        return value


    def set(self, key : str, value : ConfigValue, section : Optional[str] = None):
        if key in self._map:
            raise ValueError(f'Key \"{key}\" already exists in settings')
        if not isinstance(value, ConfigValue):
            raise ValueError(f'Value must be of type {ConfigValue} got : \"{value}\"')
        if isinstance(value, list):
            self.check_list_ok(the_list=value)
        if not section is None:
            self._map[section] = {}
        inner_dict = self._map if section is None else self._map[section]
        inner_dict[key] = value
        self.update_config_resouce(key=key, value=str(value), section=section)


    @abstractmethod
    def update_config_resouce(self, key : str, value : str, section : Optional[str] = None):
        pass


    @staticmethod
    def cast_string(value : list[str] | ConfigValue) -> ConfigValue:
        try:
            value = ast.literal_eval(value)
        except (ValueError, SyntaxError):
            pass
        return value


    @staticmethod
    def check_list_ok(the_list : list):
        if len(the_list) == 0:
            return True
        if not isinstance(the_list[0], BasicValue):
            raise ValueError(f'List the_lists must be of type {BasicValue} got:'
                             f' {the_list[0]} of type {type(the_list[0])}')
        list_dtype = type(the_list[0])
        print(f'List dtype = {list_dtype}')
        is_uniform = all(isinstance(entry, list_dtype) for entry in the_list)
        if not is_uniform:
            raise ValueError(f'List values must be of the same type, got : {the_list}')


def flatten(obj : dict) -> dict:
    flat_dict = {}

    def add(key : str, value : object):
        if key in flat_dict:
            raise ValueError(f'Key {key} already exists in flattened dictionary')
        flat_dict[key] = value

    for k1, v1 in obj.items():
        if isinstance(v1, dict):
            flattened_subdict = flatten(v1)
            for k2, v2 in flattened_subdict.items():
                add(key=k2, value=v2)
        else:
            add(key=k1, value=v1)
    return flat_dict


def check_dtype_confirmity(obj : object, dtype : type) -> bool:
    if get_origin(dtype) is list:
        if not isinstance(obj, list):
            return False
        if not get_args(dtype):
            return False
        element_type = get_args(dtype)[0]
        return all([isinstance(x, element_type) for x in obj])
    else:
        obj_conforms = isinstance(obj, dtype)
    return obj_conforms