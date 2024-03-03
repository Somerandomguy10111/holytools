class Singleton:
    _instance = None
    is_initialized = False

    @classmethod
    def reset_instance(cls):
        cls._instance = None
        cls.is_initialized = False
        

    def __new__(cls, *args, **kwargs):
        if (args or kwargs) and cls.is_initialized:
            print("Warning: Additional arguments provided to an already initialized singleton")

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
            raise AlreadyInitialized(f'Cannot initialize {self.__class__} more than once')


class AlreadyInitialized(Exception):
    """Exception raised when a singleton instance is initialized more than once."""
    def __init__(self, message="Singleton instance has already been initialized"):
        self.message = message
        super().__init__(self.message)