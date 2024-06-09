from __future__ import annotations

import dataclasses
from datetime import datetime, date, time
from enum import Enum
from types import NoneType
from typing import get_type_hints, get_origin, get_args, Union

import orjson
from dataclasses import dataclass
from holytools.abstract.serialization.serializable import Serializable

typecast_classes = ['Decimal', 'UUID', 'Path', 'Enum', 'str', 'int', 'float', 'bool']
conversion_map = {
    datetime: datetime.fromisoformat,
    date: date.fromisoformat,
    time: time.fromisoformat,
}
elementary_type_names : list[str] = typecast_classes + [cls.__name__ for cls in conversion_map.keys()]

# -------------------------------------------

@dataclass
class JsonDataclass(Serializable):
    def __init__(self, *args, **kwargs):
        _, __ = args, kwargs
        if not dataclasses.is_dataclass(self):
            raise TypeError(f'{self.__class__} must be a dataclass to be Jsonifyable')

    def to_str(self) -> str:
        defined_fields = set([f.name for f in dataclasses.fields(self) if f.init])
        json_dict = {attr: get_entry(obj=value) for attr, value in self.__dict__.items() if attr in defined_fields}
        return orjson.dumps(json_dict).decode("utf-8")

    @classmethod
    def from_str(cls, json_str: str):
        json_dict = orjson.loads(json_str)
        if not dataclasses.is_dataclass(cls):
            raise TypeError(f'{cls} is not a dataclass. from_json can only be used with dataclasses')
        type_hints = get_type_hints(cls)
        init_dict = {}
        for key, value in json_dict.items():
            dtype = type_hints.get(key)

            print(f'Dtype = {dtype}')
            print(f'dtype is optional = {TypeAnalzer.is_optional(dtype)}')
            if TypeAnalzer.is_optional(dtype) and value is None:
                init_dict[key] = value
                continue
            if dtype is None:
                continue

            dtype = TypeAnalzer.strip_nonetype(dtype)
            print(f'key, dtype, dtype origin = {key}, {dtype}, {get_origin(dtype)}')
            if get_origin(dtype) == list:
                value = [make_instance(cls=TypeAnalzer.get_core_type(dtype), value=x) for x in value]
            else:
                value = make_instance(cls=TypeAnalzer.get_core_type(dtype), value=value)
            init_dict[key] = value

        return cls(**init_dict)


def get_entry(obj):
    if isinstance(obj, Serializable):
        entry = obj.to_str()
    elif isinstance(obj, Enum):
        entry = obj.value
    elif isinstance(obj, dict):
        entry = orjson.dumps(obj).decode("utf-8")
    elif isinstance(obj, list):
        entry = [get_entry(x) for x in obj]
    else:
        entry = obj
    return entry


def make_instance(cls, value : str):
    if cls in conversion_map:
        return conversion_map[cls](value)
    elif cls.__name__ in typecast_classes:
        return cls(value)
    elif issubclass(cls, Enum):
        return cls(value)
    elif get_origin(cls) == dict:
        value = orjson.loads(value)
    elif issubclass(cls, Serializable):
        value = cls.from_str(value)
    else:
        raise TypeError(f'Unsupported type {cls}')
    return value
        


class TypeAnalzer:
    @staticmethod
    def is_optional(dtype):
        origin = get_origin(dtype)
        if origin is Union:
            return NoneType in get_args(dtype)
        else:
            return False

    # noinspection DuplicatedCode
    @staticmethod
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
    
    @staticmethod
    def get_core_type(dtype : type) -> type:
        try:
            inner_dtype = get_args(dtype)
            return inner_dtype[0]
        except:
            return dtype


if __name__ == "__main__":
    pass