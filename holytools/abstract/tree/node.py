from __future__ import annotations
from dataclasses import dataclass, field
from typing import Optional, Callable

from typing import Optional
from abc import abstractmethod, ABC

# -------------------------------------------


tree_str = """root
    a
        a
        a
        b
            c
    b
        a
            a
        a
        d"""


@dataclass
class Node:
    def __init__(self, name : str):
        self.name : str = name
        self.children : list[Node] = []

    def get_descendants(self):
        desc : list[Node] = [x for x in self.children]
        for c in self.children:
            desc += c.get_descendants()
        return desc

    @classmethod
    def from_str(cls, s : str) -> Node:
        lines = s.split('\n')

        root = Node(name=lines[0])
        ancestors : list[Node] = [root]

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

            node = Node(name=sl)
            parent = ancestors[-1]
            parent.children.append(node)
            ancestors.append(node)

        return root

    def get_tree(self, indent : int   = 0):
        tree = '|\t' * indent +  self.name
        for c in self.children:
            tree += f'\n{c.get_tree(indent=indent+1)}'
        return tree


example_node = Node.from_str(s=tree_str)
print(example_node.get_tree())
