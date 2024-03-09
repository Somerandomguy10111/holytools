from typing import Any
import inspect
from dataclasses import dataclass
from typing import Callable


@dataclass
class Argument:
    name: str
    dtype: type

    def set_default_val(self, val: object):
        setattr(self, 'default_val', val)

    def has_default_val(self):
        return hasattr(self, 'default_val')

    def get_default_val(self) -> Any:
        if not self.has_default_val():
            raise AttributeError(f"Argument '{self.name}' has no default value.")
        return getattr(self, 'default_val')


class ModuleInspector:
    @staticmethod
    def get_methods(cls: type, public_only=False) -> list[Callable]:
        if public_only:
            attr_filter = lambda attr: callable(getattr(cls, attr)) and not attr.startswith("_")
        else:
            attr_filter = lambda attr: callable(getattr(cls, attr))
        public_methods = [method for name, method in cls.__dict__.items() if attr_filter(name)]
        return public_methods


    @staticmethod
    def get_args(func: Callable) -> list[Argument]:
        spec = inspect.getfullargspec(func)
        start_index = 1 if spec.args and spec.args[0] in ['self', 'cls'] else 0
        relevant_arg_names = spec.args[start_index:]
        defaults = spec.defaults or ()
        defaults_mapping = dict(zip(spec.args[::-1], defaults[::-1]))

        def create_arg(name : str):
            dtype = spec.annotations.get(name, Any)
            argument = Argument(name=name, dtype=dtype)
            if name in defaults_mapping:
                argument.set_default_val(defaults_mapping[name])
            return argument


        return [create_arg(name=name) for name in relevant_arg_names]