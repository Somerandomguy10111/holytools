import os
def load_asset_as_bytes(filename: str) -> bytes:
    module_dir = os.path.dirname(__file__)
    file_path = os.path.join(module_dir, filename)
    try:
        with open(file_path, 'rb') as file:
            return file.read()
    except FileNotFoundError:
        print(f"File {filename} not found.")
        return b''  # Return empty bytes if the file does not exist

def get_test_png() -> bytes:
    return load_asset_as_bytes('test.png')

def get_test_jpg() -> bytes:
    return load_asset_as_bytes('test.jpg')

def get_test_pdf() -> bytes:
    return load_asset_as_bytes('test.pdf')

def get_test_txt() -> bytes:
    return load_asset_as_bytes('test.txt')

def get_test_csv() -> bytes:
    return load_asset_as_bytes('test.csv')


if __name__ == "__main__":
    png_content = get_test_png()
    jpg_content = get_test_jpg()
    pdf_content = get_test_pdf()
    txt_content = get_test_txt()
    csv_content = get_test_csv()