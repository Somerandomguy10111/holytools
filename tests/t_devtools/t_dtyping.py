from typing import Optional, Union
from hollarek.devtools import Unittest, is_optional_type


class TestOptionalTyping(Unittest):
    @classmethod
    def setUpClass(cls):
        cls.optional_int= Optional[int]
        cls.union_none_int= Union[None, int]
        cls.nested_optional = Optional[Union[int,str]]
        cls.triple_union = Union[None, int, str]


    def test_optional_type(self):
        optional_types = [self.optional_int, self.union_none_int]
        for dtype in optional_types:
            self.assertTrue(is_optional_type(dtype), msg=f'\"{dtype}\" should be recognized as Optional')

    def test_complex_optional_type(self):
        for dtype in [self.nested_optional, self.triple_union]:
            self.assertTrue(is_optional_type(dtype), msg=f'\"{dtype}\" should be recognized as Optional')


    def test_non_optional_type(self):
        self.assertFalse(is_optional_type(int))
        self.assertFalse(is_optional_type(Union[int, str]))
        self.assertFalse(is_optional_type(float))



if __name__ == "__main__":
    TestOptionalTyping.execute_all()
    # print(is_optional_type(Optional[Union[int,str]]))