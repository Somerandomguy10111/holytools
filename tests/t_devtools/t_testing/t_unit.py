from holytools.devtools import Unittest
from holytools.fileIO import FileIO
import os

# -------------------------------------------

class RealCar:
    @staticmethod
    def drive():
        return "Driving the Real Car"

class FakeCar:
    def drive(self):
        _ = self
        return "Driving the Fake Car"

class CustomFile:
    def __init__(self, fpath : str):
        _ = fpath
        print(f'This is just a *fake* CustomFile you fool!')

    @staticmethod
    def write(content : str):
        _ = content
        return f'Pranked!'


class TestPatchMechanism(Unittest):
    @Unittest.patch_module(FileIO, CustomFile)
    def test_imported_cls(self):
        file_instance = FileIO(fpath='any')
        output = file_instance.write(content='this content')
        self.assertEqual(output, "Pranked!")

    @Unittest.patch_module(RealCar.drive, FakeCar().drive)
    def test_main_file_cls(self):
        car = RealCar()
        result = car.drive()
        self.assertEqual(result, "Driving the Fake Car")

    # noinspection PyNoneFunctionAssignment
    @Unittest.patch_module(print, lambda *args,**kwargs : args[0])
    def test_builtin(self):
        output = print("Hello, world!")
        self.assertEqual(output, "Hello, world!")

    @Unittest.patch_module(os.path.abspath, lambda *args, **kwargs : '/fake/path')
    def test_stdlib_function(self):
        result = os.path.abspath("anything")
        self.assertEqual(result, "/fake/path")


if __name__ == "__main__":
    TestPatchMechanism.execute_all()