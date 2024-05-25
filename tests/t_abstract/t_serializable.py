from __future__ import annotations
from uuid import UUID
from enum import Enum
from datetime import datetime, date, time
from dataclasses import dataclass, field
from tempfile import NamedTemporaryFile
from abc import abstractmethod
from holytools.abstract import SerializableType, JsonDataclass
from holytools.devtools import Unittest


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


simple_data_instance = SimpleDataclass(
    id=1,
    name='Test',
    timestamp=datetime.now(),
    is_active=True,
    unique_id=UUID('12345678-1234-5678-1234-567812345678')
)

# This is to prevent discovery of the base test
class HiderClass:
    class SerializationBase(Unittest):
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
                dictionary_data: dict[str, str] = field(default_factory=dict)

                def __post_init__(self):
                    self.dictionary_data = {'key1': 'value1', 'key2': 'value2'}

            instance = ComplexDataclass(
                date_field=test_date,
                time_field=test_time,
                enum_field=ThisParticularEnum.OPTION_A,
                simple_data=simple_data_instance
            )

            return instance, ComplexDataclass


        def test_tostr_fromstr_roundtrip(self):
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
            original_dict = str(obj1.__dict__)
            reloaded_dict = str(obj2.__dict__)
            self.assertEqual(original_dict, reloaded_dict)
            print()
            print(f'{original_dict}, {reloaded_dict} for {self.__class__.__name__}')


        @classmethod
        @abstractmethod
        def get_serializable(cls) -> SerializableType:
            pass


class TestJsonDataclass(HiderClass.SerializationBase):
    @classmethod
    def get_serializable(cls):
        from holytools.abstract.serialization import JsonDataclass
        return JsonDataclass


class TestDillable(HiderClass.SerializationBase):
    @classmethod
    def get_serializable(cls):
        print(f' Getting serializable for Dillable')
        from holytools.abstract.serialization import Dillable
        return Dillable

class TestPicklable(HiderClass.SerializationBase):
    @classmethod
    def get_serializable(cls):
        from holytools.abstract.serialization import Picklable
        return Picklable

    def get_instance_and_cls(self) -> (SerializableType, type[SerializableType]):
        instance = simple_data_instance
        cls = SimpleDataclass
        return instance, cls


if __name__ == '__main__':
    TestJsonDataclass.execute_all()
    # dill has a known issue that prevents it from serializing "Enums defined in __main__" in particular
    # see: https://github.com/uqfoundation/dill/issues/250
    # Hence if you execute it via __main__ rather than via unittest discovery you will see an error
    TestDillable.execute_all()
    TestPicklable.execute_all()
