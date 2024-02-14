from pypdf import PdfReader
from enum import Enum

class FileType(Enum):
    TXT = 'TXT'
    PDF = 'PDF'


def get_text_file_content(fpath: str, file_type : FileType) -> str:
    if file_type == FileType.TXT:
        return _get_plain_text_content(file_path=fpath)
    elif file_type == FileType.PDF:
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