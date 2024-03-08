from typing import Any
import inspect
from dataclasses import dataclass
from typing import Callable



@dataclass
class Argument:
    name : str
    dtype : type
    default_val : Any


class ModuleInspector:
    @staticmethod
    def get_methods(cls : type, public_only = False) -> list[Callable]:
        if public_only:
            attr_filter = lambda attr : callable(getattr(cls, attr)) and not attr.startswith("_")
        else:
            attr_filter = lambda attr : callable(getattr(cls, attr))
        public_methods = [method for name,method in cls.__dict__.items() if attr_filter(name)]
        return public_methods


    @staticmethod
    def get_args(func: Callable) -> list[Argument]:
        spec = inspect.getfullargspec(func)
        start_index = 1 if spec.args and spec.args[0] in ['self', 'cls'] else 0
        defaults = spec.defaults or ()
        defaults_mapping = dict(zip(spec.args[::-1], defaults[::-1]))

        args = []
        for arg_name in spec.args[start_index:]:
            dtype = spec.annotations.get(arg_name, Any)
            default_val = defaults_mapping.get(arg_name)
            args.append(Argument(name=arg_name,dtype=dtype,default_val=default_val))

        return args



# if __name__ == "__main__":
#     print(ModuleInspector.get_methods(cls=TestClass))