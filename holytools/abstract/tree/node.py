from __future__ import annotations

from dataclasses import dataclass
from typing import Callable, Optional

# -------------------------------------------


tree_str = """a
    b
        a
        c
            b
            b2
    c
        a3"""


@dataclass
class TreeNode:
    name : str

    def __post_init__(self):
        self.children : list[TreeNode] = []

    def make_copy(self) -> TreeNode:
        new = TreeNode(name=self.name)
        new.children = self.children
        return new

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

    def make_pruned[T](self : T | TreeNode, is_relevant : Callable[[TreeNode], bool]) -> list[T]:
        pruned_children = []
        for c in self.children:
            pruned_children += c.make_pruned(is_relevant=is_relevant)

        if is_relevant(self):
            new = self.make_copy()
            new.children = pruned_children
            return [new]
        else:
            return pruned_children

    def distribute_unique(self, node_map : dict[str, TreeNode], parent : Optional[TreeNode] = None):
        if not self.name in node_map:
            new = TreeNode(name=self.name)
            node_map[self.name] = new
            if parent:
                node_map[parent.name].children.append(new)

        for c in self.children:
            c.distribute_unique(node_map=node_map, parent=node_map[self.name])

    # -----------------------------------------------------
    # Properties

    def get_fullname(self) -> str:
        return self.name

    def get_descendants(self):
        desc : list[TreeNode] = [x for x in self.children]
        for c in self.children:
            desc += c.get_descendants()
        return desc

    def get_tree(self, indent : int   = 0):
        tree = '|\t' * indent +  self.get_fullname()
        for c in self.children:
            tree += f'\n{c.get_tree(indent=indent+1)}'
        return tree



if __name__ == "__main__":
    nm = {}
    example_node = TreeNode.from_str(s=tree_str)
    example_node.distribute_unique(node_map=nm)
    print(nm[example_node.name].get_tree())