class Singleton:
    _instance = None
    _is_initialized = False

    @classmethod
    def reset_instance(cls):
        cls.set_instance(instance=None)
        cls.set_initialized(val=False)
        

    def __new__(cls, *args, **kwargs):
        if (args or kwargs) and cls.get_is_initialized():
            raise AlreadyInitialized("Additional arguments provided to an already initialized singleton."
                                     "Cannot re-initialize or modify singleton after it is initialized.")

        if not cls.get_instance():
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
        return cls._is_initialized

    @classmethod
    def set_initialized(cls, val : bool = True):
        cls._is_initialized = val

    @classmethod
    def set_instance(cls, instance : object):
        cls._instance = instance

    @classmethod
    def get_instance(cls):
        return cls._instance

class AlreadyInitialized(Exception):
    """Exception raised when a singleton instance is initialized more than once."""
    def __init__(self, message="Singleton instance has already been initialized"):
        self.message = message
        super().__init__(self.message)