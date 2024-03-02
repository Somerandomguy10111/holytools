from .file_io import IO

class BinaryIO(IO):
    @staticmethod
    def read(fpath: str) -> bytes:
        with open(fpath, 'rb') as file:
            content = file.read()
        return content


    @staticmethod
    def write(fpath: str, content: bytes):
        with open(fpath, 'wb') as file:
            file.write(content)