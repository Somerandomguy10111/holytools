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
    # Tree manipulation

    def create_pruned_subtree[T](self : T | TreeNode, is_relevant : Callable[[T | TreeNode], bool]) -> list[T]:
        pruned_children = []
        for c in self.children:
            pruned_children += c.create_pruned_subtree(is_relevant=is_relevant)

        if is_relevant(self):
            new = self.mk_empty_copy()
            new.children = pruned_children
            return [new]
        else:
            return pruned_children

    def create_unique_subtree(self, node_map : Optional[dict[str, TreeNode]] = None, parent : Optional[TreeNode] = None) -> TreeNode:
        if node_map is None:
            node_map = {}
        uid = self.get_id()
        if not uid in node_map:
            new = self.mk_empty_copy()
            node_map[uid] = new
            if parent:
                node_map[parent.get_id()].children.append(new)

        for c in self.children:
            c.create_unique_subtree(node_map=node_map, parent=node_map[uid])

        return node_map[uid]

    def get_id(self) -> str:
        return self.name

    def mk_empty_copy(self) -> TreeNode:
        new = TreeNode(name=self.name)
        new.children = []
        return new

    # ------------------------------------------------
    # Navigation

    def get_node_to_idx(self) -> dict[str, int]:
        idx_to_node = self.get_idx_to_node()
        return {node.get_id() : j for j, node in idx_to_node.items()}

    def get_idx_to_node[T](self : T | TreeNode) -> dict[int, T]:
        all_nodes = [self] + self.get_descendants()
        all_nodes = [x for x in all_nodes if x.is_indexable()]

        return {j : node for j, node in enumerate(all_nodes)}

    def is_indexable(self) -> bool:
        _ = self
        return True

    def get_descendants[T](self : T | TreeNode) -> list[T]:
        desc : list[TreeNode] = [x for x in self.children]
        for c in self.children:
            desc += c.get_descendants()
        return desc

    # -----------------------------------------------------
    # Properties

    def get_tree(self, indent : int   = 0, node_to_idx : Optional[dict[str, int]] = None):
        idx = node_to_idx.get(self.get_id()) if not node_to_idx is None else None
        conditional_idx = f' | ID = {idx}' if not idx is None else ''
        indentation = '\t' * indent

        tree = (f'{indentation}{self.get_fullname()}{conditional_idx}'
                f'{self.get_desc()}')
        for c in self.children:
            tree += f'\n{c.get_tree(indent=indent+1, node_to_idx=node_to_idx)}'
        return tree

    def get_desc(self) -> str:
        _ = self
        return ''

    def get_fullname(self) -> str:
        return self.name

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
    unique_node = example_node.create_unique_subtree()
    print(unique_node.get_tree())
    example_idx_to_node = unique_node.get_node_to_idx()
    print(unique_node.get_tree(node_to_idx=example_idx_to_node))
