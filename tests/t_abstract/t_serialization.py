from __future__ import annotations

from holytools.abstract import SerializableType
import tests.t_abstract.base as base


class TestJsonDataclass(base.SerializationTest):
    @classmethod
    def get_serializable_type(cls):
        from holytools.abstract.serialization import JsonDataclass
        return JsonDataclass

# dill has a known issue that prevents it from serializing "Enums defined in __main__" in particular
# see: https://github.com/uqfoundation/dill/issues/250
class TestDillable(base.SerializationTest):
    @classmethod
    def get_serializable_type(cls):
        print(f' Getting serializable for Dillable')
        from holytools.abstract.serialization import Dillable
        return Dillable

class TestPicklable(base.SerializationTest):
    @classmethod
    def get_serializable_type(cls):
        from holytools.abstract.serialization import Picklable
        return Picklable

      # pickle is unable to serialize the complex dataclass
    def get_instance_and_cls(self) -> (SerializableType, type[SerializableType]):
        print(f'Using simple dataclass for pickle serialization test')
        instance = base.SimpleDataclass.make_example()
        cls = base.SimpleDataclass
        return instance, cls

if __name__ == '__main__':
    TestJsonDataclass.execute_all()
    TestPicklable.execute_all()
    TestDillable.execute_all()
