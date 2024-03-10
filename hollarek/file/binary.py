from .file import File

class BinaryFile(File):
    def read(self) -> bytes:
        with open(self.fpath, 'rb') as file:
            content = file.read()
        return content


    def write(self,content: bytes):
        with open(self.fpath, 'wb') as file:
            file.write(content)

    def view(self):
        content = self.read()
        hex_content = content.hex()
        for i in range(0, len(hex_content), 20):
            line = ' '.join(hex_content[j:j + 2] for j in range(i, min(i + 20, len(hex_content)), 2))
            print(line)

    def decode(self, encoding='utf-8', error_handling='strict') -> str:
        content = self.read()
        return content.decode(encoding, errors=error_handling)