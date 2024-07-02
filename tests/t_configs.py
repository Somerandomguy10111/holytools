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
        pass_dirpath = '/home/daniel/Drive/.password-store'

        @classmethod
        def setUpClass(cls):
            cls.configs = cls.get_configs()


        @patch('builtins.input', lambda *args : '42')
        def test_get_nonexistent_key(self):
            non_existent_key = str(uuid.uuid4())
            self.configs.get(non_existent_key)
            value = self.configs.get(non_existent_key,prompt_if_missing=True)
            print(f'Value is {value}')
            self.assertEqual(value, 42)


        def test_set_get_key(self):
            str_key, str_val = self.make_random_str(), self.make_random_str()
            self.configs.set(key=str_key, value=str_val)
            value = self.configs.get(str_key)
            self.assertEqual(value, str_val)

            expected_val = False
            bool_key = self.make_random_str()
            self.configs.set(key=bool_key, value=expected_val)
            actual = self.configs.get(key=bool_key)
            self.assertEqual(actual, expected_val)


        @patch('builtins.input', lambda *args: '')
        def test_new_obj_get(self):
            str_key, str_val = self.make_random_str(), self.make_random_str()
            self.configs.set(key=str_key, value=str_val)

            new_configs = self.get_configs()
            value = new_configs.get(key=str_key)
            self.assertEqual(value, str_val)

        def test_section_set_get(self):
            section = self.make_random_str()
            key, value = self.make_random_str(), self.make_random_str()
            self.configs.set(key=key, value=value, section=section)
            value = self.configs.get(key=key)
            self.assertEqual(value, value)


        def test_list_of_int_set_get(self):
            key = self.make_random_str()
            list_of_ints = [i for i in range(10)]
            self.configs.set(key=key, value=list_of_ints)
            value = self.configs.get(key=key)
            self.assertEqual(value, list_of_ints)
        # ---------------------------------------------------------

        @staticmethod
        def make_random_str() -> str:
            return str(uuid.uuid4())

        @classmethod
        @abstractmethod
        def get_configs(cls) -> BaseConfigs:
            pass


    class PassConfigTests(ConfigTest):
        @classmethod
        def get_configs(cls) -> BaseConfigs:
            return PassConfigs(pass_dirpath=cls.pass_dirpath)


class FileConfigsTests(Hider.ConfigTest):
    @classmethod
    def get_configs(cls) -> BaseConfigs:
        return FileConfigs(fpath=cls.configs_fpath)


if __name__ == '__main__':
    # FileConfigsTests.execute_all()

    # confs = FileConfigs(f'test')
    # confs.set(key='newnew', value='asdf', section='!!!')
    # confs.get(key='newnew')
    # Hider.PassConfigTests.execute_all()
    # configs = FileConfigs()
    # configs2 = FileConfigs()
    # import unittest

    loader = unittest.TestLoader()
    tests = loader.discover('/home/daniel/misc/holytools/tests', pattern='t_*.py')
    str_io = StringIO()
    testRunner = unittest.runner.TextTestRunner(stream=str_io)
    testRunner.run(tests)
    print(f'{str_io.getvalue()}')