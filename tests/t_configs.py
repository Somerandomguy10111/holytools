import unittest
import uuid
from abc import abstractmethod
from io import StringIO
from unittest.mock import patch

from holytools.configs import BaseConfigs, FileConfigs, PassConfigs
from holytools.devtools import Unittest
from holytools.fsys import SaveManager

# ---------------------------------------------------------

class Hider:
    class ConfigTest(Unittest):
        configs_fpath = SaveManager.tmp_fpath()
        pass_dirpath = '/home/daniel/OneDrive/.password-store'

        @classmethod
        def setUpClass(cls):
            cls.configs = cls.get_configs()

        def test_set_get_key(self):
            str_key, str_val = self.make_random_str(), self.make_random_str()
            self.configs.set(key=str_key, value=str_val)
            value = self.configs.get(str_key)
            self.assertEqual(value, str_val)

        def test_section_set_get(self):
            section = self.make_random_str()
            key, value = self.make_random_str(), self.make_random_str()
            self.configs.set(key=key, value=value, section=section)
            value = self.configs.get(key=key, section=section)
            self.assertEqual(value, value)

        # ---------------------------------------------------------

        @staticmethod
        def make_random_str() -> str:
            return str(uuid.uuid4())

        @classmethod
        @abstractmethod
        def get_configs(cls) -> BaseConfigs:
            pass


class PassConfigTests(Hider.ConfigTest):
    @classmethod
    def get_configs(cls) -> BaseConfigs:
        return PassConfigs(pass_dirpath=cls.pass_dirpath)


class FileConfigsTests(Hider.ConfigTest):
    @classmethod
    def get_configs(cls) -> BaseConfigs:
        return FileConfigs(fpath=cls.configs_fpath)


if __name__ == '__main__':
    # FileConfigsTests.execute_all()
    PassConfigTests.execute_all()

    # confs = FileConfigs(f'test')
    # confs.set(key='newnew', value='asdf', section='!!!')
    # confs.get(key='newnew')
    # Hider.PassConfigTests.execute_all()
    # configs = FileConfigs()
    # configs2 = FileConfigs()
    # import unittest

    # loader = unittest.TestLoader()
    # tests = loader.discover('/home/daniel/misc/holytools/tests', pattern='t_*.py')
    # str_io = StringIO()
    # testRunner = unittest.runner.TextTestRunner(stream=str_io)
    # testRunner.run(tests)
    # print(f'{str_io.getvalue()}')