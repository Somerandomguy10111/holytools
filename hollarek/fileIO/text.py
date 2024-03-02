from docx import Document
import textract
from .file_io import IO

class TextIO(IO):
    @staticmethod
    def read(fpath: str) -> str:
        text = textract.process(fpath)
        return text.decode('utf-8')

    @staticmethod
    def write(fpath: str, content: str) -> None:
        parts = fpath.split('.')
        suffix = parts[-1] if len(parts) > 1 else None

        if suffix == 'docx':
            doc = Document()
            doc.add_paragraph(content)
            doc.save(fpath)
        elif suffix == 'txt' or suffix is None:
            with open(fpath, 'w', encoding='utf-8') as file:
                file.write(content)
        else:
            raise ValueError(f'Unsupported file type: {suffix}')
