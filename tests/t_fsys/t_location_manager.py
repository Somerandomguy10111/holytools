import os
from holytools.fsys import LocationManager
from holytools.devtools import Unittest

class TestLocationManager(Unittest):
    #noinspection PyUnresolvedReferences
    @classmethod
    def setUpClass(cls):
        # Define the root directory for testing
        cls.test_root_dir = '/tmp/.testlocationmanager'
        # Ensure the test directory does not already exist
        if not os.path.exists(cls.test_root_dir):
            os.makedirs(cls.test_root_dir)
        # Set the root directory in LocationManager
        LocationManager.set_root(cls.test_root_dir)

    def test_set_root(self):
        # Test setting the root directory successfully
        self.assertEqual(LocationManager.get_root_dirpath(), self.test_root_dir)

    def test_relative_dir(self):
        # Test creating a relative directory
        test_dir_path = LocationManager.relative_dir('testdir')
        self.assertTrue(os.path.isdir(test_dir_path))
        self.assertEqual(test_dir_path, os.path.join(self.test_root_dir, 'testdir'))

    def test_relative_dir_cleanup(self):
        # Ensure that the directory is removed after testing
        test_dir_path = LocationManager.relative_dir('testdir')
        os.rmdir(test_dir_path)
        self.assertFalse(os.path.exists(test_dir_path))

    def test_relative_file(self):
        # Test accessing a relative file path
        test_file_path = LocationManager.relative_file('testfile.txt')
        self.assertEqual(test_file_path, os.path.join(self.test_root_dir, 'testfile.txt'))

if __name__ == '__main__':
    TestLocationManager.execute_all()
