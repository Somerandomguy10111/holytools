import importlib
import os
import pkgutil
import inspect
import subprocess
import sys


def check_subdir_namecollsions():
    call_stack = inspect.stack()[1]
    caller_source_file = inspect.getmodule(call_stack[0])
    package_path = caller_source_file.__path__
    package_name = caller_source_file.__name__

    imported_names = set()
    for _, module_name, _ in pkgutil.iter_modules(package_path):
        module = importlib.import_module(f"{package_name}.{module_name}")

        dir_names = [name for name in dir(module) if not name.startswith('_')]
        selected_names = dir_names if not hasattr(module,'__all__') else module.__all__

        for name in selected_names:
            if name in imported_names:
                raise ImportError(f"Name collision detected: {name}")
            else:
                imported_names.add(name)


def generate_venv(src_dirpath : str, venv_name : str = 'venv'):
    # setup dependencies
    """
    Generates a venv with all python packages that can be found in src code in src_dirpath
    """

    print(f'-> Creating virtual environment')
    venv_path = os.path.join(venv_name, "bin", "python")
    run_in_shell(f'{sys.executable} -m venv {venv_name}')

    print(f'-> Generating requirements.txt')
    run_in_shell(f'{venv_path} -m pip install pipreqs && pipreqs {src_dirpath}')

    print(f'-> Installing requirements')
    run_in_shell(f"source {venv_name}/bin/activate && pip install -r {src_dirpath}/requirements.txt")


def run_in_shell(cmd_str : str):
    subprocess.run(cmd_str, check=True, executable=f'/bin/bash', shell=True)
