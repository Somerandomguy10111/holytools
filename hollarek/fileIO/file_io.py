from abc import abstractmethod
from typing import Optional
import os
from enum import Enum


class Access(Enum):
    READABLE = os.R_OK
    WRITABLE = os.W_OK
    EXECUTABLE = os.X_OK

class File:
    def __init__(self, fpath : str, allow_view_only : bool = True, require_executable : bool = False):
        self.fpath : str = fpath
        required_permissions : set[Access] = {Access.READABLE}
        if not allow_view_only:
            required_permissions.add(Access.WRITABLE)
        if require_executable:
            required_permissions.add(Access.EXECUTABLE)

        actual_permissions = {access for access in required_permissions if self.has_permission(access=access)}
        missing_permissions = required_permissions - actual_permissions
        if missing_permissions:
            raise PermissionError(f'File {fpath} does not have required permissions: {missing_permissions}')


    def has_permission(self, access : Access) -> bool:
        if os.path.isdir(self.fpath):
            return False
        if os.path.isfile(self.fpath):
            return os.access(self.fpath, access.value)
        else:
            parent_directory = os.path.dirname(self.fpath)
            return os.access(parent_directory, access.value) if parent_directory else False


    @abstractmethod
    def read(self):
        pass

    @abstractmethod
    def write(self, content):
        pass

    @abstractmethod
    def view(self):
        print(f'Displaying content of file \"{self.fpath}\":')
        print('-'*20)


    def get_suffix(self) -> Optional[str]:
        parts = self.fpath.split('.')
        suffix = parts[-1] if len(parts) > 1 else None
        return suffix

