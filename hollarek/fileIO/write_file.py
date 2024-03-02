import os
from typing import Union
# -------------------------------------------

def write(fpath : str,
          content : Union[str, bytes],
          allow_override : bool = True):

    if not allow_override:
        if os.path.exists(fpath):
            print(f'File {fpath} already exists. Skipping write.')
            return

    mode = 'wb' if isinstance(content, bytes) else 'w'
    with open(fpath, mode) as f:
        f.write(content)

def append(fpath : str, content : str):
    with open(fpath, 'a') as f:
        f.write(content)
