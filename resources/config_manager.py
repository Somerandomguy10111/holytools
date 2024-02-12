import os.path
from configparser import ConfigParser
from enum import Enum



# def get_client_token() -> str:
#     return _get_value(key='client_auth', category=Category.CLIENT)
#
# def get_zenodo_access_token() -> str:
#     return _get_value(key='zenodo_token', category=Category.ZENODO)
#
# def get_mail_password() -> str:
#     return _get_value(key='mail_pwd', category=Category.MAIL)
#
# def get_google_key() -> str:
#     return _get_value(key='google_key', category=Category.SEARCH_ENGINE)
#
# def get_searchengine_id() -> str:
#     return _get_value(key='search_engine_id', category=Category.SEARCH_ENGINE)


# ---------------------------------------------------------


class Category(Enum):
    pass


class ConfigManager:
    def __init__(self, config_file_location : str = os.path.expanduser('~/.py_credential_manager')):
        self.CONFIG_FILE_LOCATION : str = config_file_location

    def _get_value(self, key: str, category : Category) -> str:
        try:
            value =self._read_value_from_file(key=key, category=category)
        except:
            value = input(f'Could not retrieve {key} from config file. Please set it manually:\n'
                          f'Note: Entered key will be saved in {self.CONFIG_FILE_LOCATION} for future use\n')
            self._write_value_to_file(key=key, value=value, category=category)
        return value


    def _read_value_from_file(self,key: str, category : Category) -> str:
        section = category.value
        conf_parser = ConfigParser()
        conf_parser.read(self.CONFIG_FILE_LOCATION)
        return conf_parser.get(section, key)


    def _write_value_to_file(self, key: str, value: str, category : Category) -> None:
        section = category.value
        conf_writer = ConfigParser()
        conf_writer.read(self.CONFIG_FILE_LOCATION)
        if not conf_writer.has_section(section):
            conf_writer.add_section(section)
        conf_writer.set(section, key, value)
        with open(self.CONFIG_FILE_LOCATION, 'w') as configfile:
            conf_writer.write(configfile)

