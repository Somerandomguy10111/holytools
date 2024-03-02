from __future__ import annotations
from typing import Optional
# -------------------------------------------


class TreeNode:
    def __init__(self, name : str, parent : Optional[TreeNode] = None):
        self._name : str = name if parent else '/'
        self._parent : TreeNode = parent
        self._children : set[TreeNode] = set()

    def remove_child(self, node : TreeNode):
        self._children.remove(node)


    def _add_child(self, node : TreeNode):
        if node.get_parent() != self:
            raise ValueError(f'Node already has parent')
        self._children.add(node)

    # -------------------------------------------
    # get

    def get_name(self) -> str:
        return self._name


    def get_tree(self) -> dict:
        tree = {}
        for child in self._children:
            tree[child] = child.get_tree()
        return tree


    def get_children(self) -> list[TreeNode]:
        return list(self._children)


    def get_root(self) -> TreeNode:
        current = self
        while current._parent:
            current = current._parent
        return current

    def get_parent(self) -> Optional[TreeNode]:
        return self._parent


