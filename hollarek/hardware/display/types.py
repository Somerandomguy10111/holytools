from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Grid:
    x_size : int
    y_size : int

    def is_in_bounds(self, lattice_point : LatticePoint) -> bool:
        return 0 <= lattice_point.x <= self.x_size and 0 <= lattice_point.y <= self.y_size


@dataclass
class LatticePoint:
    x: int
    y: int
