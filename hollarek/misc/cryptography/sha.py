from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend



class SHA:
    @staticmethod
    def hash_string(input_string: str, bit_length: int = 256) -> bytes:
        if bit_length == 256:
            algorithm = hashes.SHA256()
        elif bit_length == 384:
            algorithm = hashes.SHA384()
        elif bit_length == 512:
            algorithm = hashes.SHA512()
        else:
            raise ValueError("Unsupported bit length for SHA hash.")

        digest = hashes.Hash(algorithm=algorithm, backend=default_backend())
        digest.update(input_string.encode())
        return digest.finalize()

