from typing import Optional, Union
from hollarek.devtools import Unittest, is_optional_type


class TestIsOptionalType(Unittest):

    @classmethod
    def setup(cls):
        cls.optional_int= Optional[int]
        cls.union_none_int= Union[None, int]


    def test_optional_type(self):
        optional_types = [self.optional_int, self.union_none_int]
        for types in optional_types:
            self.assertTrue(is_optional_type(types))

    def test_non_optional_type(self):
        self.assertFalse(is_optional_type(int))
        self.assertFalse(is_optional_type(Union[int, str]))
        self.assertFalse(is_optional_type(float))

    def test_complex_optional_type(self):
        self.assertTrue(is_optional_type(Optional[Union[int, str]]))
        self.assertTrue(is_optional_type(Union[None, int, str]))



if __name__ == "__main__":
    TestIsOptionalType.execute_all()