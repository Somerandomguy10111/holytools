from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from .sha import SHA
from .crypto import Crypto
import os

# -------------------------------------------

class AES(Crypto):
    def __init__(self):
        self.iv = os.urandom(16)
        self.backend = default_backend()
        self.sha = SHA()


    def encrypt(self, content: str, key : str) -> str:
        byte_content, byte_key = content.encode(), self.sha.get_hash(str_key=key)

        encryptor = self._get_encryptor(byte_key=byte_key)
        encrypted_content = encryptor.update(byte_content) + encryptor.finalize()
        return b64encode(self.iv + encrypted_content).decode()


    def decrypt(self, key : str, content: str) -> str:
        if len(key) != 32:
            raise ValueError("Key must be 32 bytes long for AES-256.")

        encrypted_data = b64decode(content)
        byte_key = self.sha.get_hash(str_key=key)
        iv, data  = encrypted_data[:16], encrypted_data[16:]
        decryptor = self._get_decryptor(byte_key=byte_key)

        decrypted_content = decryptor.update(data) + decryptor.finalize()
        return decrypted_content.decode()

    # -------------------------------------------
    # get


    def _get_encryptor(self, byte_key : bytes):
        return self._get_cipher(key=byte_key).encryptor()

    def _get_decryptor(self, byte_key : bytes):
        return self._get_cipher(key=byte_key).decryptor()

    def _get_cipher(self, key : bytes):
        return Cipher(algorithms.AES(key), modes.CFB(self.iv), backend=self.backend)

