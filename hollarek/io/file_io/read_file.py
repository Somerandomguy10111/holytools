from pypdf import PdfReader
from enum import Enum

class TextFileType(Enum):
    PLAINTEXT = 'plain'
    PDF = 'pdf'

    @classmethod
    def from_str(cls, str_repr : str):
        str_repr = str_repr.lower()
        for file_type in cls:
            if file_type.value == str_repr:
                return file_type
        return None


def get_text(fpath: str, file_type : TextFileType = TextFileType.PLAINTEXT) -> str:
    if file_type == TextFileType.PLAINTEXT:
        return _get_plain_text_content(file_path=fpath)
    elif file_type == TextFileType.PDF:
        return _get_pdf_file_content(file_path=fpath)


def _get_plain_text_content(file_path : str) -> str:
    with open(file_path, 'r') as file:
        file_content = file.read()
    return file_content


def _get_pdf_file_content(file_path : str) -> str:
    pdf_file = open(file_path, 'rb')
    pdf_reader = PdfReader(pdf_file)

    pdf_content = ''
    for page in pdf_reader.pages:
        pdf_content += page.extract_text()

    pdf_file.close()

    return pdf_content