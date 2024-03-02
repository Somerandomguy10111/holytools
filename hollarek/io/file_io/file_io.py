from abc import abstractmethod
from hollarek.dev.log import Loggable

class FileIO(Loggable):
    @staticmethod
    @abstractmethod
    def read(fpath : str):
        pass

    @staticmethod
    @abstractmethod
    def write(fpath : str, content):
        pass

