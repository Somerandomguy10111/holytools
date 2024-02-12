import subprocess
import sys
import os


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

if __name__ == "__main__":
    generate_venv(src_dirpath=os.getcwd())