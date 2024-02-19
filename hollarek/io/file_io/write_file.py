import os
from typing import Union
# -------------------------------------------

def write_if_free(path : str, content : Union[str, bytes]):
    if os.path.exists(path):
        print(f'File {path} already exists. Skipping write.')
    else:
        write(path=path, content=content)

def write(path : str, content : Union[str, bytes]):
    mode = 'wb' if isinstance(content, bytes) else 'w'
    with open(path, mode) as f:
        f.write(content)