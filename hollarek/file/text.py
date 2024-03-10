from docx import Document
import textract
from .file import File

class TextFile(File):
    def read(self) -> str:
        text = textract.process(self.fpath)
        return text.decode('utf-8')

    def write(self,content: str):
        parts = self.fpath.split('.')
        suffix = parts[-1] if len(parts) > 1 else None

        if suffix == 'docx':
            doc = Document()
            doc.add_paragraph(content)
            doc.save(self.fpath)
        elif suffix == 'txt' or suffix is None:
            with open(self.fpath, 'w', encoding='utf-8') as file:
                file.write(content)
        else:
            raise ValueError(f'Unsupported file type: {suffix}')


    def view(self):
        content = self.read()
        print(content)