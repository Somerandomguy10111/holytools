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


def get_temp_test_png() -> str:
    return create_temp_copy('test.png')

def get_temp_test_jpg() -> str:
    return create_temp_copy('test.jpg')

def get_temp_test_pdf() -> str:
    return create_temp_copy('test.pdf')

def get_temp_test_txt() -> str:
    return create_temp_copy('test.txt')

def get_temp_test_csv() -> str:
    return create_temp_copy('test.csv')


if __name__ == "__main__":
    temp_png_path = get_temp_test_png()
    temp_jpg_path = get_temp_test_jpg()
    temp_pdf_path = get_temp_test_pdf()
    temp_txt_path = get_temp_test_txt()
    temp_csv_path = get_temp_test_csv()

    # Print the paths of the temporary files
    print(f"Temporary PNG file created at: {temp_png_path}")
    print(f"Temporary JPG file created at: {temp_jpg_path}")
    print(f"Temporary PDF file created at: {temp_pdf_path}")
    print(f"Temporary TXT file created at: {temp_txt_path}")
    print(f"Temporary CSV file created at: {temp_csv_path}")