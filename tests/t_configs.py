import tempfile
import uuid
from abc import abstractmethod

from holytools.configs import BaseConfigs, FileConfigs, PassConfigs
from holytools.devtools import Unittest


# ---------------------------------------------------------

class Hider:
    class ConfigTest(Unittest):
        def setUp(self):
            self.configs_fpath : str = tempfile.mktemp()
            self.configs = self.get_configs()

        def test_set_get(self):
            key, value = self.make_random_str(), self.make_random_str()
            self.configs.set(key=key, value=value)

            new_configs = self.get_configs()
            new_value = new_configs.get(key)
            self.assertEqual(new_value, value)

        def test_set_get_section(self):
            section = self.make_random_str()
            key, value = self.make_random_str(), self.make_random_str()
            self.configs.set(key=key, value=value, section=section)

            new_configs = self.get_configs()
            new_value = new_configs.get(key)
            self.assertEqual(new_value, value)

        # ---------------------------------------------------------

        @staticmethod
        def make_random_str() -> str:
            return str(uuid.uuid4())

        @abstractmethod
        def get_configs(self) -> BaseConfigs:
            pass


class PassConfigTests(Hider.ConfigTest):
    def get_configs(self) -> BaseConfigs:
        return PassConfigs()

class FileConfigsTests(Hider.ConfigTest):
    def get_configs(self) -> BaseConfigs:
        return FileConfigs(fpath=self.configs_fpath)


if __name__ == '__main__':
    FileConfigsTests.execute_all()
    PassConfigTests.execute_all()