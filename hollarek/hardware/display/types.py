from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Grid:
    x_size : int
    y_size : int

    def in_horizontal_bounds(self, x : int) -> bool:
        return 0 <= x <= self.x_size

    def is_in_vertical_bounds(self, y : int) -> bool:
        return 0 <= y <= self.y_size

    def is_in_bounds(self, point : LatticePoint) -> bool:
        return self.in_horizontal_bounds(point.x) and self.is_in_vertical_bounds(point.y)


@dataclass
class LatticePoint:
    x: int
    y: int
