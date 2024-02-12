import inspect, os
from typing import Optional

def get_parentfile_path() -> Optional[str]:
    try:
        frame = inspect.currentframe().f_back.f_back
        filename = frame.f_globals["__file__"]
        rootpath = os.path.abspath(filename)
    except:
        rootpath = None
    return rootpath