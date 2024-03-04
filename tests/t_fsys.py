from hollarek.fsys import FsysNode
from hollarek.devtools import Unittest
import tempfile
import os
import shutil

class TestFsysNode(Unittest):
    num_hard_files = 8
    num_hard_folders = 2
    num_total_dat_files = 4
    num_total_files = num_hard_files+1
    num_total_nodes= num_total_files+num_hard_folders

    @classmethod
    def setup(cls):
        pass

    def setUp(self):
        self.test_dir = tempfile.mkdtemp()
        self.files = ['file1.txt', 'file2.txt']
        self.subdirs = ['dir1', 'dir2']
        self.subfiles = {'dir1': ['sub1.dat', 'sub2.dat', 'sub3.dat'],
                         'dir2': ['sub1png', 'sub2png', 'sub3png']}

        for the_file in self.files:
            open(os.path.join(self.test_dir, the_file), 'a').close()  # Create empty files

        for subdir, subfiles in self.subfiles.items():
            subdir_path = os.path.join(self.test_dir, subdir)
            os.makedirs(subdir_path)
            for subfile in subfiles:
                open(os.path.join(subdir_path, subfile), 'a').close()

        os.symlink(os.path.join(self.test_dir, 'dir1', 'sub1.dat'), os.path.join(self.test_dir, 'symlink_sub1.dat'))

        self.root_node = FsysNode(self.test_dir)

    def tearDown(self):
        shutil.rmtree(self.test_dir)

    def test_get_subnodes(self):
        subnodes = self.root_node.get_subnodes()
        self.assertEqual(len(subnodes), self.num_total_nodes)

    def test_select_dat_files(self):
        dat_nodes = self.root_node.get_file_subnodes(['.dat'])
        self.assertEqual(len(dat_nodes), self.num_total_dat_files)

    def test_get_file_subnodes(self):
        file_subnodes = self.root_node.get_file_subnodes()
        self.assertEqual(len(file_subnodes), self.num_total_files)

    def test_get_dict(self):
        the_dict = self.root_node.get_dict()
        self.assertIsInstance(the_dict, dict)

    def test_get_yaml(self):
        the_yaml = self.root_node.get_tree()
        self.assertIsInstance(the_yaml, str)

# This allows the test script to be run from the command line
if __name__ == '__main__':
    # TestFsysNode.execute_all(show_run_times=True)
    dir_path = '/home/daniel/OneDrive/Downloads'
    # download_node = FsysNode(path=os.path.join(dir_path, 'cute_doggo.png'))
    download_node = FsysNode(path=dir_path)
    download_bytes = download_node.get_zip()

    zip_path = os.path.join(dir_path, 'test.zip')
    with open(f'{zip_path}', 'wb') as file:
        file.write(download_bytes)
