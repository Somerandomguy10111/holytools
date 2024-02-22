from types import NoneType
from typing import get_origin, Union, get_args



def get_type_list(dtype : type) -> list:
    """
    :return: If dtype is of form Union[<dtype>] returns [<dtype1>, <dtype2>,...] ; Else returns [<dtype>]
    """
    if get_origin(dtype) is Union:
        return list(get_args(dtype))
    else:
        return [dtype]


def get_core_type(dtype : type):
    """
    :return: If dtype is of form Optional[<dtype>] returns <dtype>; Else returns <dtype>
    """
    if get_origin(dtype) is Union:
        types = get_args(dtype)

        core_types = [t for t in types if not t is NoneType]
        if len(core_types) == 1:
            return core_types[0]
        else:
            raise ValueError(f'Union dtype {dtype} has more than one core dtype')
    else:
        return dtype


def is_optional_type(dtype : type):
    """
    :return: Returns true if <dtype> is of form Optional[<dtype>] or Union[None, (...)]; Else returns false
    """
    if get_origin(dtype) is Union:
        types = get_args(dtype)
        return any([t for t in types if t is NoneType])

    return False

#
# if __name__ == '__main__':
#     from typing import Optional
#    # Test get_type_list
#     print("Testing get_type_list...")
#     print(get_type_list(int))  # Expected: [int]
#     print(get_type_list(Union[int, float]))  # Expected: [int, float]
#     print(get_type_list(Union[int, None]))  # Expected: [int, NoneType]
#
#     # Test get_core_type
#     print("\nTesting get_core_type...")
#     print(get_core_type(int))  # Expected: int
#     print(get_core_type(Optional[int]))  # Expected: int
#     # This should raise an error
#     try:
#         print(get_core_type(Union[int, str]))  # Expected: ValueError
#     except ValueError as e:
#         print(e)

from hollarek.dev.test import Unittest
from typing import Optional, Union, get_origin, get_args


class TestIsOptionalType(Unittest):
    def test_optional_type(self):
        self.assertTrue(is_optional_type(Optional[int]))
        self.assertTrue(is_optional_type(Union[None, int]))
        self.assertTrue(is_optional_type(Union[int, None]))

    def test_non_optional_type(self):
        self.assertFalse(is_optional_type(int))
        self.assertFalse(is_optional_type(Union[int, str]))
        self.assertFalse(is_optional_type(float))

    def test_complex_optional_type(self):
        self.assertTrue(is_optional_type(Optional[Union[int, str]]))
        self.assertTrue(is_optional_type(Union[None, int, str]))

    def test_none_type(self):
        self.assertFalse(is_optional_type(None))
        self.assertFalse(is_optional_type(NoneType))

    def setUp(self):
        pass



if __name__ == '__main__':
    test = TestIsOptionalType()
    test.run_tests()