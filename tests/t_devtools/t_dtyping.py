from typing import Optional, Union
from hollarek.devtools import Unittest, TypeInspector



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
            self.assertTrue(TypeInspector.is_optional_type(dtype), msg=f'\"{dtype}\" should be recognized as Optional')

    def test_complex_optional_type(self):
        for dtype in [self.nested_optional, self.triple_union]:
            self.assertTrue(TypeInspector.is_optional_type(dtype), msg=f'\"{dtype}\" should be recognized as Optional')


    def test_non_optional_type(self):
        for dtype in [int, Union[int, str], float]:
            self.assertFalse(TypeInspector.is_optional_type(dtype), msg=f'\"{dtype}\" should not be recognized as Optional')



if __name__ == "__main__":
    TestOptionalTyping.execute_all()
    # print(is_optional_type(Optional[Union[int,str]]))