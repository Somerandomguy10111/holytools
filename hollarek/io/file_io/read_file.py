import os.path
from pypdf import PdfReader
from enum import Enum
from typing import Optional, Union
from hollarek.dev.log import get_logger
import logging


logger = get_logger()
def log(msg : str, level = logging.INFO):
    logger.log(msg=msg, level=level)


class ReadType(Enum):
    BYTES = 'BYTES'
    STR = 'STR'

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


def read(fpath : str,
         read_type : ReadType = ReadType.STR) -> Optional[Union[str, bytes]]:
    if not os.path.isfile(fpath):
        log(f'No file found at: {fpath}')
        return None

    mode = 'r' if read_type.STR else 'rb'
    with open(fpath, mode) as file:
        return file.read()


if __name__ == '__main__':
    test_fpath = 'write_file.py'
    print(read(test_fpath))