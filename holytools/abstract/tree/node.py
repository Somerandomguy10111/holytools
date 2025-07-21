from __future__ import annotations

import copy
from dataclasses import dataclass
from typing import Callable, Optional, Any, Self

# -------------------------------------------

@dataclass
class TreeNode:
    name : str

    def __post_init__(self):
        self.children : list[TreeNode | Any] = []

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

            node = TreeNode(name=sl)
            parent = ancestors[-1]
            parent.children.append(node)
            ancestors.append(node)

        return root

    # -------------------------------------------
    # Tree manipulation

    def create_pruned(self, is_relevant : Callable[[Self], bool]) -> Optional[Self]:
        new_children = [c.create_pruned(is_relevant=is_relevant) for c in self.children]
        new_children = [c for c in new_children if not c is None]
        is_included = is_relevant(self) or len(new_children) > 0

        new = self.mk_empty_copy() if is_included else None
        if new:
            new.children = new_children
        return new

    def create_unique(self, node_map : Optional[dict[str, TreeNode]] = None, parent : Optional[TreeNode] = None) -> TreeNode:
        if node_map is None:
            node_map = {}

        uid = self.get_id()
        if not uid in node_map:
            new = self.mk_empty_copy()
            node_map[uid] = new
            if parent:
                node_map[parent.get_id()].children.append(new)

        for c in self.children:
            c.create_unique(node_map=node_map, parent=node_map[uid])
        return node_map[uid]

    def mk_empty_copy(self) -> TreeNode:
        new = copy.deepcopy(self)
        new.children = []

        return new

    # ------------------------------------------------
    # Navigation

    def get_nodeid_to_idx(self) -> dict[str, int]:
        idx_to_node = self.get_idx_to_node()
        return {node.get_id() : j for j, node in idx_to_node.items()}

    def get_idx_to_node(self) -> dict[int, Self]:
        all_nodes = [self] + self.get_descendants()
        all_nodes = [x for x in all_nodes if x.is_indexable()]

        return {j : node for j, node in enumerate(all_nodes)}

    def get_id(self) -> str:
        return self.name

    def is_indexable(self) -> bool:
        _ = self
        return True

    def get_descendants[T](self : T | TreeNode) -> list[T]:
        descendants : list[TreeNode] = []
        for c in self.children:
            descendants.append(c)
            descendants += c.get_descendants()
        return descendants

    # -----------------------------------------------------
    # Properties

    def get_tree(self, indent : int   = 0, nodeid_to_idx : Optional[dict[str, int]] = None):
        idx = nodeid_to_idx.get(self.get_id()) if not nodeid_to_idx is None else None
        desc = self.get_desc()

        marked_indent = '|\t' * indent
        conditional_idx = f' | ID = {idx}' if not idx is None else ''
        conditional_desc = f'\n{marked_indent}{desc}' if desc else ''

        tree = (f'{marked_indent}{self.get_fullname()}{conditional_idx}'
                f'{conditional_desc}')

        for c in self.children:
            tree += f'\n{c.get_tree(indent=indent+1, nodeid_to_idx=nodeid_to_idx)}'
        return tree

    def get_desc(self) -> str:
        _ = self
        return ''

    def get_fullname(self) -> str:
        return self.name
