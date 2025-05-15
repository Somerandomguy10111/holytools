import os
import tempfile

from holytools.fsys import FsysManager
from holytools.devtools import Unittest




class TestFsysManager(Unittest):
    def setUp(self):
        test_root_dir = tempfile.mktemp()
        os.makedirs(test_root_dir, exist_ok=True)
        self.fsys_manager = FsysManager(root_dirpath=test_root_dir)
        self.test_root_dir = test_root_dir

    def test_set_root(self):
        self.assertEqual(self.fsys_manager.get_root_dirpath(), self.test_root_dir)

    def test_dir(self):
        test_dir_path = os.path.join(self.test_root_dir, 'testdir')
        self.assertTrue(os.path.isdir(test_dir_path) == False)

        loc_dirpath = self.fsys_manager.add_dir('testdir')
        self.assertTrue(os.path.isdir(test_dir_path))
        self.assertEqual(test_dir_path, loc_dirpath)

    def test_file(self):
        test_file_path = self.fsys_manager.add_file('testfile.txt')
        self.assertEqual(test_file_path, os.path.join(self.test_root_dir, 'testfile.txt'))


    def test_create_fsys(self):
        example_tree = {
            'a': {
                'b': None,
                'c': {
                    'd': None,
                    'e': None
                },
                'f': 'Content'
            },
            'g': None,
            'h': {
                'i': None
            },
            'empty' : {}
        }
        
        self.fsys_manager.add_tree(root_dirpath=self.fsys_manager.get_root_dirpath(), tree=example_tree)
        testdir = self.fsys_manager.get_root_dirpath()

        def is_registered_dir(path : str):
            is_dir = os.path.isdir(path)
            registered = path in self.fsys_manager.dirpaths
            return is_dir and registered

        def is_registered_file(abspath : str):
            is_file = os.path.isfile(abspath)
            is_registerd = abspath in self.fsys_manager.fpaths
            return is_file and is_registerd

        dir_assertions = {
            "a": True,
            "a/c": True,
            "h": True,
            'empty' : True
        }

        file_assertions = {
            "a/b": False,
            "a/c/d": False,
            "a/c/e": False,
            "a/f": True,
            "g": False,
            "h/i": False,
        }

        for rel_path, expected in dir_assertions.items():
            abs_path = os.path.join(testdir, rel_path)
            print(abs_path)
            self.assertEqual(is_registered_dir(abs_path), expected)

        for rel_path, expected in file_assertions.items():
            abs_path = os.path.join(testdir, rel_path)
            print(abs_path)
            self.assertEqual(is_registered_file(abs_path), expected)

if __name__ == '__main__':
    TestFsysManager.execute_all()
