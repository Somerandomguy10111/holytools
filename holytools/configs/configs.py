import os.path
import subprocess
from typing import Optional

from holytools.configs.base import BaseConfigs, DictType
from holytools.logging import LogLevel


# ---------------------------------------------------------


class FileConfigs(BaseConfigs):
    def __init__(self, fpath : str = '~/.pyconfig'):
        self._config_fpath: str = as_absolute(path=fpath)
        config_dirpath = os.path.dirname(self._config_fpath)
        os.makedirs(config_dirpath, exist_ok=True)
        super().__init__()

    def _retrieve_map(self) -> dict:
        with open(self._config_fpath, 'r') as f:
            content = f.read()

        lines = content.split(f'\n')
        current_section = None
        map_dict = {}
        for line in lines:
            if line.startswith('[') and line.endswith(']'):
                current_section = line[1:-1]
                map_dict[current_section] = {}
                continue

            parts = line.split(f' = ')
            if len(parts) < 2:
                continue
            if len(parts) > 2:
                raise ValueError(f'Invalid line in config file: \"{line}\"')

            key, value = parts
            if len(key.split(f' ')) > 1:
                raise ValueError(f'Key must not contain whitespaces, got : \"{key}\"')
            if current_section:
                map_dict[current_section][key] = value
            else:
                map_dict[key] = value
        return map_dict


    def update_config_resouce(self, key : str, value : str, section : Optional[str] = None):
        self._map.write()


class PassConfigs(BaseConfigs):
    def __init__(self, pass_dirpath : str = '~/.password-store' ):
        pass_dirpath = as_absolute(path=pass_dirpath)
        print(f'Password store dir is : "{pass_dirpath}"')
        os.environ['PASSWORD_STORE_DIR'] = pass_dirpath
        self._pass_dirpath : str = pass_dirpath
        super().__init__()

    def update_config_resouce(self, key : str, value : str, section : Optional[str] = None):
        insert_command = f"echo \"{value}\" | pass insert --echo {key}"
        self.try_run_cmd(cmd=insert_command)

    def _retrieve_map(self) -> DictType:
        keys = self.get_keys()
        config_map = {}
        for k in keys:
            config_map[k] = self.try_run_cmd(f'pass {k}')
        return config_map

    # ---------------------------------------------------------

    def try_run_cmd(self, cmd : str) -> Optional[str]:
        try:
            result = subprocess.run(cmd, text=True, capture_output=True, check=True, shell=True)
            return result.stdout.strip()
        except Exception as e:
            self.log(f"An error occurred during command execution, you configuration is likely not saved to pass:\n"
                     f'err = \"{e}\"\n', level=LogLevel.WARNING)
            result = None
        return result

    def get_keys(self) -> list[str]:
        filenames = os.listdir(path=self._pass_dirpath)
        keys = [os.path.splitext(f)[0] for f in filenames if f.endswith('.gpg')]
        return keys


def as_absolute(path : str) -> str:
    path = os.path.expanduser(path=path)
    path = os.path.abspath(path)
    return path


if __name__ == "__main__":
    configs = FileConfigs(fpath='/home/daniel/aimat/ada/configs.txt')
    print(f'configs map = {configs._map}')