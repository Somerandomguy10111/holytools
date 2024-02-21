import os.path
from configparser import ConfigParser
from enum import Enum
import io
from hollarek.crypt import AES
from typing import Optional

class StdCategories(Enum):
    GENERAL = 'GENERAL'
    APIS = 'APIS'


class ConfigManager:
    def __init__(self, config_fpath : str = os.path.expanduser('~/.py_config'),
                       encryption_key : Optional[str] = None):
        self._config_fpath : str = config_fpath
        self._parser : ConfigParser = ConfigParser()
        self.aes : AES = AES()
        self.encr_key : Optional[str] = encryption_key

        encr_text = f'Encryption: y' if encryption_key else f'Encryption: n'
        print(f'Initialized ConfigManager with \"{self._config_fpath}\ | {encr_text}"')


    def get_value(self, key: str, category : Enum) -> str:
        try:
            if not os.path.isfile(self._config_fpath):
                raise FileNotFoundError
            value =self._read_value(key=key, category=category)
        except:
            value = input(f'Could not retrieve key \"{key}\" from config file, please set it manually. The value will be saved in {self._config_fpath} for future use\n')
            self._write_value(key=key, value=value, category=category)
        return value


    def _read_value(self, key: str, category : Enum) -> str:
        self._update_parser(fpath=self._config_fpath)
        return self._parser.get(category.value, key)


    def _write_value(self, key: str, value: str, category : Enum):
        if os.path.isfile(self._config_fpath):
            self._update_parser(fpath=self._config_fpath)
        self._set(key=key, value=value, section=category.value)
        self._update_file(parser=self._parser)

    # -------------------------------------------
    # updates

    def _update_file(self, parser: ConfigParser):
        with io.StringIO() as configIO:
            parser.write(configIO)
            config_str = configIO.getvalue()
            encrypted_data = self.encrypt(content=config_str)
            with open(self._config_fpath, 'w') as configfile:
                configfile.write(encrypted_data)

    def _update_parser(self, fpath: str):
        with open(fpath, 'r') as configfile:
            decrypted_data = self.decrypt(configfile.read().strip())
            self._parser.read_string(decrypted_data)


    def encrypt(self, content : str) -> str:
        # print(f'Plain text value : {content}')
        encr = self.aes.encrypt(content=content, key = self.encr_key) if self.encr_key else content
        # print(f'Encrypted value: {encr}')
        return encr


    def decrypt(self, content : str) -> str:
        # print(f'Encrypted value: {content}')
        decr = self.aes.decrypt(content=content, key=self.encr_key) if self.encr_key else content
        # print(f'Decrypted value: {decr}')
        return decr


    def _set(self, key : str, value : str, section : str):
        if not self._parser.has_section(section):
            self._parser.add_section(section)
        self._parser.set(section, key, value)



if __name__ == "__main__":
    conf = ConfigManager(encryption_key='abc')
    print(conf.get_value(key='abc', category=StdCategories.GENERAL))


