import os
import shutil
import tempfile


def create_temp_copy(filename: str) -> str:
    module_dir = os.path.dirname(__file__)
    original_file_path = os.path.join(module_dir, filename)

    try:
        temp_fd, temp_filepath = tempfile.mkstemp(suffix=os.path.splitext(filename)[1], dir='/tmp')
        os.close(temp_fd)
        shutil.copy2(original_file_path, temp_filepath)

        return temp_filepath
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return ''


class Spoofer:
    @staticmethod
    def get_png() -> str:
        return create_temp_copy('test.png')

    @staticmethod
    def get_jpg() -> str:
        return create_temp_copy('test.jpg')

    @staticmethod
    def get_pdf() -> str:
        return create_temp_copy('test.pdf')

    @staticmethod
    def get_txt() -> str:
        return create_temp_copy('test.txt')

    @staticmethod
    def get_csv() -> str:
        return create_temp_copy('test.csv')