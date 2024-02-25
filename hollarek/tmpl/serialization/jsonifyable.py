from __future__ import annotations

import dataclasses
from datetime import datetime
import json
from typing import  get_type_hints
from hollarek.dev import get_core_type
from abc import ABC


# -------------------------------------------

class Jsonifyable(ABC):
    @classmethod
    def from_str(cls, json_str: str):
        json_dict = json.loads(json_str, object_hook=cls.json_decode)
        return cls.from_json(json_dict=json_dict)

    def to_str(self) -> str:
        return json.dumps(self.to_json(), default=self.json_encode)

    def to_json(self) -> dict:
        return {attr : self.get_json_entry(obj=value) for attr, value in self.__dict__.items()}


    def __init__(self):
        if not dataclasses.is_dataclass(self):
            raise TypeError(f'{self.__class__} must be dataclass to be Jsonifyable')


    @classmethod
    def from_json(cls, json_dict : dict) -> Jsonifyable:
        obj = cls.__new__(cls)
        type_hints = get_type_hints(cls)

        print(f'--- Initializing object of class {cls} ---')
        for key, value in json_dict.items():
            core_type = get_core_type(dtype=type_hints.get(key))
            print(f'key, value, type = {key}, {value}, {type_hints.get(key)}')

            if issubclass(core_type, Jsonifyable):
                if not value is None:
                    setattr(obj, key, core_type.from_json(json_dict=value))
            else:
                setattr(obj, key, value)
        return obj


    @staticmethod
    def get_json_entry(obj):
        is_composite = isinstance(obj, Jsonifyable)
        if is_composite:
            return obj.to_json()
        return obj


    @staticmethod
    def json_decode(json_dict):
        for key, value in json_dict.items():
            if isinstance(value, str):
                try:
                    json_dict[key] = datetime.fromisoformat(value)
                except ValueError:
                    pass
        return json_dict

    @staticmethod
    def json_encode(obj):
        if isinstance(obj, datetime):
            return obj.isoformat()
        return json.JSONEncoder().default(obj)