from __future__ import annotations
import time

from holytools.userIO import TrackedInt, CLI
from holytools.devtools import Unittest


class Account:
    def __init__(self, name: str, active: bool = True):
        self.name = name
        self.active = active

    def greet(self):
        return f"Hello, {self.name}! Active status: {self.active}"

    def set_status(self, active: bool):
        self.active = active
        return f"Active status set to {self.active}"

    def update_name(self, new_name: str):
        self.name = new_name
        return f"Name updated to {self.name}"

    def set_details(self, new_name: str, age: int, height: float):
        self.name = new_name
        age = age
        height = height
        return f"Updated details - Name: {self.name}, Age: {age}, Height: {height}"

    def deactivate(self):
        self.active = False
        return "Account deactivated"


class TestTrackedInt(Unittest):
    def test_incrementation(self):
        ti = TrackedInt(start_value=0, finish_value=10)
        for _ in range(20):
            ti += 1
            time.sleep(0.05)

    def test_incremenation_beyond_max_val(self):
        ti = TrackedInt(start_value=0, finish_value=10)
        for _ in range(20):
            ti += 1
            time.sleep(0.05)
        self.assertEqual(ti,20)

    def test_comparison(self):
        ti = TrackedInt(start_value=0, finish_value=10)
        is_smaller =  -1 < ti
        self.assertTrue(is_smaller)

    # def test_sticky(s3

if __name__ == "__main__":
    # Assuming InteractiveCLI and TestClass are defined
    cli = CLI(Account, "This is a test class with various types of methods.")
    cli.command_loop()
    # TestTrackedInt.execute_all()
