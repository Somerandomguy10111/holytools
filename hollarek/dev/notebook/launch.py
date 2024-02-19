from notebook.app import main
from typing import Optional
import sys


def launch(password_hash: Optional[str] = None):
    sys.argv = ["", "--NotebookApp.token=''", f"--NotebookApp.password='{password_hash}'"]  # Use the hashed password
    main()

if __name__ == '__main__':
    from jupyter_server.auth import passwd
    hashed_pw = passwd(input('Enter notebook password:'))
    launch(password_hash=hashed_pw)