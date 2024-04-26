import uuid
from abc import abstractmethod
from unittest.mock import patch

from holytools.configs import Configs, FileConfigs, PassConfigs
from holytools.devtools import Unittest
from holytools.fsys import SaveManager

# ---------------------------------------------------------

class BaseConfigTests(Unittest):
    configs_fpath = SaveManager.tmp_fpath()

    def setUp(self):
        self.configs = self.get_configs()
        self.test_key = "test_key"
        self.test_val = "test_value"


    @patch('builtins.input', lambda *args : '42')
    def test_get_nonexistent_key(self):
        non_existent_key = str(uuid.uuid4())
        self.configs.get(non_existent_key)
        value = self.configs.get(non_existent_key)
        print(f'Value is {value}')
        self.assertEqual(value, 42)


    def test_set_get_key(self):
        self.configs.set(key=self.test_key, value=self.test_val)
        value = self.configs.get(self.test_key)
        self.assertEqual(value, self.test_val)

        expected_val = False
        bool_key = str(uuid.uuid4())
        self.configs.set(key=bool_key, value=expected_val)
        actual = self.configs.get(key=bool_key)
        self.assertEqual(actual, expected_val)


    @patch('builtins.input', lambda *args: '')
    def test_new_obj_get(self):
        new_key = str(uuid.uuid4())
        self.configs.set(key=new_key, value=self.test_val)

        new_configs = self.get_configs()
        value = new_configs.get(key=new_key)
        self.assertEqual(value, self.test_val)

    # ---------------------------------------------------------

    @abstractmethod
    def get_configs(self) -> Configs:
        pass


class FileConfigsTests(BaseConfigTests):
    def get_configs(self) -> Configs:
        return FileConfigs(config_fpath=self.configs_fpath)

class PassConfigTests(BaseConfigTests):
    def get_configs(self) -> Configs:
        return PassConfigs(pass_dirpath='/home/daniel/Drive/.password-store')

if __name__ == '__main__':
    FileConfigsTests.execute_all()
    PassConfigTests.execute_all()
    # configs = FileConfigs()
    # configs2 = FileConfigs()