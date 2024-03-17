from abc import abstractmethod

class Serializable:
    @abstractmethod
    def to_str(self) -> str:
        pass

    @classmethod
    @abstractmethod
    def from_str(cls, s: str):
        pass
