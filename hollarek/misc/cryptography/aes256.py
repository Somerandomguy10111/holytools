from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
import os

# -------------------------------------------

class AES:
    def __init__(self):
        self.iv = os.urandom(16)
        self.backend = default_backend()


    def encrypt(self, content: str, key : bytes) -> str:
        encryptor = self._get_encryptor(key=key)
        byte_content = content.encode()
        encrypted_content = encryptor.update(byte_content) + encryptor.finalize()
        return b64encode(self.iv + encrypted_content).decode()


    def decrypt(self, key : bytes, content: str) -> str:
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes long for AES-256.")

        encrypted_data = b64decode(content)
        iv, data  = encrypted_data[:16], encrypted_data[16:]
        decryptor = self._get_decryptor(key=key)

        decrypted_content = decryptor.update(data) + decryptor.finalize()
        return decrypted_content.decode()

    # -------------------------------------------
    # get

    def _get_encryptor(self, key : bytes):
        return self._get_cipher(key=key).encryptor()

    def _get_decryptor(self, key : bytes):
        return self._get_cipher(key=key).decryptor()

    def _get_cipher(self, key : bytes):
        return Cipher(algorithms.AES(key), modes.CFB(self.iv), backend=self.backend)


if __name__ == "__main__":
    pass