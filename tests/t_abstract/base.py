from __future__ import annotations

import json
import random
import unittest
import uuid
from uuid import UUID
from enum import Enum
from datetime import datetime, date, time
from dataclasses import dataclass, field
from tempfile import NamedTemporaryFile
from abc import abstractmethod
from holytools.abstract import SerializableType, JsonDataclass, Serializable
from holytools.devtools import Unittest

# -------------------------------------------


class ThisParticularEnum(Enum):
    OPTION_A = 1
    OPTION_B = 2

    def __str__(self):
        return self.name

@dataclass
class SimpleDataclass(JsonDataclass):
    id: int
    name: str
    timestamp: datetime
    is_active: bool
    unique_id: UUID

    @classmethod
    def make_example(cls) -> SimpleDataclass:
        return cls(id=1, name='Test', timestamp=datetime.now(), is_active=True,
                        unique_id=UUID('12345678-1234-5678-1234-567812345678'))


class SerializableInt(Serializable):
    def __init__(self):
        self.the_int_val : int = random.randint(2, 100)
        self.uuid : int = uuid.uuid4().int

    def to_str(self) -> str:
        the_dict = {'the_int_val': self.the_int_val, 'uuid': self.uuid}
        return json.dumps(the_dict)

    @classmethod
    def from_str(cls, s: str) -> SerializableInt:
        this = cls()
        the_dict = json.loads(s)

        this.the_int_val = the_dict['the_int_val']
        this.uuid = the_dict['uuid']
        return this

    def __eq__(self, other):
        return self.the_int_val == other.the_int_val

    def __hash__(self):
        return self.uuid



class SerializationTest(Unittest):
    def setUp(self):
        if self.__class__ is SerializationTest:
            raise unittest.SkipTest("Skip BaseTest tests, it's a base class")
        self.instance, self.cls = self.get_instance_and_cls()


    def get_instance_and_cls(self) -> (SerializableType, type[SerializableType]):
        test_date = date.today()
        test_time = time(12, 34, 56)

        ClassType = self.get_serializable_type()

        @dataclass
        class ComplexDataclass(ClassType):
            date_field: date
            time_field: time
            enum_field : ThisParticularEnum
            simple_data: SimpleDataclass
            float_list : list[float]
            nan_float_list : list[float]
            float_tuple: tuple[float, float, float]
            int_list : list[int]
            dataclass_list: list[SimpleDataclass]
            serializable_list : list[SerializableInt]
            serializable_dict : dict[SerializableInt, SerializableInt]
            dictionary_data: dict[str, str] = field(default_factory=dict)

            def __post_init__(self):
                self.dictionary_data = {'key1': 'value1', 'key2': 'value2'}

        instance = ComplexDataclass(
            date_field=test_date,
            time_field=test_time,
            float_list=[1.0, 2.0, 3.0],
            float_tuple=(1.0, 2.0, 3.0),
            nan_float_list=[float('nan'), float('nan')],
            int_list=[1, 2, 3],
            dataclass_list=[SimpleDataclass.make_example(), SimpleDataclass.make_example()],
            serializable_list=[SerializableInt(), SerializableInt()],
            serializable_dict={SerializableInt(): SerializableInt(), SerializableInt(): SerializableInt()},
            enum_field=ThisParticularEnum.OPTION_A,
            simple_data=SimpleDataclass.make_example()
        )

        return instance, ComplexDataclass


    def test_ser_deser_roundtrip(self):
        serialized_str = self.instance.to_str()
        reloaded_data = self.cls.from_str(serialized_str)
        self.check_effectively_equal(obj1=self.instance, obj2=reloaded_data)

    def test_save_load_roundtrip(self):
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
        self.instance.save(temp_file_path, force_overwrite=True)
        reloaded_data = self.cls.load(temp_file_path)

        self.check_effectively_equal(obj1=self.instance, obj2=reloaded_data)


    def check_effectively_equal(self, obj1 : object, obj2 : object):
        self.assert_recursively_same(obj1.__dict__, obj2.__dict__)

    @classmethod
    @abstractmethod
    def get_serializable_type(cls) -> SerializableType:
        pass

if __name__ == "__main__":
    SerializationTest.execute_all()