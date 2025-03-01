import os
import shutil
import tempfile

from holytools.devtools import Unittest
from holytools.fsys import FsysNode
from holytools.fsys.fsys_node import Directory


# -------------------------------------------------------------

class TestFsysNode(Unittest):
    num_hard_files = 9
    num_hard_folders = 3
    num_total_dat_files = 5
    num_total_files = num_hard_files+1
    num_total_nodes= num_total_files+num_hard_folders

    @classmethod
    def setUpClass(cls):
        pass

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.files = ['file1.txt', 'file2.txt']
        self.subdirs = ['.hiddendir','dir1', 'dir2']
        self.subfiles = {'dir1': ['sub1.dat', 'sub2.dat', 'sub3.dat', '.hiddenfile.dat'],
                         'dir2': ['sub1.png', 'sub2.png', 'sub3.png']}

        for the_file in self.files:
            open(os.path.join(self.test_dir, the_file), 'a').close()  # Create empty files

        for subdir, subfiles in self.subfiles.items():
            subdir_path = os.path.join(self.test_dir, subdir)
            os.makedirs(subdir_path)
            for subfile in subfiles:
                open(os.path.join(subdir_path, subfile), 'a').close()

        os.symlink(os.path.join(self.test_dir, 'dir1', 'sub1.dat'), os.path.join(self.test_dir, 'symlink_sub1.dat'))
        self.root_node = Directory(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_file_fpaths(self):
        subfile_paths = self.root_node.get_subfile_fpaths()
        self.assertEqual(len(subfile_paths), self.num_total_files)

    def test_zip(self):
        zip_bytes = self.root_node.get_zip()
        self.assertTrue(len(zip_bytes) > 0)
        self.assertIsInstance(zip_bytes, bytes)


if __name__ == '__main__':
    TestFsysNode.execute_all()