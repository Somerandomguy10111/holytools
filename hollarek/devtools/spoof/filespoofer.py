import os
import shutil
import tempfile
from hollarek.file import BinaryFile, ImageFile, TextFile

# ---------------------------------------------------------

def create_temp_copy(filename: str) -> str:
    module_dir = os.path.dirname(__file__)
    original_file_path = os.path.join(module_dir, filename)

    temp_fd, temp_filepath = tempfile.mkstemp(suffix=os.path.splitext(filename)[1], dir='/tmp')
    os.close(temp_fd)
    shutil.copy2(original_file_path, temp_filepath)

    return temp_filepath


class FileSpoofer:
    @staticmethod
    def lend_png() -> ImageFile:
        fpath = create_temp_copy('spoof.png')
        return ImageFile(fpath=fpath)

    @staticmethod
    def lend_jpg() -> ImageFile:
        fpath = create_temp_copy('spoof.jpg')
        return ImageFile(fpath=fpath)

    @staticmethod
    def lend_pdf() -> TextFile:
        fpath = create_temp_copy('spoof.pdf')
        return TextFile(fpath=fpath)

    @staticmethod
    def lend_txt() -> TextFile:
        fpath = create_temp_copy('spoof.txt')
        return TextFile(fpath=fpath)

    @staticmethod
    def lend_csv() -> TextFile:
        fpath = create_temp_copy('spoof.csv')
        return TextFile(fpath=fpath)

    @staticmethod
    def lend_bin():
        fpath = create_temp_copy('spoof.bin')
        return BinaryFile(fpath=fpath)