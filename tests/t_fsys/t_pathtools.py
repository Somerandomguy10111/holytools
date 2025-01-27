import os
import tempfile

from holytools.devtools import Unittest
from holytools.fsys import PathTools, LocationManager


class TestPathTools(Unittest):
    def setUp(self):
        self.tmp_dirpath = tempfile.mktemp()
        os.makedirs(self.tmp_dirpath)
        self.location_manager = LocationManager(root_dirpath=self.tmp_dirpath)

    def test_ensure_suffix(self):
        self.assertEqual(PathTools.ensure_suffix('testfile', 'txt'), 'testfile.txt')
        self.assertEqual(PathTools.ensure_suffix('testfile.txt', 'txt'), 'testfile.txt')
        self.assertEqual(PathTools.ensure_suffix('testfile.jpg', 'txt'), 'testfile.txt')

    def test_get_suffix(self):
        self.assertEqual(PathTools.get_suffix('file.txt'), 'txt')
        self.assertIsNone(PathTools.get_suffix('file'))

    def test_increment(self):
        initial_dirpath = os.path.join(self.tmp_dirpath, 'testdir')
        d = PathTools.increment_idx_until_free(initial_dirpath)
        self.location_manager.add_dir('testdir')

        d1 = PathTools.increment_idx_until_free(initial_dirpath)
        self.location_manager.add_dir('testdir_1')

        d2 = PathTools.increment_idx_until_free(initial_dirpath)

        self.assertEqual(d, os.path.join(self.tmp_dirpath, 'testdir'))
        self.assertEqual(d1, os.path.join(self.tmp_dirpath, 'testdir_1'))
        self.assertEqual(d2, os.path.join(self.tmp_dirpath, 'testdir_2'))


if __name__ == '__main__':
    # TestFsysNode.execute_all()
    TestPathTools.execute_all()