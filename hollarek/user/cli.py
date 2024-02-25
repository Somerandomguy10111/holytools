import inspect


class InteractiveCLI:
    def __init__(self, cls : type, description : str = ''):
        self.cls : type = cls
        self.description : str = description
        self.obj : object = self.initialize_object()
        self.methods_dict : dict[int, callable] = self.get_methods_dict(obj=self.obj)


    def initialize_object(self):
        print(f"Description: {self.description}\n")
        print(f'Object {self.cls.__name__} requires initialization arguments: ')
        arg_names = inspect.getfullargspec(self.cls.__init__).args[1:]
        init_kwargs = {}
        for arg in arg_names:
            init_kwargs[arg] = input(f"Enter value for {arg}: ")
        return self.cls(**init_kwargs)


    def get_methods_dict(self, obj) -> dict[int, callable]:
        public_methods_names = self.get_public_method_names()
        return {i + 1: getattr(obj,name) for i, name in enumerate(public_methods_names)}


    def get_public_method_names(self) -> list[str]:
        is_public_callable = lambda attr: callable(getattr(self.obj, attr)) and not attr.startswith("_")
        public_method_names = [method for method in dir(self.obj) if is_public_callable(method)]
        return public_method_names


    def loop(self):
        while True:
            print("\nAvailable methods:")
            exit_str = 'q'
            for index, method in self.methods_dict.items():
                print(f"{index}: {method.__name__}")
            user_input = input(f"\nChoose a method by entering its number (or type '{exit_str} to quit): ")

            if user_input.lower() == exit_str:
                break

            if not user_input.isdigit() or int(user_input) not in self.methods_dict:
                print("Please enter a valid number.")
                continue

            method_index = int(user_input)
            self.call(method_index)


    def call(self, index : int):
        mthd = self.methods_dict[index]
        spec = inspect.getfullargspec(mthd)
        if spec.args[1:]:
            arg_value = input(f"Enter value for {spec.args[1]}: ")
            result = mthd(arg_value)
        else:
            result = mthd()
        print(f"Result: {result}")


class TestClass:
    def __init__(self, name):
        self.name = name

    def greet(self):
        return f"Hello, {self.name}!"

    def update_name(self, new_name):
        self.name = new_name
        return f"Name updated to {self.name}"


if __name__ == "__main__":
    cli = InteractiveCLI(TestClass)
    cli.loop()