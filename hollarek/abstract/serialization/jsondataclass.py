from __future__ import annotations

import orjson
import dataclasses
from datetime import datetime, date, time
from typing import get_type_hints, get_origin, get_args, Union
from types import NoneType

from enum import Enum
from .serializable import Serializable
# -------------------------------------------


class JsonDataclass(Serializable):
    def __init__(self):
        if not dataclasses.is_dataclass(self):
            raise TypeError(f'{self.__class__} must be a dataclass to be Jsonifyable')

    @classmethod
    def from_str(cls, json_str: str):
        json_str_dict = orjson.loads(json_str)
        return from_json(cls=cls, json_dict=json_str_dict)

    def to_str(self) -> str:
        return orjson.dumps(self.to_json()).decode("utf-8")

    def to_json(self) -> dict:
        return {attr: get_json_entry(obj=value) for attr, value in self.__dict__.items()}

    @classmethod
    def from_json(cls, json_dict : dict) -> JsonDataclass:
        return from_json(cls=cls, json_dict=json_dict)


def get_json_entry(obj):
    if hasattr(obj, '__dict__'):
        entry = {attr: value for attr, value in obj.__dict__.items() if not callable(value)}
    else:
        entry = obj
    return entry


def from_json(cls : type, json_dict: dict):
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f'{cls} is not a dataclass. from_json can only be used with dataclasses')

    type_hints = get_type_hints(cls)
    init_dict = {}
    for key, value in json_dict.items():
        if value is None:
            init_dict[key] = value
            continue

        core_type = get_core_type(dtype=type_hints.get(key))
        if not isinstance(value, dict):
            init_dict[key] = make_elementary(cls=core_type,value=value)
        elif issubclass(core_type, Enum):
            init_dict[key] = core_type(value['_value_'])
        else:
            init_dict[key] = from_json(cls=core_type, json_dict=value)

    return cls(**init_dict)


def make_elementary(cls, value : str):
    conversion_map = {
        datetime: datetime.fromisoformat,
        date: date.fromisoformat,
        time: time.fromisoformat,
    }

    typecast_classes = ['Decimal', 'UUID', 'Path', 'str', 'int', 'float', 'bool']
    if cls in conversion_map:
        return conversion_map[cls](value)
    elif cls.__name__ in typecast_classes or issubclass(cls, Enum):
        return cls(value)
    else:
        raise TypeError(f'Unsupported type {cls}')

# noinspection DuplicatedCode
def get_core_type(dtype : type) -> type:
    if get_origin(dtype) is Union:
        types = get_args(dtype)
        core_types = [t for t in types if not t is NoneType]
        if len(core_types) == 1:
            return core_types[0]
        else:
            raise ValueError(f'Union dtype {dtype} has more than one core dtype')
    else:
        return dtype