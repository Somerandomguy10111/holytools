import os.path
from configparser import ConfigParser
from enum import Enum

class StdCategories(Enum):
    GENERAL = 'GENERAL'
    APIS = 'APIS'


class ConfigManager:
    def __init__(self, config_file_location : str = os.path.expanduser('~/.py_config_manager')):
        self._config_fpath : str = config_file_location
        self._parser : ConfigParser = ConfigParser()


    def get_value(self, key: str, category : Enum) -> str:
        try:
            value =self._read_value(key=key, category=category)
        except:
            value = input(f'Could not retrieve {key} from config file. Please set it manually:\n'
                          f'Note: Entered key will be saved in {self._config_fpath} for future use\n')
            self._write_value(key=key, value=value, category=category)
        return value


    def _read_value(self, key: str, category : Enum) -> str:
        self._update_parser(fpath=self._config_fpath)
        return self._parser.get(category.value, key)


    def _write_value(self, key: str, value: str, category : Enum):
        self._update_parser(fpath=self._config_fpath)
        self._set(key=key, value=value, section=category.value)
        self._update_file(parser=self._parser)

    # -------------------------------------------
    # updates

    def _update_file(self, parser : ConfigParser):
        with open(self._config_fpath, 'w') as configfile:
            parser.write(configfile)


    def _update_parser(self, fpath : str):
        self._parser.read(fpath)


    def _set(self, key : str, value : str, section : str):
        if not self._parser.has_section(section):
            self._parser.add_section(section)
        self._parser.set(section, key, value)


if __name__ == "__main__":
    conf = ConfigManager()
    conf.get_value(key='abc', category=StdCategories.GENERAL)

