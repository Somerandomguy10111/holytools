from __future__ import annotations
from uuid import UUID
from enum import Enum
from datetime import datetime, date, time
from hollarek.templates import JsonDataclass
from dataclasses import dataclass, field
from hollarek.devtools import Unittest

@dataclass
class SimpleDataclass:
    id: int
    name: str
    timestamp: datetime
    is_active: bool
    unique_id: UUID
    # Add more fields as needed

@dataclass
class ComplexDataclass(JsonDataclass):
    date_field: date
    time_field: time
    enum_field: MyEnum  # Define MyEnum based on your needs
    simple_data: SimpleDataclass
    # Add more fields as needed

# Define MyEnum here
class MyEnum(Enum):
    OPTION_A = 1
    OPTION_B = 2


class TestJsonDataclass(Unittest):

    @classmethod
    def setUpClass(cls):
        pass

    def test_store_load(self):
        # Create an instance of ComplexDataclass
        original_data = ComplexDataclass(
            date_field=date.today(),
            time_field=time(12, 34, 56),
            enum_field=MyEnum.OPTION_A,
            simple_data=SimpleDataclass(
                id=1,
                name='Test',
                timestamp=datetime.now(),
                is_active=True,
                unique_id=UUID('12345678-1234-5678-1234-567812345678'),
            )
        )

        # Serialize and then deserialize the data
        serialized_str = original_data.to_str()
        reloaded_data = ComplexDataclass.from_str(serialized_str)
        self.assertEqual(original_data.__dict__, reloaded_data.__dict__, "Original and reloaded data should match")


    def test_invalid(self):
        with self.assertRaises(TypeError):
            @dataclass
            class InvalidDataclass(JsonDataclass):
                my_set: set = field(default_factory=set)

                def __post_init__(self):
                    self.my_set = {1, 2, 3}

            this = InvalidDataclass()
            this.to_str()

        with self.assertRaises(TypeError):
            class NonDataclass(JsonDataclass):
                pass
            this =NonDataclass()
            this.to_json()

if __name__ == '__main__':
    TestJsonDataclass.execute_all()
