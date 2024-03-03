from __future__ import annotations
from typing import Optional
import yaml
# -------------------------------------------

from typing import TypeVar
TreeNodeType = TypeVar('TreeNodeType', bound='TreeNode')

class TreeNode:
    def __init__(self, name : str, parent : Optional[TreeNodeType] = None):
        self._name : str = name
        self._parent : TreeNodeType = parent
        self._children : Optional[list[TreeNodeType]] = None

    def _add_child(self, node : TreeNodeType):
        if node.get_parent() != self:
            raise ValueError(f'Node already has parent')
        self._children.append(node)

    def get_name(self) -> str:
        return self._name

    # -------------------------------------------
    # descendants

    def get_subnodes(self) -> list[TreeNodeType]:
        subnodes = []
        for child in self.get_child_nodes():
            subnodes.append(child)
            subnodes += child.get_subnodes()
        return subnodes

    def get_child_nodes(self) -> list[TreeNodeType]:
        return self._children

    def get_tree(self, pretty : bool = True) -> str:
        if pretty:
            tree = get_pretty_tree(the_dict=self.get_dict())
            to_replace = f'{{}}'
        else:
            tree = yaml.dump(data=self.get_dict(), indent=4)
            to_replace = f': {{}}'
        tree = tree.replace(f'{to_replace}', '')
        return tree

    def get_dict(self) -> Optional[dict]:
        the_dict = {self._name: {}}
        for child in self.get_child_nodes():
            the_dict[self._name].update(child.get_dict())
        return the_dict

    # -------------------------------------------
    # ancestors

    def get_ancestors(self) -> list[TreeNodeType]:
        current = self
        ancestors = []
        while current._parent:
            ancestors.append(current._parent)
            current = current._parent
        return ancestors

    def get_parent(self) -> Optional[TreeNodeType]:
        return self._parent

    def get_root(self) -> TreeNodeType:
        current = self
        while current.get_parent():
            current = current.get_parent()
        return current


def get_pretty_tree(the_dict, prefix='', is_last=True) -> str:
    output = ''
    for index, (key, value) in enumerate(the_dict.items()):
        connector = '└── ' if is_last else '├── '
        new_prefix = prefix + ('    ' if is_last else '│   ')

        if isinstance(value, dict) and value:
            output = f'{prefix}{connector}{key}\n'
            last_child = len(value) - 1
            for sub_index, (sub_key, sub_value) in enumerate(value.items()):
                sub_is_last = sub_index == last_child
                output += get_pretty_tree({sub_key: sub_value}, new_prefix, sub_is_last)
        else:
            output += f'{prefix}{connector}{key} {value}\n'
    return output