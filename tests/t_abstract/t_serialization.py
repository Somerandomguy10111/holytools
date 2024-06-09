from __future__ import annotations

from holytools.abstract import SerializableType
from tests.t_abstract.basetest import SerializationTest, SimpleDataclass


class TestJsonDataclass(SerializationTest):
    @classmethod
    def get_serializable(cls):
        from holytools.abstract.serialization import JsonDataclass
        return JsonDataclass

# dill has a known issue that prevents it from serializing "Enums defined in __main__" in particular
# see: https://github.com/uqfoundation/dill/issues/250
class TestDillable(SerializationTest):
    @classmethod
    def get_serializable(cls):
        print(f' Getting serializable for Dillable')
        from holytools.abstract.serialization import Dillable
        return Dillable

class TestPicklable(SerializationTest):
    @classmethod
    def get_serializable(cls):
        from holytools.abstract.serialization import Picklable
        return Picklable

      # pickle is unable to serialize the complex datacalss
    def get_instance_and_cls(self) -> (SerializableType, type[SerializableType]):
        instance = SimpleDataclass.make_example()
        cls = SimpleDataclass
        return instance, cls


if __name__ == '__main__':
    TestJsonDataclass.execute_all()
    # Hence if you execute it via __main__ rather than via unittest discovery you will see an error
    # TestDillable.execute_all()
    TestPicklable.execute_all()
    TestDillable.execute_all()
