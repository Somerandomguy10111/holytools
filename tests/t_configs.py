from abc import abstractmethod
from holytools.configs import Configs, FileConfigs, PassConfigs
from holytools.devtools import Unittest
from unittest.mock import patch
from holytools.fsys import SaveManager


class BaseConfigTests(Unittest):
    configs_fpath = SaveManager.tmp_fpath()

    @classmethod
    def setUpClass(cls):
        cls.configs = cls.get_configs()
        cls.test_key = "test_key"
        cls.test_val = "test_value"


    @patch('builtins.input', lambda *args : '42')
    def test_get_nonexistent_key(self):
        key = 'non_existent key'
        self.configs.get(key)
        value = self.configs.get(key)
        print(f'Value is {value}')
        self.assertEqual(value,'42')


    def test_set_get(self):
        self.configs.set(key=self.test_key, value=self.test_val)
        value = self.configs.get(self.test_key)
        self.assertEqual(value, self.test_val)


    @patch('builtins.input', lambda *args: '')
    def test_z_renewed_access(self):
        new_configs = self.get_configs()
        value = new_configs.get(key=self.test_key)
        self.assertEqual(value, self.test_val)

    @classmethod
    @abstractmethod
    def get_configs(cls) -> Configs:
        pass


class FileConfigsTests(BaseConfigTests):
    @classmethod
    def get_configs(cls) -> Configs:
        return FileConfigs(config_fpath=cls.configs_fpath)

class PassConfigTests(BaseConfigTests):
    @classmethod
    def get_configs(cls) -> Configs:
        return PassConfigs(pass_dirpath='/home/daniel/Drive/.password-store')

if __name__ == '__main__':
    FileConfigsTests.execute_all()
    PassConfigTests.execute_all()
