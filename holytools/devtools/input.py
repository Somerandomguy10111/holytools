import builtins


class InputSimulator:
    def __init__(self, inputs : list[str]):
        def generator():
            for inp in inputs:
                yield inp

        self.gen = generator()
        self.original_input = input

    def redirect_input(self):
        builtins.input = self.simulated_input

    def restore_input(self):
        builtins.input = self.original_input

    def simulated_input(self, *args, **kwargs):
        _ = kwargs
        response = next(self.gen)
        combined = f'{args[0]} {response}' if args else response
        print(combined)
        return response

if __name__ == "__main__":
    a = InputSimulator([f'An ice cream please','No, thank you'])
    a.redirect_input()

    item = input('What do you want?')
    r = input(f'Anything else?')

    print(f'done')