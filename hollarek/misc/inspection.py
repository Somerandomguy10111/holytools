import inspect


def get_function_code(func: callable) -> str:
    return inspect.getsource(func)


def get_function_kwargs(func: callable) -> list[str]:
    func_sig = inspect.signature(func)
    params = list(func_sig.parameters.keys())
    return params
