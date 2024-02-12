import subprocess
import sys
import os


def generate_venv(src_dirpath : str, venv_name : str = 'venv'):
    # setup dependencies
    """
    Generates a venv with all python packages that can be found in src code in src_dirpath
    """
    # mk venv

    run = lambda cmd : subprocess.run(cmd, check=True)

    print(f'-> Creating virtual environment')
    venv_path = os.path.join(venv_name, "bin", "python")
    run([sys.executable, "-m", "venv", venv_name])

    # Install generate requirements and install
    print(f'-> Generating requirements.txt')
    run([venv_path, "-m", "pip", "install", "pipreqs"])
    run(["pipreqs", src_dirpath])

    print(f'-> Installing requirements')
    command = f"source {venv_name}/bin/activate && pip install -r {src_dirpath}/requirements.txt"
    subprocess.run(command, shell=True, executable='/bin/bash')


if __name__ == "__main__":
    generate_venv(src_dirpath=os.getcwd())