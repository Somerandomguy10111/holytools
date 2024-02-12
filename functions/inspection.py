import inspect


def get_function_args(func: callable) -> list[str]:
    func_sig = inspect.signature(func)
    params = list(func_sig.parameters.keys())
    return params


