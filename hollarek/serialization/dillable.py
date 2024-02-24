import dill
from abc import ABC


class Dillable(ABC):
    def to_str(self) -> str:
        return dill.dumps(self).hex()

    @classmethod
    def from_str(cls, dill_str: str):
        return dill.loads(bytes.fromhex(dill_str))


# Example usage:
if __name__ == "__main__":
    class Example(Dillable):
        def __init__(self, data):
            self.data = data

    original = Example(data="Sample data")
    test_dill_str = original.to_str()
    restored = Example.from_str(test_dill_str)

    print(f"Original: {original.data}")
    print(f"Restored: {restored.data}")
