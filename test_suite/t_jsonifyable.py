from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from hollarek.templates import JsonDataclass


@dataclass
class Person(JsonDataclass):
    name: str
    age: int


@dataclass
class ComplexPerson(JsonDataclass):
    timestamp: datetime  # Testing proper templates of datetime
    person : Person


@dataclass
class FaultyPerson(JsonDataclass):
    name: str
    unsupported: set  # 'set' is not directly JSON templates





if __name__ == "__main__":
    person_json = '{"name": "John Doe", "age": 30}'
    person = Person.from_str(person_json)
    complex_person = ComplexPerson(person=person, timestamp=datetime.now())
    faulty_person = FaultyPerson(name="Faulty", unsupported={1, 2, 3})

    print(person.to_str())  # Convert back to JSON string
    complex_str = complex_person.to_str()

    loaded_person = ComplexPerson.from_str(json_str=complex_str)

    try:
        print(faulty_person.to_str())  # This should raise an exception
    except TypeError as e:
        print(f"Expected error for non-serializable type: {e}")

