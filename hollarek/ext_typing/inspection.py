import inspect
from typing import get_origin, get_args, Union
from types import NoneType



def get_function_args(func: callable) -> list[str]:
    func_sig = inspect.signature(func)
    params = list(func_sig.parameters.keys())
    return params


def get_core_type(the_type : type):
    """
    :return: If the_type is of form Optional[<type>] returns <type>; Else returns the_type
    """
    if get_origin(the_type) is Union:
        types = get_args(the_type)

        core_types = [t for t in types if not t is NoneType]
        if len(core_types) == 1:
            return core_types[0]
        else:
            raise ValueError(f'Union type {the_type} has more than one core type')
    else:
        return the_type