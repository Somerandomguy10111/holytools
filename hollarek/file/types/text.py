import textract
from .file import File

class TextFile(File):
    def read(self) -> str:
        if f'.{self.get_suffix()}' in self.get_non_plaintext_formats():
            binary_data = textract.process(self.fpath)
            text = binary_data.decode('utf-8')
        else:
            with open(self.fpath, 'r') as f:
                text = f.read()
        return text


    def write(self,content: str):
        if f'.{self.get_suffix()}' in self.get_non_plaintext_formats():
            raise ValueError(f'Cannot write to .{self.get_suffix()} files, only to plain text files')
        with open(self.fpath, 'w', encoding='utf-8') as file:
            file.write(content)

    def view(self):
        content = self.read()
        print(content)

    @classmethod
    def get_non_plaintext_formats(cls) -> list[str]:
        return [".doc", ".docx", ".eml", ".epub", ".gif", ".jpg", ".jpeg", ".json", ".html", ".htm",
                    ".msg", ".odt", ".ogg", ".pdf", ".png", ".pptx", ".ps", ".rtf", ".xlsx", ".xls"]
