from __future__ import annotations
from typing import Optional
from abc import abstractmethod
# -------------------------------------------


class TreeNode:
    def __init__(self, name : str, parent : Optional[TreeNode] = None):
        self._name : str = name if parent else '/'
        self._parent : TreeNode = parent
        self._children : Optional[set[TreeNode]] = set()

    def remove_child(self, node : TreeNode):
        self._children.remove(node)

    def _add_child(self, node : TreeNode):
        if node.get_parent() != self:
            raise ValueError(f'Node already has parent')
        self._children.add(node)

    @abstractmethod
    def _retrieve_children(self) -> set[TreeNode]:
        pass

    # -------------------------------------------
    # get

    def get_name(self) -> str:
        return self._name


    def get_ancestors(self) -> list[TreeNode]:
        current = self
        ancestors = []
        while current._parent:
            ancestors.append(current._parent)
            current = current._parent
        return ancestors


    def get_child_nodes(self) -> set[TreeNode]:
        if self._children is None:
            self._children = self._retrieve_children()
        return self._children


    def get_dict(self) -> Optional[dict]:
        if not self.get_child_nodes():
            return None

        return {child.get_name() : child.get_dict() for child in self.get_child_nodes()}


    def get_root(self) -> TreeNode:
        current = self
        while current._parent:
            current = current._parent
        return current


    def get_parent(self) -> Optional[TreeNode]:
        return self._parent


