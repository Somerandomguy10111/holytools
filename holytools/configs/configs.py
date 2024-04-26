import os.path
from configobj import ConfigObj

from typing import Optional
import subprocess
from holytools.configs.abstr import Configs, StrMap

# ---------------------------------------------------------

class FileConfigs(Configs):
    def __init__(self, config_fpath : str = os.path.expanduser('~/.pyconfig')):
        super().__init__()
        self._config_fpath : str = config_fpath
        self._map : ConfigObj = ConfigObj(infile=config_fpath)
        self.log(f'Initialized {self.__class__.__name__} with \"{self._config_fpath}\"')

    def set(self, key : str, value:  str):
        self._map[key] = value
        self._map.write()

    def _retrieve_map(self) -> ConfigObj:
        return ConfigObj(self._config_fpath)


class PassConfigs(Configs):
    def __init__(self, pass_dirpath : str):
        super().__init__()
        self._pass_dirpath : str = pass_dirpath
        os.environ['PASSWORD_STORE_DIR'] = pass_dirpath

    def set(self, key : str, value : str):
        self._map[key] = value
        insert_command = f"echo \"{value}\" | pass insert --echo {key}"
        self.run_cmd(cmd=insert_command)


    def _retrieve_map(self) -> StrMap:
        keys = self.get_keys()
        str_map = StrMap()
        for k in keys:
            str_map[k] = self.run_cmd(f'pass {k}')
        return str_map

    def get_keys(self) -> list[str]:
        filenames = os.listdir(path=self._pass_dirpath)
        keys = [os.path.splitext(f)[0] for f in filenames if f.endswith('.gpg')]

        return keys

    @staticmethod
    def run_cmd(cmd : str) -> Optional[str]:
        try:
            result = subprocess.run(cmd, text=True, capture_output=True, check=True, shell=True)
            return result.stdout.strip()
        except Exception as e:
            print(f"An error occurred during command execution {e}")
            result = None
        return result


if __name__ == "__main__":
    pass_config = PassConfigs(pass_dirpath='/home/daniel/Drive/.password-store')
    pypi_key = pass_config.get(key='pypi')
    # pass_config.set(key='this', value='that')
    print(pypi_key)
    pass_config.set(key='newnew', value='asdf')
    print(pass_config.get(key='newnew'))

