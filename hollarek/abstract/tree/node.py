from __future__ import annotations
from typing import Optional
# -------------------------------------------

class TreeNode:
    def __init__(self, name : str, parent : Optional[TreeNode] = None):
        self._name : str = name
        self._parent : TreeNode = parent
        self._children : Optional[list] = None

    def _add_child(self, node : TreeNode):
        if node.get_parent() != self:
            raise ValueError(f'Node already has parent')
        if self._children is None:
            self._children = []
        self._children.append(node)

    def get_name(self) -> str:
        return self._name

    # -------------------------------------------
    # descendants

    def get_subnodes(self) -> list[TreeNode]:
        subnodes = []
        for child in self.get_child_nodes():
            subnodes.append(child)
            subnodes += child.get_subnodes()
        return subnodes

    def get_child_nodes(self) -> list[TreeNode]:
        return self._children

    def get_tree(self, max_child_size : int = 100) -> Tree:
        return Tree(root_node=self)
        # sub_dict = self.get_dict()[self._name]
        # for key, value in [(key,value) for (key, value) in sub_dict.items() if isinstance(value, dict)]:
        #     elem_count = get_total_elements(recursive_dict=value)
        #     if elem_count > max_child_size:
        #         sub_dict[key] = f': {key} exceeds limit of {max_child_size} elements contains {elem_count} files/folders'
        #
        # tree = get_pretty_tree(the_dict={self._name : sub_dict})
        # tree = tree.replace('{}', '')
        # return tree

    # -------------------------------------------
    # ancestors

    def get_ancestors(self) -> list[TreeNode]:
        current = self
        ancestors = []
        while current._parent:
            ancestors.append(current._parent)
            current = current._parent
        return ancestors

    def get_parent(self) -> Optional[TreeNode]:
        return self._parent

    def get_root(self) -> TreeNode:
        current = self
        while current.get_parent():
            current = current.get_parent()
        return current


class Tree:
    def __init__(self, root_node : TreeNode):
        def get_subtree_dict(node : TreeNode):
            the_dict = {node.get_name() : {}}
            for child in node.get_child_nodes():
                the_dict[node.get_name()].update(get_subtree_dict(child))
            return the_dict

        self.recursive_dict = get_subtree_dict(node=root_node)

    def as_str(self) -> str:
        return nested_dict_as_str(the_dict=self.recursive_dict)


def nested_dict_as_str(the_dict: dict, prefix=''):
    output = ''
    for index, (key, value) in enumerate(the_dict.items()):
        is_last = index == len(the_dict) - 1
        new_prefix = prefix + ('    ' if is_last else '│   ')
        connector = '└── ' if is_last else '├── '
        output += f'{prefix}{connector}{key}\n'
        output += nested_dict_as_str(the_dict=value, prefix = new_prefix)
    return output