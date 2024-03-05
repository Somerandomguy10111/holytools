from __future__ import annotations

import psutil
from hollarek.templates import Singleton
# -------------------------------------------


class RAM(Singleton):
    def __init__(self, include_swap : bool = False):
        if self.get_is_initialized():
            return

        self.include_swap = include_swap
        super().__init__()


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