from hollarek.userIO import InteractiveCLI

class Person:
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

if __name__ == "__main__":
    # Assuming InteractiveCLI and TestClass are defined
    cli = InteractiveCLI(Person, "This is a test class with various types of methods.")
    cli.loop()
