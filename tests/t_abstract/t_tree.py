from holytools.abstract import TreeNode
from holytools.devtools import Unittest

class TestTreeNode(Unittest):
    def setUp(self):
        self.tree_str = """root
    child1
        grandchild1
        grandchild2
        child2
    child2"""

    def test_from_str(self):
        tree = TreeNode.from_str(self.tree_str)
        self.assertEqual(tree.name, "root")
        self.assertEqual(len(tree.children), 2)
        self.assertEqual(tree.children[0].name, "child1")
        self.assertEqual(len(tree.children[0].children), 3)
        self.assertEqual(tree.children[1].name, "child2")

    def test_create_pruned(self):
        def is_relevant_fn(node):
            return node.name == 'child2' or node.name == 'grandchild2'

        root = TreeNode.from_str(self.tree_str)
        pruned = root.create_pruned(is_relevant_fn)

        tree = pruned.get_tree()
        print(f'-Pruned subtree: {tree}')
        self.assertEqual(pruned.name, "root")
        self.assertIn('|	|	grandchild2', tree)
        self.assertIn('|	child2', tree)
        self.assertNotIn('grandchild1', tree)

    def test_create_unique(self):
        root = TreeNode.from_str(self.tree_str)
        unique_tree = root.create_unique()
        print(f'-Unique tree: {unique_tree.get_tree()}')

    def test_enumerated_tree(self):
        root = TreeNode.from_str(self.tree_str)
        nodeid_to_idx = root.get_nodeid_to_idx()

        tree = root.get_tree(nodeid_to_idx=nodeid_to_idx)
        print(f'-Enumerated tree: {tree}')
        self.assertIn('|	|	grandchild2 | ID = 3', tree)

if __name__ == "__main__":
    TestTreeNode.execute_all()