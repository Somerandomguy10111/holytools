import os
import tempfile

from holytools.devtools import Unittest
from holytools.fsys.fsys_node import Directory, File


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

        for d in self.subdirs:
            os.makedirs(os.path.join(self.test_dir, d))

        for the_file in self.files:
            open(os.path.join(self.test_dir, the_file), 'a').close()  # Create empty files

        for subdir, subfiles in self.subfiles.items():
            subdir_path = os.path.join(self.test_dir, subdir)
            for subfile in subfiles:
                open(os.path.join(subdir_path, subfile), 'a').close()

        os.symlink(os.path.join(self.test_dir, 'dir1', 'sub1.dat'), os.path.join(self.test_dir, 'symlink_sub1.dat'))
        self.root_node = Directory(path=self.test_dir)

    def test_get_tree(self):
        tree = self.root_node.get_tree()

        expected_expression = f'{os.path.basename(self.test_dir)}/ -> tmp/'
        print(f'- Expected expression: {expected_expression}')
        print(f'- Tree:\n{tree}')
        self.assertTrue(expected_expression in tree)


    def test_get_subnodes(self):
        subfile_paths = self.root_node.get_subfile_fpaths()
        self.assertEqual(len(subfile_paths), self.num_total_files)

        subnode_paths = self.root_node.get_all_subpaths()
        self.assertEqual(len(subnode_paths), self.num_total_nodes)

    def test_dir_properties(self):
        self.assertTrue(self.root_node.get_name() == os.path.basename(self.test_dir))
        self.assertTrue(isinstance(self.root_node.get_last_modified_epochtime(), float))

    def test_file(self):
        dat_fpath = os.path.join(self.test_dir, 'dir1', 'sub1.dat')
        file = File(path=dat_fpath)
        self.assertTrue(file.get_suffix() == 'dat')

    def test_hidden(self):
        self.assertTrue(self.root_node.is_hidden() == False)
        hidden_dir = Directory(path=os.path.join(self.test_dir, '.hiddendir'))
        self.assertTrue(hidden_dir.is_hidden() == True)

    def test_zip(self):
        zip_bytes = self.root_node.get_zip()
        self.assertTrue(len(zip_bytes) > 0)
        self.assertIsInstance(zip_bytes, bytes)


if __name__ == '__main__':
    TestFsysNode.execute_all()