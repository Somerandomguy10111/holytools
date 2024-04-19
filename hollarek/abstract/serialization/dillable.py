import dill
from pickle import dumps, loads
from .serializable import Serializable

class Dillable(Serializable):
    def to_str(self) -> str:
        return dill.dumps(self).hex()

    @classmethod
    def from_str(cls, dill_str: str):
        return dill.loads(bytes.fromhex(dill_str))


class Picklable(Serializable):
    def to_str(self) -> str:
        return dumps(self).hex()

    @classmethod
    def from_str(cls, pickl_str: str):
        return loads(bytes.fromhex(pickl_str))


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
