from abc import abstractmethod
from hollarek.configs import Configs, ConfigFile
from hollarek.devtools import Unittest
from unittest.mock import patch

class BaesConfigTest(Unittest):
    def setUp(self):
        self.configs = Configs()

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


class FileConfigs(BaesConfigTest):
    def get_configs(self) -> Configs:
        return ConfigFile()


if __name__ == '__main__':
    FileConfigs.execute_all()