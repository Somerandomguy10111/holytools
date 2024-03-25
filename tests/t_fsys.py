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
    def setUpClass(cls):
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

    def test_get_yaml(self):
        the_yaml = self.root_node.get_tree()
        self.assertIsInstance(the_yaml, str)


if __name__ == '__main__':
    dir_path = '/home/daniel/lotus'
    # node = FsysNode(path=dir_path)
    # children = node.get_child_nodes()
    # # print(f'children nodes are {children}')
    # # print(f'subnodes count is {len(node.get_subnodes())}')
    #
    # tree = node.get_tree(exclude_hidden=True)
    # # newtree = node.get_tree(max_size=100)
    # from hollarek.abstract import Tree
    # new_tree = Tree.join_trees(root=node, subtrees=[child.get_tree() for child in node.get_child_nodes()])
    # print(tree.as_str())
    # # assert(tree.as_str() == new_tree.as_str())
    #
    new_node = FsysNode(path='/home/daniel/lotus')
    children = new_node.get_child_nodes(exclude_hidden=False)
    for child in children:
        print(child)
    new_tree = new_node.get_tree(exclude_hidden=False)
    print(new_tree.as_str())