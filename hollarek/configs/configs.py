import os.path
from typing import Optional

import boto3
from boto3.session import Session
from botocore.auth import NoCredentialsError
from botocore.client import BaseClient
from configobj import ConfigObj
from .abstr import StrMap, Configs
# ---------------------------------------------------------

class ConfigsAWS(Configs):
    def __init__(self, secret_name : str, region : str):
        super().__init__()
        self.secret_name: str = secret_name
        self.region : str = region
        self.session = self.create_session()
        self.client = self.session.client(service_name='secretsmanager', region_name=region)
        self.log(f'Initialized {self.__class__.__name__} with region \"{region}\"')

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
            self.critical('No AWS credentials found')
            err = NoCredentialsError
        except Exception as e:
            self.critical(f'An error occurred while trying to connect to AWS: {e}')
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
            self.error(f'An error occurred while trying to read value from AWS: {e}')
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
        return self.session.client(service_name='secretsmanager', region_name=self.region)


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

