from typing import Any
from queue import Queue




class InputWaiter:
    _undefined = object()

    def __init__(self, target_value : Any = _undefined):
        self.q = Queue()
        self.target_value : Any = target_value
        self.input_found : bool = False

    def clear(self):
        self.q = Queue()

    def write(self, value):
        self.q.put(value)

    def read(self) -> Any:
        value = self.q.get()
        if not self.target_value == InputWaiter._undefined:
            if value == self.target_value:
                self.input_found = True
        else:
            self.input_found = True
        return value


if __name__ == "__main__":
    waiter = InputWaiter(target_value=None)