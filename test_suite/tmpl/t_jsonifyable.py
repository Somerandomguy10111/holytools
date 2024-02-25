from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from hollarek.tmpl import Jsonifyable


@dataclass
class Person(Jsonifyable):
    name: str
    age: int
    birthday: Optional[datetime] = None


@dataclass
class ComplexPerson(Jsonifyable):
    name: str
    data: dict  # This is to test_suite non-Jsonifyable, but still JSON-compatible
    timestamp: datetime  # Testing proper tmpl of datetime


@dataclass
class FaultyPerson(Jsonifyable):
    name: str
    unsupported: set  # 'set' is not directly JSON tmpl


person_json = '{"name": "John Doe", "age": 30, "birthday": "1992-05-01T00:00:00"}'
person = Person.from_str(person_json)
complex_person = ComplexPerson(name="Alice", data={"key": "value"}, timestamp=datetime.now())
faulty_person = FaultyPerson(name="Faulty", unsupported={1, 2, 3})


if __name__ == "__main__":
    # Object expected to work
    print(person.to_str())  # Convert back to JSON string

    # Object with all JSON-compatible types but not Jsonifyable inherently
    print(complex_person.to_str())

    # Object intended to fail due to containing a non-tmpl 'set'
    try:
        print(faulty_person.to_str())  # This should raise an exception
    except TypeError as e:
        print(f"Expected error for non-serializable type: {e}")