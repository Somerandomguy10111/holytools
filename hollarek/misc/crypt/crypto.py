from abc import abstractmethod, ABC


class Crypto:
    @abstractmethod
    def encrypt(self, content: str, key: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, key: str, content: str) -> str:
        pass