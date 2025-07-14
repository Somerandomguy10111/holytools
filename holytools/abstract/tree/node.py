from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

# -------------------------------------------

@dataclass
class TreeNode:
    name : str

    def __post_init__(self):
        self.children : list[TreeNode] = []

    @classmethod
    def from_str(cls, s : str) -> TreeNode:
        lines = s.split('\n')

        root = TreeNode(name=lines[0])
        ancestors : list[TreeNode] = [root]

        for l in lines[1:]:
            sl = l.lstrip(' ')
            blank_lines = len(l) - len(sl)
            if not blank_lines % 4 == 0:
                raise ValueError(f'Invalid indentation in line: {l}. Must be multiple of 4')

            indent = blank_lines // 4
            if indent > len(ancestors):
                raise ValueError(f'Invalid indentation in line: {l}')

            while indent < len(ancestors):
                ancestors.pop()

            parent = ancestors[-1]
            node = TreeNode(name=sl)
            parent.children.append(node)
            ancestors.append(node)

        return root

    # -------------------------------------------
    # Updates

    def make_pruned[T](self : T | TreeNode, is_relevant : Callable[[TreeNode], bool]) -> list[T]:
        pruned_children = []
        for c in self.children:
            pruned_children += c.make_pruned(is_relevant=is_relevant)

        if is_relevant(self):
            new = self.make_empty_copy()
            new.children = pruned_children
            return [new]
        else:
            return pruned_children

    def make_unique(self, node_map : Optional[dict[str, TreeNode]] = None, parent : Optional[TreeNode] = None):
        if node_map is None:
            node_map = {}
        if not self.name in node_map:
            new = self.make_empty_copy()
            node_map[self.name] = new
            if parent:
                node_map[parent.name].children.append(new)

        for c in self.children:
            c.make_unique(node_map=node_map, parent=node_map[self.name])

        return node_map[self.name]

    def make_empty_copy(self) -> TreeNode:
        new = TreeNode(name=self.name)
        new.children = []
        return new

    # -----------------------------------------------------
    # Properties

    def get_tree(self, indent : int   = 0):
        tree = '|\t' * indent +  self.get_fullname()
        for c in self.children:
            tree += f'\n{c.get_tree(indent=indent+1)}'
        return tree

    def get_fullname(self) -> str:
        return self.name

    def get_descendants(self):
        desc : list[TreeNode] = [x for x in self.children]
        for c in self.children:
            desc += c.get_descendants()
        return desc



if __name__ == "__main__":
    nm = {}
    tree_str = """a
        b
            a
            c
                b
                b2
        c
            a3"""

    example_node = TreeNode.from_str(s=tree_str)
    unique_node = example_node.make_unique()
    print(unique_node.get_tree())