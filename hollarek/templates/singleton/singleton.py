class Singleton:
    _instance = None
    is_initialized = False

    @classmethod
    def reset_instance(cls):
        cls._instance = None
        cls.is_initialized = False
        

    def __new__(cls, *args, **kwargs):
        print(f'new called with args: {args} and kwargs: {kwargs}')
        if (args or kwargs) and cls.get_is_initialized():
            raise AlreadyInitialized("Additional arguments provided to an already initialized singleton."
                                     "Cannot re-initialize or modify singleton after it is initialized.")

        if not cls._instance:
            cls._instance = super().__new__(cls)

        return cls._instance


    def __init__(self, *args, **kwargs):
        super().__init__()

        if not self.get_is_initialized():
            self.set_initialized()
        else:
            raise AlreadyInitialized(f'Cannot initialize {self.__class__} more than once')

    @classmethod
    def get_is_initialized(cls):
        return cls.is_initialized

    @classmethod
    def set_initialized(cls):
        cls.is_initialized = True

class AlreadyInitialized(Exception):
    """Exception raised when a singleton instance is initialized more than once."""
    def __init__(self, message="Singleton instance has already been initialized"):
        self.message = message
        super().__init__(self.message)