from __future__ import annotations
import psutil
from typing import Optional

# -------------------------------------------


class RAM:
    _instance : Optional[RAM] = None
    _is_intialized : bool = False

    def __new__(cls, *args, **kwargs):
        if not RAM._instance:
            RAM._instance = super().__new__(cls)
        return RAM._instance

    def __init__(self, include_swap : bool = False):
        if RAM._is_intialized:
            return

        self.include_swap = include_swap


    def get_available_in_GB(self) -> float:
        available_memory = psutil.virtual_memory().available / (1024 ** 3)
        if self.include_swap:
            swap_memory = psutil.swap_memory().free / (1024 ** 3)
            available_memory += swap_memory
        return available_memory


    def get_total_in_GB(self) -> float:
        total_memory = psutil.virtual_memory().total / (1024 ** 3)
        if self.include_swap:
            swap_memory = psutil.swap_memory().total / (1024 ** 3)
            total_memory += swap_memory

        return total_memory


if __name__ == '__main__':
    total = RAM().get_total_in_GB()