import os
import tempfile

from holytools.fsys import ResourceManager
from holytools.devtools import Unittest

class TestLocationManager(Unittest):
    def setUp(self):
        test_root_dir = tempfile.mktemp()
        os.makedirs(test_root_dir, exist_ok=True)
        self.location_manager = ResourceManager(root_dirpath=test_root_dir)
        self.test_root_dir = test_root_dir

    def test_set_root(self):
        self.assertEqual(self.location_manager.get_root_dirpath(), self.test_root_dir)

    def test_dir(self):
        test_dir_path = os.path.join(self.test_root_dir, 'testdir')
        self.assertTrue(os.path.isdir(test_dir_path) == False)

        loc_dirpath = self.location_manager.add_dir('testdir')
        self.assertTrue(os.path.isdir(test_dir_path))
        self.assertEqual(test_dir_path, loc_dirpath)

    def test_file(self):
        test_file_path = self.location_manager.add_file('testfile.txt')
        self.assertEqual(test_file_path, os.path.join(self.test_root_dir, 'testfile.txt'))

if __name__ == '__main__':
    TestLocationManager.execute_all()
