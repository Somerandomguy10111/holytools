from abc import abstractmethod
from hollarek.devtools import Loggable

class FileIO(Loggable):
    @staticmethod
    @abstractmethod
    def read(fpath : str):
        pass

    @staticmethod
    @abstractmethod
    def write(fpath : str, content):
        pass

