import os.path
from typing import Optional

import boto3
from boto3.session import Session
from botocore.auth import NoCredentialsError
from botocore.client import BaseClient

from hollarek.crypt import AES
from hollarek.cloud import AWSRegion
from hollarek.logging import LogLevel
from .abstr import StrMap, Configs
# ---------------------------------------------------------

class AWSConfigs(Configs):
    def __init__(self, secret_name : str, region : AWSRegion = AWSRegion.EU_NORTH_1):
        if self.get_is_initialized():
            return

        super().__init__()
        self.secret_name: str = secret_name
        self.region : AWSRegion = region
        self.session = self.create_session()
        self.client = self.session.client(service_name='secretsmanager', region_name=region.value)
        self.log(f'Initialized {self.__class__.__name__} with region \"{region.value}\"')

        err = self._check_errors()
        if err == NoCredentialsError:
            self._set_aws_credentials()
            err = self._check_errors()
        if err:
            raise ConnectionError

    def set(self, key : str, value : str):
        self._map[key] = value
        self.client.update_secret(SecretId=self.secret_name, SecretString=self._map.to_str())

    def _check_errors(self) -> Optional[Exception]:
        err = None
        try:
            self.client.get_secret_value(SecretId=self.secret_name)
        except NoCredentialsError:
            self.log('No AWS credentials found', LogLevel.CRITICAL)
            err = NoCredentialsError
        except Exception as e:
            self.log(f'An error occurred while trying to connect to AWS: {e}', LogLevel.CRITICAL)
            err = e
        return err

    def _set_aws_credentials(self):
        os.environ['AWS_ACCESS_KEY_ID'] = input('Enter your AWS Access key ID: ')
        os.environ['AWS_SECRET_ACCESS_KEY'] = input('Enter your AWS Secret Access Key: ')

        self.log(f'Enter your AWS Access key ID: ')
        key_id = input()
        self.log(f'Enter your AWS Secret Access key: ')
        access_key = input()

        self.log(f'Credentials set successfully')
        self.session = self.create_session(key_id=key_id, access_token=access_key)
        self.client = self.create_client()

    def _retrieve_map(self):
        try:
            secret_value = self.client.get_secret_value(SecretId=self.secret_name)
            settings = StrMap.from_str(secret_value['SecretString'])
        except Exception as e:
            self.log(f'An error occurred while trying to read value from AWS: {e}', LogLevel.ERROR)
            settings = StrMap()

        return settings

    # -------------------------------------------
    # create

    @classmethod
    def create_session(cls, key_id : Optional[str] = None, access_token : Optional[str] = None) -> Session:
        if not key_id or not access_token:
            return boto3.session.Session()
        return boto3.session.Session(aws_access_key_id=key_id, aws_secret_access_key=access_token)

    def create_client(self) -> BaseClient:
        return self.session.client(service_name='secretsmanager', region_name=self.region.value)


class LocalConfigs(Configs):
    def __init__(self, config_fpath : str = os.path.expanduser('~/.pyconfig'),
                       encryption_key : Optional[str] = None):
        if self.get_is_initialized():
            return

        super().__init__()
        self._config_fpath : str = config_fpath
        self._aes : AES = AES()
        self._encr_key : Optional[str] = encryption_key
        self.log(f'Initialized {self.__class__.__name__} with \"{self._config_fpath}\"')


    def set(self, key : str, value:  str):
        self._map[key] = value
        parent_dir = os.path.basename(self._config_fpath)
        os.makedirs(parent_dir)
        with open(self._config_fpath, 'w') as configfile:
            config_str = self._map.to_str()
            encr = self._encrypt(content=config_str)
            configfile.write(encr)


    def _retrieve_map(self):
        try:
            file_content = self._get_file_content()
            settings = StrMap.from_str(json_str=file_content)
        except FileNotFoundError:
            settings = StrMap()
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



