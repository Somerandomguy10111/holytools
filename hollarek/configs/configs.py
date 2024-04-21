import os.path
from configobj import ConfigObj
from .abstr import Configs
# ---------------------------------------------------------


class ConfigFile(Configs):
    def __init__(self, config_fpath : str = os.path.expanduser('~/.pyconfig')):
        super().__init__()
        self._config_fpath : str = config_fpath
        self._map : ConfigObj = ConfigObj()
        self.log(f'Initialized {self.__class__.__name__} with \"{self._config_fpath}\"')

    def set(self, key : str, value:  str):
        self._map[key] = value
        self._map.write(outfile=self._config_fpath)

    def _retrieve_map(self) -> ConfigObj:
        return ConfigObj(self._config_fpath)

# configs using unix pass
# class PassConfig(Configs):
#     pass
