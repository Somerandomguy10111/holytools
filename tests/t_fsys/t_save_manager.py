import os
import tempfile

from holytools.devtools import Unittest
from holytools.fsys import PathTools


class TestSaveManager(Unittest):
    @classmethod
    def setUpClass(cls):
        cls.test_dir = tempfile.mkdtemp()

    def test_ensure_suffix(self):
        self.assertEqual(PathTools.ensure_suffix('testfile', 'txt'), 'testfile.txt')
        self.assertEqual(PathTools.ensure_suffix('testfile.txt', 'txt'), 'testfile.txt')
        self.assertEqual(PathTools.ensure_suffix('testfile.jpg', 'txt'), 'testfile.txt')

    def test_get_suffix(self):
        self.assertEqual(PathTools.get_suffix('file.txt'), 'txt')
        self.assertIsNone(PathTools.get_suffix('file'))

    # noinspection PyUnresolvedReferences
    # @classmethod
    # def tearDownClass(cls):
    #     os.rmdir(cls.test_dir)


if __name__ == '__main__':
    # TestFsysNode.execute_all()
    TestSaveManager.execute_all()