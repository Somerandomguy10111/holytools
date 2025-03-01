import json
import random
import unittest
import uuid
from abc import abstractmethod
from dataclasses import dataclass, field
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from tempfile import NamedTemporaryFile
from types import NoneType
from typing import Optional

from PIL.Image import Image

from holytools.abstract import JsonDataclass, Serializable
from holytools.devtools import Unittest
from holytools.fileIO import ExampleFiles


# -------------------------------------------

class SerializationTest(Unittest):
    def setUp(self):
        if self.__class__ is SerializationTest:
            raise unittest.SkipTest("Skip BaseTest tests, it's a base class")
        self.instance : Serializable = self.get_instance()
        self.cls : type[Serializable] = self.instance.__class__

    def test_ser_deser_roundtrip(self):
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
        self.assertSame(obj1.__dict__, obj2.__dict__)

    # ----------------------------


    def get_instance(self) -> Serializable:
        test_date = date.today()
        test_time = time(12, 34, 56)

        ClassType = self.get_serializable_type()

        @dataclass
        class ComplexDataclass(ClassType):
            date_field: date
            time_field: time
            enum_field : ThisParticularEnum
            simple_data: BasicDataclass
            float_list : list[float]
            nan_float_list : list[float]
            float_tuple: tuple[float, float, float]
            int_list : list[int]
            dataclass_list: list[BasicDataclass]
            serializable_list : list[SerializableInt]
            serializable_dict : dict[SerializableInt, SerializableInt]

            dictionary_data: dict[str, str] = field(default_factory=dict)
            optional_data : Optional[str] = None

            def __post_init__(self):
                self.dictionary_data = {'key1': 'value1', 'key2': 'value2'}

        instance = ComplexDataclass(
            date_field=test_date,
            time_field=test_time,
            float_list=[1.0, 2.0, 3.0],
            float_tuple=(1.0, 2.0, 3.0),
            nan_float_list=[float('nan'), float('nan')],
            int_list=[1, 2, 3],
            dataclass_list=[BasicDataclass.make_example(), BasicDataclass.make_example()],
            serializable_list=[SerializableInt(), SerializableInt()],
            serializable_dict={SerializableInt(): SerializableInt(), SerializableInt(): SerializableInt()},
            enum_field=ThisParticularEnum.OPTION_A,
            simple_data=BasicDataclass.make_example(),
        )

        return instance


    @classmethod
    @abstractmethod
    def get_serializable_type(cls):
        pass


class ThisParticularEnum(Enum):
    OPTION_A = 1
    OPTION_B = 2

    def __str__(self):
        return self.name

class SerializableInt(Serializable):
    def __init__(self):
        self.the_int_val : int = random.randint(2, 100)
        self.uuid : int = uuid.uuid4().int

    def to_str(self) -> str:
        the_dict = {'the_int_val': self.the_int_val, 'uuid': self.uuid}
        return json.dumps(the_dict)

    @classmethod
    def from_str(cls, s: str):
        this = cls()
        the_dict = json.loads(s)

        this.the_int_val = the_dict['the_int_val']
        this.uuid = the_dict['uuid']
        return this

    def __eq__(self, other):
        return self.the_int_val == other.the_int_val

    def __hash__(self):
        return self.uuid


@dataclass
class BasicDataclass(JsonDataclass):
    is_active: bool
    id: int
    single_float: float
    name: str
    serializable : SerializableInt
    decimal : Decimal
    dt: datetime
    d : date
    t : time
    enum_field : ThisParticularEnum
    img: Image
    none_obj : NoneType = None

    @classmethod
    def make_example(cls):
        return cls(id=1, name='Test',
                   dt=datetime.now(),
                   decimal=Decimal('1.234'),
                   d=date.today(),
                   t=time(12, 34, 56),
                   enum_field=ThisParticularEnum.OPTION_A,
                   serializable=SerializableInt(),
                   is_active=True,
                   single_float=2.2,
                   img=ExampleFiles.lend_png().read())




if __name__ == "__main__":
    # SerializationTest.execute_all()
    pass


