import os.path
from configobj import ConfigObj

import subprocess
from typing import Optional
from holytools.logging import LogLevel
from holytools.configs.abstr import Configs, DictType

# ---------------------------------------------------------

class FileConfigs(Configs):
    def __init__(self, config_fpath : str = os.path.expanduser('~/.pyconfig')):
        self._config_fpath: str = config_fpath
        super().__init__()
        # self.log(f'Initialized {self.__class__.__name__} with \"{self._config_fpath}\"')

    def _retrieve_map(self) -> ConfigObj:
        return ConfigObj(self._config_fpath)

    def update_config_resouce(self, key : str, value : str):
        self._map.write()


class PassConfigs(Configs):
    def __init__(self, pass_dirpath : str):
        self._pass_dirpath: str = pass_dirpath
        os.environ['PASSWORD_STORE_DIR'] = pass_dirpath
        super().__init__()

    def update_config_resouce(self, key : str, value : str):
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




if __name__ == "__main__":
    pass_config = PassConfigs(pass_dirpath='/home/daniel/Drive/.password-store')
    pypi_key = pass_config.get(key='pypi')
    # pass_config.set(key='this', value='that')
    print(pypi_key)
    pass_config.set(key='newnew', value='asdf')
    print(pass_config.get(key='newnew'))

