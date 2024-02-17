from types import NoneType
from typing import get_origin, Union, get_args


def get_core_type(the_type : type):
    """
    :return: If the_type is of form Optional[<typ>] returns <typ>; Else returns the_type
    """
    if get_origin(the_type) is Union:
        types = get_args(the_type)

        core_types = [t for t in types if not t is NoneType]
        if len(core_types) == 1:
            return core_types[0]
        else:
            raise ValueError(f'Union typ {the_type} has more than one core typ')
    else:
        return the_type
