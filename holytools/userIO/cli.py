
from typing import Callable
import inspect
from holytools.logging import Loggable, LogLevel
# ---------------------------------------------------------


class CLI(Loggable):
    _exit_str = 'q'

    def __init__(self, cls : type, description : str = ''):
        super().__init__()
        self._cls : type = cls
        self._desc : str = description

        self._log_header()
        self.obj : object = self._create_object()
        self.methods_dict : dict[int, Callable] = self._get_methods_dict(obj=self.obj)


    def _log_header(self):
        header_size = 40
        cls_name = self._cls.__name__
        hash_count = int(max(header_size-len(cls_name), 0)/2)
        hashes = '-' * hash_count
        self.log(f'{hashes} {cls_name.upper()} CLI {hashes}')
        desc_str = self._desc if self._desc else 'No description found'
        self.log(f"Description: {desc_str} \n")


    def _create_object(self):
        self.log(f'Initializing object {self._cls.__name__}:')
        try:
            init_kwargs = self._get_args_dict(mthd=self._cls.__init__)
            return self._cls(**init_kwargs)
        except Exception as e:
            self.log(f"Error initializing {self._cls.__name__}: {e}. Please try again\n")
            return self._create_object()



    def _get_methods_dict(self, obj) -> dict[int, Callable]:
        public_methods_names = self._get_public_method_names()
        return {i + 1: getattr(obj,name) for i, name in enumerate(public_methods_names)}


    def _get_public_method_names(self) -> list[str]:
        is_public_callable = lambda attr: callable(getattr(self.obj, attr)) and not attr.startswith("_")
        public_method_names = [method for method in dir(self.obj) if is_public_callable(method)]
        return public_method_names

    # ---------------------------------------------------------
    # loop

    def command_loop(self):
        while True:
            self.print_info()
            user_input = input()
            if user_input == self._exit_str:
                break

            if not user_input.isdigit() or int(user_input) not in self.methods_dict:
                self.log("Please enter a valid number.")
                continue

            try:
                result = self._handle_mthd_call(int(user_input))
                msg = f"Result : {result}"
                level = LogLevel.INFO
            except Exception as e:
                msg = f"Error: {e}"
                level = LogLevel.WARNING
            self.log(msg=msg, level=level)


    def print_info(self):
        text = f"\nChoose a method by entering its number or '{self._exit_str}' to quit): "
        for index, method in self.methods_dict.items():
            text += f"\n{index}: {method.__name__}"
        self.log(msg=text)


    def _handle_mthd_call(self, index : int):
        mthd = self.methods_dict[index]
        args_dict = self._get_args_dict(mthd=mthd)
        result = mthd(**args_dict)
        return result


    def _get_args_dict(self, mthd: Callable) -> dict:
        args_dict = {}
        spec = inspect.getfullargspec(mthd)
        annotations = spec.annotations
        for argname in spec.args[1:]:
            typ = annotations.get(argname, str)
            if isinstance(typ, str):
                typ = type(typ)
            user_input = input(f"Enter value for \"{mthd.__name__}\" argument \"{argname}\" ({typ.__name__}): ")
            args_dict[argname] = self._get_value(user_input=user_input, arg_type=typ, arg_name=argname)
        return args_dict


    @staticmethod
    def _get_value(user_input : str, arg_type : type, arg_name : str):
        if arg_type == bool:
            if user_input not in ['0', '1']:
                raise ValueError(f"For argument '{arg_name}', please enter '0' for False or '1' for True.")
            val = bool(int(user_input))
        else:
            try:
                val = arg_type(user_input)
            except ValueError:
                raise ValueError(f"Invalid input type for '{arg_name}'. Expected a value of type {arg_type.__name__}.")
        return val



if __name__ == "__main__":
    pass