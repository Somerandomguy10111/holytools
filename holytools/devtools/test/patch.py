import unittest.mock
import inspect
from holytools.file.types.file import File
from typing import Callable
import os


def patch_module(original : type | Callable, replacement : type | Callable):
    module_path = inspect.getmodule(original).__name__
    qualified_name = original.__qualname__
    full_path = f"{module_path}.{qualified_name}"

    print(f'Original full path = {full_path}')

    def decorator(func):
        return unittest.mock.patch(full_path, replacement)(func)
    return decorator




if __name__ == "__main__":
    class CustomFile:
        @staticmethod
        def write():
            print(f'Pranked!')


    class TestTheWriting(unittest.TestCase):
        @unittest.mock.patch('holytools.file.types.file.File', CustomFile)
        def test_do_write(self):
            print(f'The file type is = {File}')
            print(f'Writing to ')
            thefile = File(fpath='abc')
            print(os.path.abspath(thefile.fpath))
            thefile.write(content='this content')

    class RealCar:
        def drive(self):
            return "Driving the Real Car"


    class FakeCar:
        def drive(self):
            return "Driving the Fake Car"


    # Test case using unittest
    class TestCarRental(unittest.TestCase):
        @patch_module(RealCar, FakeCar)
        def test_rent_a_fake_car(self):
            result = rent_a_car()
            print(f'Result = {result}')
            # Verify that we are using the FakeCar's drive method instead of the RealCar's
            self.assertEqual(result, "Driving the Fake Car")


    # A function that creates and uses a RealCar
    def rent_a_car():
        car = RealCar()
        return car.drive()


    unittest.main()
