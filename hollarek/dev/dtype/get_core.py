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


if __name__ == '__main__':
    from typing import Optional
   # Test get_type_list
    print("Testing get_type_list...")
    print(get_type_list(int))  # Expected: [int]
    print(get_type_list(Union[int, float]))  # Expected: [int, float]
    print(get_type_list(Union[int, None]))  # Expected: [int, NoneType]

    # Test get_core_type
    print("\nTesting get_core_type...")
    print(get_core_type(int))  # Expected: int
    print(get_core_type(Optional[int]))  # Expected: int
    # This should raise an error
    try:
        print(get_core_type(Union[int, str]))  # Expected: ValueError
    except ValueError as e:
        print(e)