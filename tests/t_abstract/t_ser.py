from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID

from holytools.abstract import JsonDataclass, Picklable
from holytools.abstract.serialization import Dillable

import tests.t_abstract.base as base

# -----------------------------------------



class TestJsonDataclass(base.SerializationTest):
    @classmethod
    def get_serializable_type(cls):
        return JsonDataclass

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
