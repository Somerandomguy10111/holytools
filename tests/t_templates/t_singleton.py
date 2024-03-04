from hollarek.templates import Singleton, AlreadyInitialized
from hollarek.devtools import Unittest

class SingletonTest(Unittest):
    @classmethod
    def setUpClass(cls):
        pass

    class SingletonSubclass(Singleton):
        def __init__(self, *args, **kwargs):
            if self.is_initialized:
                return

            super().__init__(*args, **kwargs)

    def setUp(self):
        self.SingletonSubclass.reset_instance()  # Resetting Singleton instance before each test

    def test_same_instance(self):
        instance1 = self.SingletonSubclass('arg')
        instance2 = self.SingletonSubclass()
        new = 'abc'
        self.assertIs(instance1, new)

    def test_handle_invalid_init(self):
        with self.assertRaises(AlreadyInitialized):
            self.SingletonSubclass('arg1', kwarg1='kwarg1')
            self.SingletonSubclass('arg2', kwarg2='kwarg2')  # This should raise the error


if __name__ == "__main__":
    SingletonTest.execute_all()