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

    def __add__(self, other : LatticePoint):
        if isinstance(other, LatticePoint):
            return LatticePoint(self.x + other.x, self.y + other.y)
        else:
            raise TypeError("Can only add LatticePoint to another LatticePoint")

    def __sub__(self, other : LatticePoint):
        if isinstance(other, LatticePoint):
            return LatticePoint(self.x - other.x, self.y - other.y)
        else:
            raise TypeError("Can only subtract LatticePoint from another LatticePoint")


if __name__ == "__main__":
    point1 = LatticePoint(3, 5)
    point2 = LatticePoint(1, 2)
    point3 = point1 + point2  # This will be LatticePoint(x=4, y=7)
    point4 = point1 - point2  # This will be LatticePoint(x=2, y=3)

    print(point4, point3)
