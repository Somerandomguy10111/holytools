import os
from tox.run import run


def main():
    mode = 'pkg'
    conditional_recreate = ''
    script_dirpath = os.path.dirname(__file__)
    cwd = os.getcwd()
    os.environ['REPO_DIRPATH'] = cwd
    os.environ['TOX_ENVNAME'] = os.path.basename(cwd)
    args = ('-c', os.path.join(script_dirpath, 'tox.ini'), '-e', mode)
    if conditional_recreate:
        args = (*args,conditional_recreate)

    run(args)

if __name__ == "__main__":
    main()