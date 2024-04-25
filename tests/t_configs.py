from abc import abstractmethod
from hollarek.configs import Configs, FileConfigs, PassConfigs
from hollarek.devtools import Unittest
from unittest.mock import patch
from hollarek.fsys import SaveManager


class BaesConfigTest(Unittest):
    def setUp(self):
        args = () if Configs == PassConfigs else SaveManager.tmp_fpath()
        self.configs = Configs(*args)
        self.test_key = "test_key"
        self.test_val = "test_value"
        self.configs._map[self.test_key] = self.test_val
        self.configs.is_setup = True

    def test_set_get(self):
        self.configs.set(key=self.test_key, value=self.test_val)
        value = self.configs.get(self.test_key)
        self.assertEqual(value, self.test_val)

    def test_z_renewed_access(self):
        value = self.configs.get(self.test_key)
        self.assertEqual(value, self.test_val)

    @patch('builtins.input', lambda *args : '42')
    def test_get_nonexistent_key(self):
        value = self.configs.get('non_existent key')
        self.assertEqual(value,'42')

    @abstractmethod
    def get_configs(self) -> Configs:
        pass


class FileConfigsTests(BaesConfigTest):
    def get_configs(self) -> Configs:
        return FileConfigs()

class PassConfigTests(BaesConfigTest):
    def get_configs(self) -> Configs:
        return PassConfigs(pass_dirpath='"/home/daniel/Drive/.password-store')

if __name__ == '__main__':
    FileConfigsTests.execute_all()
    PassConfigTests.execute_all()