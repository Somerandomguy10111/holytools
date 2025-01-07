def valid_function(arg1: int, arg2: int = 42):
    _, __ = arg1, arg2

def invalid_function(arg1, arg2=42):
    _, __ = arg1, arg2

class SampleClass:
    def method_with_args(self, arg1 : int, arg2 : str='default'):
        pass

    def _private_method(self):
        pass

    def __magic_method__(self):
        pass

    @staticmethod
    def static():
        pass

    @classmethod
    def classmthd(cls):
        pass


class InheritedClass(SampleClass):
    pass

    def new(self):
        pass
