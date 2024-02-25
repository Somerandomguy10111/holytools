from hollarek.dev.log import Loggable, LogLevel


class Singleton(Loggable):
    _instance = None
    is_initialized = False

    @classmethod
    def reset_instance(cls):
        cls._instance = None
        cls.is_initialized = False
        

    def __new__(cls, *args, **kwargs):
        if (args or kwargs) and cls.is_initialized:
            cls.cls_log("Warning: Additional arguments provided to an already initialized singleton",
                        level=LogLevel.WARNING)

        if not cls._instance:
            cls._instance = super().__new__(cls)
        return cls._instance


    def __init__(self, *args, **kwargs):
        super().__init__()
        self.is_initialized = self.__class__.is_initialized

        if not self.is_initialized:
            self.__class__.is_initialized = True
            self.__class__._instance = self
        else:
            raise AlreadyInitialized('Cannot initialize {self.__class__} more than once')


class AlreadyInitialized(Exception):
    """Exception raised when a singleton instance is initialized more than once."""
    def __init__(self, message="Singleton instance has already been initialized"):
        self.message = message
        super().__init__(self.message)