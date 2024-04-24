from hollarek.fsys.fsys_node import FsysNode, FsysTree
from hollarek.abstract import Tree
from hollarek.devtools import Unittest
import shutil
import os
import tempfile

from tests.t_fsys.t_save_manager import TestSaveManager


class FsysTemplate(Unittest):
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
        self.root_node = FsysNode(self.test_dir)


class TestFsyNode(FsysTemplate):
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

    def test_exclude_hidden(self):
        non_hidden = self.root_node.get_child_nodes(exclude_hidden=True)
        print(f'Non hidden node are {[node.get_name() for node in non_hidden]}')
        self.assertEqual(len(non_hidden), 5)


class TestTree(FsysTemplate):
    def test_tree_ok(self):
        the_tree = self.root_node.get_tree()
        self.assertIsInstance(the_tree, FsysTree)

    def test_tree_as_str(self):
        the_tree = self.root_node.get_tree()
        tree_str = the_tree.as_str()
        self.assertIsInstance(tree_str, str)
        print(f'Tree as string is \n{tree_str}')
        self.assertIn(f'.dat', tree_str)

    def test_tree_len(self):
        the_tree = self.root_node.get_tree()
        self.assertEqual(the_tree.get_size(), self.num_total_nodes)
        print(f'Tree size is {the_tree.get_size()}')

    def test_max_depth(self):
        self.root_node.get_tree(max_depth=2)
        with self.assertRaises(ValueError):
            self.root_node.get_tree(max_depth=1)

    def test_max_size(self):
        self.root_node.get_tree(max_size=self.num_total_nodes)
        with self.assertRaises(ValueError):
            self.root_node.get_tree(max_size=self.num_total_nodes-1)


if __name__ == '__main__':
    # TestFsysNode.execute_all()
    TestTree.execute_all()
    TestSaveManager.execute_all()