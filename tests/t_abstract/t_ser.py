import dataclasses
from dataclasses import dataclass
from datetime import datetime
from types import UnionType
from uuid import UUID

from holytools.abstract import JsonDataclass, Picklable
from holytools.abstract.serialization import Dillable

import tests.t_abstract.base as base
from holytools.abstract.serialization.jsondataclass import BasicSerializable
from tests.t_abstract.base import BasicDataclass

# -----------------------------------------

class TestJsonDataclass(base.SerializationTest):
    @classmethod
    def get_serializable_type(cls):
        return JsonDataclass

    def test_type_coverage(self):
        basic_types = self.extract_types_from_union(BasicSerializable)
        actual_types = set([f.type for f in dataclasses.fields(BasicDataclass) if f.init])

        for t in basic_types:
            print(t)
            contains = any([b==t for b in actual_types])
            is_subbclass = any(issubclass(b, t) for b in actual_types)
            self.assertTrue(contains or is_subbclass)

    @staticmethod
    def extract_types_from_union(union):
        if isinstance(union, UnionType):
            return list(union.__args__)
        else:
            return [union]

# dill has a known issue that prevents it from serializing "Enums defined in __main__" in particular
# see: https://github.com/uqfoundation/dill/issues/250
class TestDillable(base.SerializationTest):
    @classmethod
    def get_serializable_type(cls):
        return Dillable

class TestPicklable(base.SerializationTest):
    @dataclass
    class PicklableDataclass(Picklable):
        id: int
        name: str
        timestamp: datetime
        is_active: bool
        unique_id: UUID

        @classmethod
        def make_example(cls):
            return cls(id=1, name='Test', timestamp=datetime.now(), is_active=True,
                       unique_id=UUID('12345678-1234-5678-1234-567812345678'))

    # pickle is unable to serialize classes defined in function scope => Cannot use base get_instance
    def get_instance(self):
        return self.PicklableDataclass.make_example()

    # Only needed in base get_instance
    @classmethod
    def get_serializable_type(cls):
        pass


if __name__ == '__main__':
    TestJsonDataclass.execute_all()
    TestPicklable.execute_all()
    TestDillable.execute_all()
