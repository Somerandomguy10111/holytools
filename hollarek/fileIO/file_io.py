from abc import abstractmethod
from typing import Optional

class IO:
    def __init__(self, fpath : str):
        self.fpath : str = fpath

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