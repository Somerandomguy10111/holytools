import os
import shutil
import tempfile
from dataclasses import dataclass


@dataclass
class File:
    fpath : str

    def __post_init__(self):
        if not (os.path.isdir(self.fpath) or os.path.isfile(self.fpath)):
            raise FileNotFoundError(f'File not found: {self.fpath}')

    def get_data(self) -> bytes:
        with open(self.fpath, 'rb') as file:
            return file.read()

def create_temp_copy(filename: str) -> File:
    module_dir = os.path.dirname(__file__)
    original_file_path = os.path.join(module_dir, filename)

    temp_fd, temp_filepath = tempfile.mkstemp(suffix=os.path.splitext(filename)[1], dir='/tmp')
    os.close(temp_fd)
    shutil.copy2(original_file_path, temp_filepath)

    return File(fpath=temp_filepath)

class Spoofer:
    @staticmethod
    def lend_png() -> File:
        file_obj = create_temp_copy('spoof.png')
        return file_obj

    @staticmethod
    def lend_jpg() -> File:
        file_obj = create_temp_copy('spoof.jpg')
        return file_obj

    @staticmethod
    def lend_pdf() -> File:
        file_obj = create_temp_copy('spoof.pdf')
        return file_obj

    @staticmethod
    def lend_txt() -> File:
        file_obj = create_temp_copy('spoof.txt')
        return file_obj

    @staticmethod
    def lend_csv() -> File:
        file_obj = create_temp_copy('spoof.csv')
        return file_obj
