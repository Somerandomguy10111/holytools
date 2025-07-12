from holytools.abstract.tree.node import Node
from holytools.devtools import Unittest

class TestNodeMerge(Unittest):
    def test_merge(self):
        t1 = Node.from_str("""
        d
            b
                a1
                a2
                    a21
        """)
        t2 = Node.from_str("""
        d
            b
                a2
                    a22
            c
                a3
        """)
        Node.merge(t1, t2)

        # After merge, t1 should have structure:
        # d
        # ├── b
        # │   ├── a1
        # │   └── a2
        # │       ├── a21
        # │       └── a22
        # └── c
        #     └── a3

        self.assertEqual(t1.name, "d")
        self.assertEqual(sorted(child.name for child in t1.children), ["b", "c"])
        b = next(child for child in t1.children if child.name == "b")
        c = next(child for child in t1.children if child.name == "c")
        self.assertEqual(sorted(child.name for child in b.children), ["a1", "a2"])
        a2 = next(child for child in b.children if child.name == "a2")
        self.assertEqual(sorted(child.name for child in a2.children), ["a21", "a22"])
        self.assertEqual(c.children[0].name, "a3")
