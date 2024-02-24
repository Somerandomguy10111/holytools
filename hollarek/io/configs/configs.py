import os.path
import boto3
from typing import Optional

from hollarek.crypt import AES
from hollarek.cloud import AWSRegion
from hollarek.dev import LogLevel
from hollarek.io.configs.abstr import Configs
from .abstr import Settings
# ---------------------------------------------------------

class AWSConfigs(Configs):
    def __init__(self, secret_name : str, region : AWSRegion = AWSRegion.EU_NORTH_1):
        super().__init__()
        self.secret_name: str = secret_name
        session = boto3.session.Session()
        self.client = session.client(service_name='secretsmanager', region_name=region.value)
        self.cls_log(f'Initialized {self.__class__.__name__} with region \"{region.value}\"')


    def set(self, key : str, value : str):
        self._settings[key] = value
        self.client.update_secret(SecretId=self.secret_name, SecretString=self._settings.to_str())


    def _retrieve_settings(self):
        try:
            secret_value = self.client.get_secret_value(SecretId=self.secret_name)
            settings = Settings.from_str(secret_value['SecretString'])
        except Exception as e:
            self.cls_log(f'An error occurred while trying to read value from AWS: {e}', LogLevel.ERROR)
            settings = Settings()

        return settings



class LocalConfigs(Configs):
    def __init__(self, config_fpath : str = os.path.expanduser('~/.pyconfig'),
                       encryption_key : Optional[str] = None):
        if LocalConfigs.is_initialized:
            return

        super().__init__()
        self._config_fpath : str = config_fpath
        self._aes : AES = AES()
        self._encr_key : Optional[str] = encryption_key
        self.cls_log(f'Initialized {self.__class__.__name__} with \"{self._config_fpath}\"')


    def set(self, key : str, value:  str):
        self._settings[key] = value
        parent_dir = os.path.basename(self._config_fpath)
        os.makedirs(parent_dir)
        with open(self._config_fpath, 'w') as configfile:
            config_str = self._settings.to_str()
            encr = self._encrypt(content=config_str)
            configfile.write(encr)


    def _retrieve_settings(self):
        try:
            file_content = self._get_file_content()
            settings = Settings.from_str(json_str=file_content)
        except FileNotFoundError:
            settings = Settings()
            self.log(msg=f'Config file \"{self._config_fpath}\" does not exist', level=LogLevel.WARNING)
        return settings

    # -------------------------------------------
    # encryption

    def _get_file_content(self) -> str:
        with open(self._config_fpath, 'r') as configfile:
            decrypted_data = self._decrypt(configfile.read())
            return decrypted_data


    def _encrypt(self, content : str) -> str:
        encr = self._aes.encrypt(content=content, key = self._encr_key) if self._encr_key else content
        return encr


    def _decrypt(self, content : str) -> str:
        decr = self._aes.decrypt(content=content, key=self._encr_key) if self._encr_key else content
        return decr



