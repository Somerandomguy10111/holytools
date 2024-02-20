from abc import abstractmethod, ABC
from typing import Optional

class Crypto:
    @abstractmethod
    def encrypt(self, content: str, key: str) -> str:
        pass

    @abstractmethod
    def decrypt(self, key: str, content: str) -> Optional[str]:
        pass