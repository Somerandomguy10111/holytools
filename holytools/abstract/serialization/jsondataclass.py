from __future__ import annotations

import dataclasses
from datetime import datetime, date, time
from enum import Enum
from types import NoneType
from typing import get_type_hints, get_origin, get_args, Union

import orjson

from holytools.abstract.serialization.serializable import Serializable

typecast_classes = ['Decimal', 'UUID', 'Path', 'str', 'int', 'float', 'bool']
conversion_map = {
    datetime: datetime.fromisoformat,
    date: date.fromisoformat,
    time: time.fromisoformat,
}
elementary_type_names : list[str] = typecast_classes + [cls.__name__ for cls in conversion_map.keys()]

# -------------------------------------------


class JsonDataclass(Serializable):
    def __init__(self):
        if not dataclasses.is_dataclass(self):
            raise TypeError(f'{self.__class__} must be a dataclass to be Jsonifyable')

    @classmethod
    def from_json(cls, json_dict : dict) -> JsonDataclass:
        return from_json(cls=cls, json_dict=json_dict)

    @classmethod
    def from_str(cls, json_str: str):
        json_str_dict = orjson.loads(json_str)
        return from_json(cls=cls, json_dict=json_str_dict)

    def to_str(self) -> str:
        json_dict = self.to_dict()
        return orjson.dumps(json_dict).decode("utf-8")

    def to_dict(self) -> dict:
        return {attr: get_jsonifyable_entry(obj=value) for attr, value in self.__dict__.items()}


def from_json(cls : type, json_dict: dict):
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f'{cls} is not a dataclass. from_json can only be used with dataclasses')
    type_hints = get_type_hints(cls)
    init_dict = {}
    for key, value in json_dict.items():
        if value is None:
            init_dict[key] = value
            continue

        dtype = type_hints.get(key)
        dtype = strip_nonetype(dtype=dtype)
        if dtype.__name__ in elementary_type_names:
            init_dict[key] = make_elementary(cls=dtype,value=value)
        elif issubclass(dtype, Enum):
            init_dict[key] = dtype(value)
        elif get_origin(dtype) == dict:
            init_dict[key] = value
        elif get_origin(dtype) == list:
            init_dict[key] = value
        elif dataclasses.is_dataclass(obj=dtype):
            init_dict[key] = from_json(cls=dtype, json_dict=value)
        else:
            raise TypeError(f'Unsupported type {dtype}')

    return cls(**init_dict)


def get_jsonifyable_entry(obj):
    if isinstance(obj, JsonDataclass):
        entry = obj.to_dict()
    elif isinstance(obj, Enum):
        entry = obj.value
    elif hasattr(obj, '__dict__'):
        entry = {attr: value for attr, value in obj.__dict__.items() if not callable(value)}
    else:
        entry = obj
    return entry


# noinspection DuplicatedCode
def strip_nonetype(dtype : type) -> type:
    origin = get_origin(dtype)
    if origin is Union:
        types = get_args(dtype)
        not_none_types = [t for t in types if not t is NoneType]
        if len(not_none_types) == 1:
            core_type = not_none_types[0]
        else:
            raise ValueError(f'Union dtype {dtype} has more than one core dtype')
    else:
        core_type = dtype
    return core_type


def make_elementary(cls, value : str):
    if cls in conversion_map:
        return conversion_map[cls](value)
    elif cls.__name__ in typecast_classes:
        return cls(value)
    else:
        raise TypeError(f'Unsupported type {cls}')



if __name__ == "__main__":
    this_dtype = list[float]
    print(strip_nonetype(this_dtype))
