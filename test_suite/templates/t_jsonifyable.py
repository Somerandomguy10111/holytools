from __future__ import annotations
from datetime import datetime, date, time
from decimal import Decimal
from uuid import UUID
from pathlib import Path
from enum import Enum
from datetime import datetime
from hollarek.templates import JsonDataclass
from dataclasses import dataclass
from hollarek.devtools import Unittest

@dataclass
class SimpleDataclass:
    id: int
    name: str
    timestamp: datetime
    price: Decimal
    is_active: bool
    unique_id: UUID
    file_path: Path
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
    def test_serialization_deserialization(self):
        # Create an instance of ComplexDataclass
        original_data = ComplexDataclass(
            date_field=date.today(),
            time_field=time(12, 34, 56),
            enum_field=MyEnum.OPTION_A,
            simple_data=SimpleDataclass(
                id=1,
                name='Test',
                timestamp=datetime.now(),
                price=Decimal('10.99'),
                is_active=True,
                unique_id=UUID('12345678-1234-5678-1234-567812345678'),
                file_path=Path('/test/path')
            )
        )

        # Serialize and then deserialize the data
        serialized_str = original_data.to_str()
        reloaded_data = ComplexDataclass.from_str(serialized_str)

        # Verify that all attributes match between the original and reloaded data
        self.assertEqual(original_data.__dict__, reloaded_data.__dict__, "Original and reloaded data should match")

    def test_invalid_dataclass_error(self):
        with self.assertRaises(TypeError):
            class InvalidDataclass(JsonDataclass):
                my_set: set = {1, 2, 3}  # Sets are not supported by default JSON

        with self.assertRaises(TypeError):
            # Attempt to serialize an instance of a non-dataclass
            class NonDataclass(JsonDataclass):
                pass
            NonDataclass().to_str()

if __name__ == '__main__':
    unittest.main()
