import os
import tempfile

from hollarek.devtools import Unittest
from hollarek.fsys import SaveManager


class TestSaveManager(Unittest):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()

    def test_ensure_suffix(self):
        self.assertEqual(SaveManager.ensure_suffix('testfile', 'txt'), 'testfile.txt')
        self.assertEqual(SaveManager.ensure_suffix('testfile.txt', 'txt'), 'testfile.txt')
        self.assertEqual(SaveManager.ensure_suffix('testfile.jpg', 'txt'), 'testfile.txt')

    def test_get_suffix(self):
        self.assertEqual(SaveManager.get_suffix('file.txt'), 'txt')
        self.assertIsNone(SaveManager.get_suffix('file'))

    def test_get_free_path(self):
        save_dir = self.test_dir
        base_name = 'test'
        suffix = 'txt'

        first_path = os.path.join(save_dir, f'{base_name}.{suffix}')
        with open(first_path, 'w') as f:
            f.write("This is a test.")
        expected_next_path = os.path.join(save_dir, f'{base_name}_1.{suffix}')
        self.assertEqual(SaveManager.get_free_path(save_dir, base_name, suffix), expected_next_path)

    # noinspection PyUnresolvedReferences
    # @classmethod
    # def tearDownClass(cls):
    #     os.rmdir(cls.test_dir)


if __name__ == '__main__':
    # TestFsysNode.execute_all()
    TestSaveManager.execute_all()