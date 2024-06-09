from __future__ import annotations

import random
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
        self.the_int_val : int = random.randint(2, 10)

    def to_str(self) -> str:
        return str(self.the_int_val)

    @classmethod
    def from_str(cls, s: str) -> SerializableInt:
        this = cls()
        this.the_int_val = int(s)
        return this

    def __eq__(self, other):
        return self.the_int_val == other.the_int_val



class SerializationTest(Unittest):
    def setUp(self):
        self.instance, self.cls = self.get_instance_and_cls()


    def get_instance_and_cls(self) -> (SerializableType, type[SerializableType]):
        test_date = date.today()
        test_time = time(12, 34, 56)

        ClassType = self.get_serializable()

        @dataclass
        class ComplexDataclass(ClassType):
            date_field: date
            time_field: time
            enum_field : ThisParticularEnum
            simple_data: SimpleDataclass
            float_list : list[float]
            int_list : list[int]
            dataclass_list: list[SimpleDataclass]
            serializable_list : list[SerializableInt]
            dictionary_data: dict[str, str] = field(default_factory=dict)

            def __post_init__(self):
                self.dictionary_data = {'key1': 'value1', 'key2': 'value2'}

        instance = ComplexDataclass(
            date_field=test_date,
            time_field=test_time,
            float_list=[1.0, 2.0, 3.0],
            int_list=[1, 2, 3],
            dataclass_list=[SimpleDataclass.make_example(), SimpleDataclass.make_example()],
            serializable_list=[SerializableInt(), SerializableInt()],
            enum_field=ThisParticularEnum.OPTION_A,
            simple_data=SimpleDataclass.make_example()
        )

        return instance, ComplexDataclass


    def test_ser_deser_roundtrip(self):
        if self.__class__ == SerializationTest:
            self.skipTest(reason=f'Cannot test base class')

        serialized_str = self.instance.to_str()
        reloaded_data = self.cls.from_str(serialized_str)
        self.check_effectively_equal(obj1=self.instance, obj2=reloaded_data)

    def test_save_load_roundtrip(self):
        if self.__class__ == SerializationTest:
            self.skipTest(reason=f'Cannot test base class')

        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
        self.instance.save(temp_file_path, force_overwrite=True)
        reloaded_data = self.cls.load(temp_file_path)

        self.check_effectively_equal(obj1=self.instance, obj2=reloaded_data)


    def check_effectively_equal(self, obj1 : object, obj2 : object):
        self.assertRecursivelyEqual(obj1.__dict__, obj2.__dict__)

    @classmethod
    @abstractmethod
    def get_serializable(cls) -> SerializableType:
        pass

