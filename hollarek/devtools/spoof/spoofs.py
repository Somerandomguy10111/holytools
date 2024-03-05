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
    def __init__(self):
        self.tempfile_paths = []

    def lend_png(self) -> str:
        path = create_temp_copy('spoof.png')
        self.tempfile_paths.append(path)
        return path

    def lend_jpg(self) -> str:
        path = create_temp_copy('spoof.jpg')
        self.tempfile_paths.append(path)
        return path

    def lend_pdf(self) -> str:
        path = create_temp_copy('spoof.pdf')
        self.tempfile_paths.append(path)
        return path

    def lend_txt(self) -> str:
        path = create_temp_copy('spoof.txt')
        self.tempfile_paths.append(path)
        return path

    def lend_csv(self) -> str:
        path = create_temp_copy('spoof.csv')
        self.tempfile_paths.append(path)
        return path