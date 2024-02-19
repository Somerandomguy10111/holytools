import os
import tempfile, shutil

from pathvalidate import sanitize_filename
# -------------------------------------------


def get_folder_zip(input_dir_path : str) -> bytes:
    with tempfile.TemporaryDirectory() as temp_dir:
        base_path = os.path.join(temp_dir, 'data_backup')
        shutil.make_archive(base_name=base_path, format='zip', root_dir=input_dir_path)

        with open(f'{base_path}.zip', 'rb') as file:
            zip_bytes = file.read()

    return zip_bytes


def get_free_path(basepath: str):
    counter = 0
    path = basepath
    while os.path.exists(path):
        unique_suffix = '' if counter == 0 else f'_{counter}'
        path = f'{basepath}{unique_suffix}'
        counter += 1
    return path


def get_writable_name(base_name : str):
    base_name = sanitize_filename(base_name)
    base_name = base_name.replace(' ', '_')
    base_name = base_name.strip()

    return base_name


