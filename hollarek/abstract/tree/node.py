from __future__ import annotations
from typing import Optional
from abc import abstractmethod, ABC
from hollarek.abstract.integer_inf import IntegerInf

# -------------------------------------------


class TreeNode(ABC):
    @abstractmethod
    def get_name(self) -> str:
        pass

    def get_tree(self, max_depth : int = IntegerInf(), max_size : int = IntegerInf()) -> dict:
        


        return Tree(root_node=self, max_depth=max_depth, max_size=max_size)

    # -------------------------------------------
    # descendants

    def get_subnodes(self) -> list[TreeNode]:
        subnodes = []
        for child in self.get_child_nodes():
            subnodes.append(child)
            subnodes += child.get_subnodes()
        return subnodes

    @abstractmethod
    def get_child_nodes(self) -> list[TreeNode]:
        pass

    # -------------------------------------------
    # ancestors

    def get_ancestors(self) -> list[TreeNode]:
        current = self
        ancestors = []
        while current.get_parent():
            ancestors.append(current.get_parent())
            current = current.get_parent()
        return ancestors

    @abstractmethod
    def get_parent(self) -> Optional[TreeNode]:
        pass

    def get_root(self) -> TreeNode:
        current = self
        while current.get_parent():
            current = current.get_parent()
        return current


class Tree:
    def __init__(self, root_node : TreeNode, max_depth : int = IntegerInf(), max_size : int = IntegerInf(), max_subtree_size = IntegerInf()):
        self.max_subtree_size = max_subtree_size
        self.max_depth = max_depth
        self.max_size = max_size
        self.current_size = 0
        self.recursive_dict = self.get_subtree_dict(node=root_node, depth=0)

    def as_str(self) -> str:
        return nested_dict_as_str(nested_dict=self.recursive_dict)

    def get_size(self) -> int:
        return get_total_elements(nested_dict=self.recursive_dict)

    def get_subtree_dict(self, node: TreeNode, depth: int):
        if depth > self.max_depth:
            raise ValueError(f'Exceeded max depth of {self.max_depth}')
        the_dict = {node.get_name(): {}}
        child_nodes = node.get_child_nodes()
        self.current_size += len(child_nodes)
        if self.current_size > self.max_size:
            raise ValueError(f'Exceeded max size of {self.max_size}')

        for child in child_nodes:
            try:
                subtree = Tree(root_node=child, max_depth=self.max_depth - 1, max_size=self.max_subtree_size)
                subtree_dict = subtree.recursive_dict
                the_dict[node.get_name()].update(subtree_dict)
            except:
                name_with_warning = f'{child.get_name()} [WARNING: Subtree too large to display]'
                the_dict[name_with_warning] = {}
        return the_dict


def nested_dict_as_str(nested_dict: dict, prefix='') -> str:
    output = ''
    for index, (key, value) in enumerate(nested_dict.items()):
        is_last = index == len(nested_dict) - 1
        new_prefix = prefix + ('    ' if is_last else '│   ')
        connector = '└── ' if is_last else '├── '
        output += f'{prefix}{connector}{key}\n'
        output += nested_dict_as_str(nested_dict=value, prefix = new_prefix)
    return output

def get_total_elements(nested_dict : dict) -> int:
    count = 0
    for key, value in nested_dict.items():
        count += 1
        if isinstance(value, dict):
            count += get_total_elements(value)
    return count