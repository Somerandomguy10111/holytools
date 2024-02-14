import os

def get_env_variable(key : str) -> str:
    try:
        key = os.getenv(key)
        if key is None:
            raise KeyError
        return key
    except KeyError:
        raise KeyError(f'Environment variable {key} not found')