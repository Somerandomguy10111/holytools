from __future__ import annotations
from uuid import UUID
from enum import Enum
from datetime import datetime, date, time
from dataclasses import dataclass, field
from tempfile import NamedTemporaryFile
from abc import abstractmethod
from hollarek.abstract import SerializableType, JsonDataclass
from hollarek.devtools import Unittest


class MyEnum(Enum):
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



class SerializationBaseTest(Unittest):
    # noinspection PyUnresolvedReferences
    @classmethod
    def setUpClass(cls):
        # Setup shared test date and time once for all test methods
        cls.test_date = date.today()
        cls.test_time = time(12, 34, 56)
        cls.test_uuid = UUID('12345678-1234-5678-1234-567812345678')

        ClassType = cls.get_serializable()

        @dataclass
        class ComplexDataclass(ClassType):
            date_field: date
            time_field: time
            enum_field : MyEnum
            simple_data: SimpleDataclass
            dictionary_data: dict[str, str] = field(default_factory=dict)

            def __post_init__(self):
                self.dictionary_data = {'key1': 'value1', 'key2': 'value2'}

        cls.ComplexDataclass = ComplexDataclass

        cls.simple_data_instance = SimpleDataclass(
            id=1,
            name='Test',
            timestamp=datetime.now(),
            is_active=True,
            unique_id=cls.test_uuid
        )
        cls.complex_data_instance = ComplexDataclass(
            date_field=cls.test_date,
            time_field=cls.test_time,
            enum_field=MyEnum.OPTION_A,
            simple_data=cls.simple_data_instance
        )

    def test_serialization_roundtrip(self):
        serialized_str = self.complex_data_instance.to_str()
        reloaded_data = self.ComplexDataclass.from_str(serialized_str)
        self.check_effectively_equal(obj1=self.complex_data_instance, obj2=reloaded_data)

    def test_save_load_roundtrip(self):
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
        self.complex_data_instance.save(temp_file_path, force_overwrite=True)
        reloaded_data = self.ComplexDataclass.load(temp_file_path)

        self.check_effectively_equal(obj1=self.complex_data_instance, obj2=reloaded_data)

    def check_effectively_equal(self, obj1 : object, obj2 : object):
        original_dict = str(obj1.__dict__)
        reloaded_dict = str(obj2.__dict__)
        self.assertEqual(original_dict, reloaded_dict)


    @classmethod
    @abstractmethod
    def get_serializable(cls) -> SerializableType:
        pass


class TestJsonDataclass(SerializationBaseTest):
    @classmethod
    def get_serializable(cls):
        from hollarek.abstract.serialization import JsonDataclass
        return JsonDataclass


class TestDillable(SerializationBaseTest):
    @classmethod
    def get_serializable(cls):
        from hollarek.abstract.serialization import Dillable
        return Dillable



if __name__ == '__main__':
    TestJsonDataclass.execute_all()
    TestDillable.execute_all()
