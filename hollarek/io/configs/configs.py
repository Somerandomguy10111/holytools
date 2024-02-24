import io
import os.path
import boto3
import json
from configparser import ConfigParser
from typing import Optional

from hollarek.crypt import AES
from hollarek.cloud import AWSRegion
from hollarek.dev import LogLevel
from hollarek.io.configs.abstr import Configs
from .abstr import Settings
# ---------------------------------------------------------



class AWSConfigs(Configs):
    def __init__(self, secret_name : str, region : AWSRegion):
        super().__init__()
        self.secret_name  : str = secret_name
        self.region_name : str = region.value
        self.settings: dict[str, str] = self.retrieve_settings()
        session = boto3.session.Session()
        self.client = session.client(service_name='secretsmanager', region_name=self.region_name)


    def set(self, key : str, value : str):
        pass


    def retrieve_settings(self) -> Optional[Settings]:
        settings = None
        try:
            secret_value = self.client.get_secret_value(SecretId=self.secret_name)
            settings = json.loads(secret_value['SecretString'])

        except Exception as e:
            self.log(f'An error occurred while trying to read value from AWS: {e}', LogLevel.ERROR)

        return settings


class LocalConfigs(Configs):
    CATEGORY_NAME = 'GENERAL'

    def __init__(self, config_fpath : str = os.path.expanduser('~/.pyconfig'),
                       encryption_key : Optional[str] = None):
        super().__init__()
        self._config_fpath : str = config_fpath
        self._parser : ConfigParser = self.make_parser()
        self._aes : AES = AES()
        self._encr_key : Optional[str] = encryption_key

        self.log(f'Initialized {self.__class__.__name__} with \"{self._config_fpath}\"')


    @staticmethod
    def make_parser():
        parser : ConfigParser = ConfigParser()
        parser.add_section(LocalConfigs.CATEGORY_NAME)
        return parser


    def retrieve_settings(self) -> Settings:
        self._parser.read_string(self.get_decrypted_from_file())
        return dict(self._parser.items(section=LocalConfigs.CATEGORY_NAME))


    def set(self, key : str, value:  str):
        self._settings[key] = value
        self._parser.set(LocalConfigs.CATEGORY_NAME, key, value)

        with open(self._config_fpath, 'w') as configfile:
            encr = self.get_encrypted_from_settings()
            configfile.write(encr)

    # -------------------------------------------
    # encryption

    def get_encrypted_from_settings(self) -> str:
        with io.StringIO() as configIO:
            self._parser.write(configIO)
            config_str = configIO.getvalue()
        return self._encrypt(content=config_str)


    def get_decrypted_from_file(self) -> str:
        with open(self._config_fpath, 'r') as configfile:
            decrypted_data = self._decrypt(configfile.read().strip())
            return decrypted_data


    def _encrypt(self, content : str) -> str:
        encr = self._aes.encrypt(content=content, key = self._encr_key) if self._encr_key else content
        return encr


    def _decrypt(self, content : str) -> str:
        decr = self._aes.decrypt(content=content, key=self._encr_key) if self._encr_key else content
        return decr



if __name__ == "__main__":
    conf = LocalConfigs(encryption_key='abc')
