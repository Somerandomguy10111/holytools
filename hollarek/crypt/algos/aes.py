import os
from base64 import b64encode, b64decode
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from hollarek.dev.log import get_logger, LogLevel
from typing import Optional

from hollarek.crypt.hash import SHA
from .crypto_algo import CryptoAlgo
# -------------------------------------------

log = get_logger().log

class AES(CryptoAlgo):
    def __init__(self):
        self.backend = default_backend()
        self.sha = SHA()


    def encrypt(self, content: str, key : str) -> str:
        byte_content = content.encode()
        byte_key, iv = self.sha.get_hash(txt=key), os.urandom(16)

        encryptor = self._get_encryptor(byte_key=byte_key, iv=iv)
        encrypted_content = encryptor.update(byte_content) + encryptor.finalize()
        return b64encode(iv + encrypted_content).decode()


    def decrypt(self, key : str, content: str) -> Optional[str]:
        encrypted_data = b64decode(content)
        byte_key = self.sha.get_hash(txt=key)
        iv, data  = encrypted_data[:16], encrypted_data[16:]
        decryptor = self._get_decryptor(byte_key=byte_key, iv=iv)

        decrypted_content = decryptor.update(data) + decryptor.finalize()
        try:
            decoded = decrypted_content.decode()
        except UnicodeDecodeError:
            log(f'Error decoding bytes to UTF-8. Most likely the decryption key is not correct', level=LogLevel.WARNING)
            decoded = None

        return decoded

    # -------------------------------------------
    # get

    def _get_encryptor(self, byte_key : bytes, iv : bytes):
        return self._get_cipher(key=byte_key, iv=iv).encryptor()

    def _get_decryptor(self, byte_key : bytes, iv : bytes):
        return self._get_cipher(key=byte_key, iv=iv).decryptor()

    def _get_cipher(self, key : bytes, iv : bytes):
        return Cipher(algorithms.AES(key), modes.CFB(iv), backend=self.backend)

