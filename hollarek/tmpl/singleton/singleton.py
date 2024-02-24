from ..loggable import Loggable
from abc import abstractmethod, ABC


class Singleton(Loggable, ABC):
    _instance = None
    _is_initialized = False

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, *args, **kwargs):
        super().__init__()
        self.is_initialized = self.__class__._is_initialized
        if (args or kwargs) and self.is_initialized:
            self.log("Warning: Additional arguments provided to an already initialized singleton")

        if not self.is_initialized:
            self.__init__once__()
            self.__class__._initialized = True
        else:
            raise ValueError(f'Cannot initialize {self.__class__} more than once')



    @abstractmethod
    def __init__once__(self):
        pass