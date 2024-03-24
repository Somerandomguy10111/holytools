from enum import Enum

class SelectableEnum(Enum):
    @classmethod
    def from_manual(cls):
        options = [e.name for e in cls]
        while True:
            val = input(f"Creating {cls.__name__} manually, choose one of options {options}, type 'exit' to quit): ")
            if val.lower() == 'exit':
                return None
            try:
                return cls[val]
            except KeyError:
                print("Invalid input. Please try again.")


class NEW(SelectableEnum):
    UP = 'up'
    DOWN = 'downn'

if __name__ == "__main__":
    a = NEW.from_manual()