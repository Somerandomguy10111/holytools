from __future__ import annotations

import orjson
import dataclasses
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from uuid import UUID
from pathlib import Path
from typing import get_type_hints

from hollarek.devtools import get_core_type
# -------------------------------------------


class JsonDataclass:
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


def from_json(cls, json_dict: dict):
    if not dataclasses.is_dataclass(cls):
        raise TypeError(f'{cls} must be a dataclass to be Jsonifyable')

    type_hints = get_type_hints(cls)
    init_dict = {}
    for key, value in json_dict.items():
        core_type = get_core_type(dtype=type_hints.get(key))
        if not isinstance(value, dict):
            if core_type in [str, int, float, bool]:
                init_dict[key] = value
            elif core_type is datetime:
                init_dict[key] = datetime.fromisoformat(value) if value else None
            elif core_type is date:
                init_dict[key] = date.fromisoformat(value) if value else None
            elif core_type is time:
                init_dict[key] = time.fromisoformat(value) if value else None
            elif core_type is Decimal:
                init_dict[key] = Decimal(value)
            elif issubclass(core_type, Enum):
                init_dict[key] = core_type(value)
            elif core_type is UUID:
                init_dict[key] = UUID(value)
            elif core_type is Path:
                init_dict[key] = Path(value)
            else:
                raise TypeError(f"Unsupported type for key {key}: {core_type}")
        else:
            init_dict[key] = from_json(cls=core_type, json_dict=value)

    return cls(**init_dict)
