import os.path
from configparser import ConfigParser
from enum import Enum

class StdCategories(Enum):
    GENERAL = 'GENERAL'
    APIS = 'APIS'


class ConfigManager:
    _HEADER_SIGNATURE = '61086fb59b7f281b14cac1eed366fe695bcbbacc4af7647f166f5005bcde2aa7'

    def __init__(self, config_file_location : str = os.path.expanduser('~/.py_credential_manager')):
        self._CONFIG_FILE_LOCATION : str = config_file_location

        if os.path.isfile(self._CONFIG_FILE_LOCATION):
           is_config_manger_file = self._check_for_header_signature()
           if not is_config_manger_file:
               raise ValueError(f'Config file {self._CONFIG_FILE_LOCATION} is missing header signature. Is it a config file from ConfigManager?')
        else:
            self._try_write_header_signature()


    def get_value(self, key: str, category : Enum) -> str:
        try:
            value =self._read_value_from_file(key=key, category=category)
        except:
            value = input(f'Could not retrieve {key} from config file. Please set it manually:\n'
                          f'Note: Entered key will be saved in {self._CONFIG_FILE_LOCATION} for future use\n')
            self._write_value_to_file(key=key, value=value, category=category)
        return value


    def _check_for_header_signature(self) -> bool:
        signature_found = False
        try:
            sinature = self._read_value_from_file(key='config_manager_signature', category=StdCategories.GENERAL)
            signature_found = sinature == ConfigManager._HEADER_SIGNATURE
        except Exception:
            pass

        return signature_found

    def _try_write_header_signature(self):
        try:
            self._write_value_to_file(key='config_manager_signature', value=ConfigManager._HEADER_SIGNATURE, category=StdCategories.GENERAL)
        except IOError as e:
            raise PermissionError(f"Cannot write to {self._CONFIG_FILE_LOCATION}: {e}")


    def _read_value_from_file(self,key: str, category : Enum) -> str:
        section = category.value
        conf_parser = ConfigParser()
        conf_parser.read(self._CONFIG_FILE_LOCATION)
        return conf_parser.get(section, key)


    def _write_value_to_file(self, key: str, value: str, category : Enum):
        section = category.value
        conf_writer = ConfigParser()
        conf_writer.read(self._CONFIG_FILE_LOCATION)
        if not conf_writer.has_section(section):
            conf_writer.add_section(section)
        conf_writer.set(section, key, value)
        with open(self._CONFIG_FILE_LOCATION, 'w') as configfile:
            conf_writer.write(configfile)



if __name__ == "__main__":
    conf = ConfigManager()
    conf.get_value(key='abc', category=StdCategories.GENERAL)