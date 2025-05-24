import os
import shutil
import tempfile

from holytools.fileIO.filetypes import PlaintextFile, BinaryFile, ImageFile

# ---------------------------------------------------------



class ExampleFiles:
    @staticmethod
    def lend_png() -> ImageFile:
        fpath = ExampleFiles._create_temp_copy('file.png')
        return ImageFile(fpath=fpath)

    @staticmethod
    def lend_jpg() -> ImageFile:
        fpath = ExampleFiles._create_temp_copy('file.jpg')
        return ImageFile(fpath=fpath)

    @staticmethod
    def lend_pdf() -> PlaintextFile:
        fpath = ExampleFiles._create_temp_copy('file.pdf')
        return PlaintextFile(fpath=fpath)

    @staticmethod
    def lend_txt() -> PlaintextFile:
        fpath = ExampleFiles._create_temp_copy('file.txt')
        return PlaintextFile(fpath=fpath)

    @staticmethod
    def lend_csv() -> PlaintextFile:
        fpath = ExampleFiles._create_temp_copy('file.csv')
        return PlaintextFile(fpath=fpath)

    @staticmethod
    def lend_bin() -> BinaryFile:
        fpath = ExampleFiles._create_temp_copy('file.bin')
        return BinaryFile(fpath=fpath)

    @staticmethod
    def lend_wav() -> BinaryFile:
        fpath = ExampleFiles._create_temp_copy('file.wav')
        return BinaryFile(fpath=fpath)

    @staticmethod
    def _create_temp_copy(filename: str) -> str:
        module_dir = os.path.dirname(__file__)
        original_file_path = os.path.join(module_dir, filename)

        temp_fd, temp_filepath = tempfile.mkstemp(suffix=os.path.splitext(filename)[1], dir='/tmp')
        os.close(temp_fd)
        shutil.copy2(original_file_path, temp_filepath)

        return temp_filepath


if __name__ == "__main__":
    print(os.path.abspath(__file__))