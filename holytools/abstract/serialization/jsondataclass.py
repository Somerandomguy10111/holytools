import dataclasses
from dataclasses import dataclass
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from types import NoneType
from typing import get_type_hints, get_origin, get_args, Union

import orjson
from PIL.Image import Image

from holytools.abstract.serialization.serializable import Serializable
from holytools.fileIO import ImageConverter

BasicSerializable = (bool | int | float | str | Decimal | datetime | date | time | Enum | Image | None | Serializable)

# -------------------------------------------

@dataclass
class JsonDataclass(Serializable):
    """Enables serialization of dataclasses with following attributes:
        - Basic serializable types as defined above
        - Lists, tuples or dicts of basic serializable types"""
    def __init__(self, *args, **kwargs):
        _, __ = args, kwargs
        if not dataclasses.is_dataclass(self):
            raise TypeError(f'{self.__class__} must be a dataclass to be Jsonifyable')

    def to_str(self) -> str:
        json_dict = self.to_dict()
        return orjson.dumps(json_dict).decode("utf-8")

    def to_dict(self) -> dict:
        defined_fields = set([f.name for f in dataclasses.fields(self) if f.init])
        json_dict = {}
        for attr, value in [(attr, value) for attr, value in self.__dict__.items() if attr in defined_fields]:
            if isinstance(value, list):
                entry = [self.get_basic_entry(x) for x in value]
            elif isinstance(value, tuple):
                entry = tuple([self.get_basic_entry(x) for x in value])
            elif isinstance(value, dict):
                entry = {self.get_basic_entry(k) : self.get_basic_entry(v) for k,v in value.items()}
            else:
                entry = self.get_basic_entry(obj=value)
            json_dict[attr] = entry
        return json_dict

    @classmethod
    def from_str(cls, json_str: str):
        if not dataclasses.is_dataclass(cls):
            raise TypeError(f'{cls} is not a dataclass. from_json can only be used with dataclasses')

        json_dict = orjson.loads(json_str)
        return cls.from_dict(json_dict=json_dict)

    @classmethod
    def from_dict(cls, json_dict : dict):
        type_hints = get_type_hints(cls)
        init_dict = {}
        for key, value in json_dict.items():
            dtype = type_hints.get(key)
            if TypeAnalzer.is_optional(dtype) and value is None:
                init_dict[key] = None
                continue
            if dtype is None:
                continue

            dtype = TypeAnalzer.strip_nonetype(dtype)
            origin = get_origin(dtype)
            if origin == list:
                item_type = TypeAnalzer.get_inner_types(dtype)[0]
                restored_value = [cls.make_basic_obj(basic_cls=item_type, entry=x) for x in value]
            elif origin == tuple:
                item_types = TypeAnalzer.get_inner_types(dtype)
                restored_value = tuple([cls.make_basic_obj(basic_cls=item_type, entry=s) for item_type, s in zip(item_types, value)])
            elif origin == dict or dtype == dict:
                key_type, value_type = TypeAnalzer.get_inner_types(dtype)
                key_list = [cls.make_basic_obj(basic_cls=key_type, entry=x) for x in value.keys()]
                value_list = [cls.make_basic_obj(basic_cls=value_type, entry=x) for x in value.values()]
                restored_value = {key: value for key, value in zip(key_list, value_list)}
            else:
                restored_value = cls.make_basic_obj(basic_cls=dtype, entry=value)
            init_dict[key] = restored_value

        return cls(**init_dict)

    @staticmethod
    def get_basic_entry(obj) -> (str | int | dict | NoneType):
        if not isinstance(obj, BasicSerializable):
            raise TypeError(f'Object {obj} is not a basic serializable type')

        if obj is None:
            entry = None
        elif isinstance(obj, JsonDataclass):
            entry = obj.to_dict()
        elif isinstance(obj, Serializable):
            entry = obj.to_str()
        elif isinstance(obj, Enum):
            entry = obj.name
        elif isinstance(obj, float) and obj != obj:
            entry = 'nan'
        elif isinstance(obj, Image):
            entry = ImageConverter.to_base64_str(image=obj)
        elif isinstance(obj, bool):
             entry = bool(int(obj))
        elif isinstance(obj, Decimal):
             entry = str(obj)
        else:
            entry = obj
        return entry

    @staticmethod
    def make_basic_obj(basic_cls, entry : str | int | float | dict):
        castable_classes = ['str', 'int', 'float', 'bool', 'Decimal', 'UUID', 'Path']
        converters = {
            datetime: datetime.fromisoformat,
            date : date.fromisoformat,
            time : time.fromisoformat,
        }

        if basic_cls in converters:
            instance = converters[basic_cls](entry)
        elif basic_cls.__name__ in castable_classes:
            instance = basic_cls(entry)
        elif issubclass(basic_cls, Enum):
            instance =  basic_cls[entry]
        elif issubclass(basic_cls, JsonDataclass):
            instance = basic_cls.from_dict(json_dict=entry)
        elif issubclass(basic_cls, Serializable):
            instance = basic_cls.from_str(entry)
        elif basic_cls == Image:
            instance = ImageConverter.from_base64_str(entry)
        elif basic_cls == NoneType:
            instance = None
        else:
            raise TypeError(f'Unsupported type {basic_cls}')
        return instance


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
    def get_inner_types(dtype : type) -> tuple:
        inner_dtypes = get_args(dtype)
        return inner_dtypes


if __name__ == "__main__":
    pass