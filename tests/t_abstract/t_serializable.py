from __future__ import annotations
from uuid import UUID
from enum import Enum
from datetime import datetime, date, time
from hollarek.abstract import JsonDataclass
from dataclasses import dataclass, field
from hollarek.devtools import Unittest
from tempfile import NamedTemporaryFile
import os


@dataclass
class SimpleDataclass(JsonDataclass):
    id: int
    name: str
    timestamp: datetime
    is_active: bool
    unique_id: UUID


@dataclass
class ComplexDataclass(JsonDataclass):
    date_field: date
    time_field: time
    enum_field: MyEnum
    simple_data: SimpleDataclass
    dictionary_data: dict[str, str] = field(default_factory=dict)

    def __post_init__(self):
        self.dictionary_data = {'key1': 'value1', 'key2': 'value2'}


class MyEnum(Enum):
    OPTION_A = 1
    OPTION_B = 2


class TestSerializableClasses(Unittest):
    # noinspection PyUnresolvedReferences
    @classmethod
    def setUpClass(cls):
        # Setup shared test date and time once for all test methods
        cls.test_date = date.today()
        cls.test_time = time(12, 34, 56)
        cls.test_uuid = UUID('12345678-1234-5678-1234-567812345678')
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
        reloaded_data = ComplexDataclass.from_str(serialized_str)
        self.assertEqual(self.complex_data_instance.__dict__, reloaded_data.__dict__,
                         "Original and reloaded data should match")

    def test_save_load_roundtrip(self):
        with NamedTemporaryFile(delete=False) as temp_file:
            temp_file_path = temp_file.name
        self.complex_data_instance.save(temp_file_path, force_overwrite=True)
        reloaded_data = ComplexDataclass.load(temp_file_path)
        self.assertEqual(self.complex_data_instance.__dict__, reloaded_data.__dict__,"Original and reloaded data should match")


if __name__ == '__main__':
    TestSerializableClasses.execute_all()
