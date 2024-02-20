from abc import abstractmethod, ABC


class Crypto:
    @abstractmethod
    def encrypt(self, content: str, key: bytes) -> str:
        pass

    @abstractmethod
    def decrypt(self, key: bytes, content: str) -> str:
        pass