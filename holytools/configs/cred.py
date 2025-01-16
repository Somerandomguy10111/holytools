import sys

from holytools.configs import FileConfigs
import argparse


def main():
    configs = FileConfigs(encrypted=True, fpath=f'~/.pyconfigs.txt')

    num_args = len(sys.argv) - 1

    if num_args == 0:
        print(f'Credential store content')
        content = configs.read().strip()
        lines = content.split(f'\n')
        for l in lines:
            if len(l) > 0 and not l.startswith(f'['):
                l = f'├── {l}'
            print(l)
    elif num_args == 2:
        arg1 = sys.argv[1]
        if arg1 == 'insert':
            arg2 = sys.argv[2]
            if not arg2:
                raise ValueError(f'No key provided')
            value = input(f'Enter value for key \"{arg2}\": ')
            configs.set(key=arg2, value=value)
        else:
            raise ValueError(f'Unknown command \"{arg1}\"')
    else:
        raise ValueError(f'Invalid command syntax: {sys.argv}')



if __name__ == "__main__":
    main()