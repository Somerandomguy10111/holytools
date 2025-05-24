import json
import os
import tempfile

from holytools.devtools import Unittest
from holytools.fileIO import BinaryFile, ExampleFiles
from holytools.fsys.node import Directory, File, FsysNode


# -------------------------------------------------------------

class FsysTest(Unittest):
    num_hard_files = 9
    num_hard_folders = 3
    num_total_dat_files = 5
    num_total_files = num_hard_files+1
    num_total_nodes= num_total_files+num_hard_folders

    def setUp(self):
        self.root_dirpath = tempfile.mkdtemp()
        self.files = ['file1.txt', 'file2.txt']
        self.subdirs = ['.hiddendir','dir1', 'dir2']
        self.subfiles = {'dir1': ['sub1.dat', 'sub2.dat', 'sub3.dat', '.hiddenfile.dat'],
                         'dir2': ['sub1.png', 'sub2.png', 'sub3.png']}

        for d in self.subdirs:
            os.makedirs(os.path.join(self.root_dirpath, d))

        for the_file in self.files:
            open(os.path.join(self.root_dirpath, the_file), 'a').close()  # Create empty files

        for subdir, subfiles in self.subfiles.items():
            subdir_path = os.path.join(self.root_dirpath, subdir)
            for subfile in subfiles:
                open(os.path.join(subdir_path, subfile), 'a').close()

        os.symlink(os.path.join(self.root_dirpath, 'dir1', 'sub1.dat'), os.path.join(self.root_dirpath, 'symlink_sub1.dat'))
        self.root_node = Directory(path=self.root_dirpath)


class TestNode(FsysTest):
    def test_get_subnodes(self):
        subfile_paths = self.root_node.get_subfile_fpaths()
        self.assertEqual(len(subfile_paths), self.num_total_files)

        subnode_paths = self.root_node.get_all_subpaths()
        self.assertEqual(len(subnode_paths), self.num_total_nodes)
        print(f'- Subnode paths')
        for n in subnode_paths:
            print(n)

    def test_dir_properties(self):
        self.assertTrue(self.root_node.get_name() == os.path.basename(self.root_dirpath))
        self.assertTrue(isinstance(self.root_node.get_last_modified_epochtime(), float))

    def test_file(self):
        dat_fpath = os.path.join(self.root_dirpath, 'dir1', 'sub1.dat')
        file = File(path=dat_fpath)
        self.assertTrue(file.get_suffix() == 'dat')

    def test_hidden(self):
        self.assertTrue(self.root_node.is_hidden() == False)
        hidden_dir = Directory(path=os.path.join(self.root_dirpath, '.hiddendir'))
        self.assertTrue(hidden_dir.is_hidden() == True)

    def test_zip(self):
        zip_bytes = self.root_node.get_zip()
        self.assertTrue(len(zip_bytes) > 0)
        self.assertIsInstance(zip_bytes, bytes)

    def test_get_tree(self):
        tree = self.root_node.get_tree()
        expected_expression = f'{os.path.basename(self.root_dirpath)}/'
        print(f'- Root Tree:\n{tree}')

        self.assertTrue(f'🗎 sub3.png' in tree)
        self.assertTrue(f'🗀 dir2/' in tree)
        self.assertTrue(expected_expression in tree)

    def test_binary_size(self):
        text_fpath = ExampleFiles.lend_txt().fpath
        png_fpath = ExampleFiles.lend_png().fpath

        bio = BinaryFile(text_fpath)

        bytes_count_mb = len(bio.read())/10**6
        fsize= FsysNode(path=png_fpath).get_size_in_MB()
        lower = int(fsize)
        upper = int(fsize+1)
        self.assertTrue(lower <= bytes_count_mb <= upper)

if __name__ == '__main__':
    TestNode.execute_all()