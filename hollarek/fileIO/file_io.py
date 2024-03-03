from abc import abstractmethod
from hollarek.logging import Loggable

class IO(Loggable):
    @staticmethod
    @abstractmethod
    def read(fpath : str):
        pass

    @staticmethod
    @abstractmethod
    def write(fpath : str, content):
        pass

