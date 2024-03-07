from __future__ import annotations

from dataclasses import dataclass
from hollarek.templates import Dillable


@dataclass
class Grid:
    x_size : int
    y_size : int

    def get_lattice_vectors(self) -> list[Vector]:
        return [lattice_point.to_vector() for lattice_point in self.get_lattice_points()]

    def get_lattice_points(self) -> list[LatticePoint]:
        return [LatticePoint(x, y) for x in range(self.x_size) for y in range(self.y_size)]

    def in_horizontal_bounds(self, x : int) -> bool:
        return 0 <= x <= self.x_size

    def is_in_vertical_bounds(self, y : int) -> bool:
        return 0 <= y <= self.y_size

    def is_in_bounds(self, point : LatticePoint) -> bool:
        return self.in_horizontal_bounds(point.x) and self.is_in_vertical_bounds(point.y)


@dataclass
class Vector:
    x : float
    y : float

    def __add__(self, other : Vector):
        return Vector(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        return Vector(self.x * other, self.y * other)

@dataclass
class LatticePoint:
    x: int
    y: int

    def to_vector(self) -> Vector:
        return Vector(x=self.x, y=self.y)

    def as_tuple(self) -> (int, int):
        return self.x, self.y

    def __mul__(self, other : float):
        return LatticePoint(int(self.x * other), int(self.y * other))

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

@dataclass
class Click(Dillable):
    point : LatticePoint
    display_index : int

if __name__ == "__main__":
    point1 = LatticePoint(3, 5)
    point2 = LatticePoint(1, 2)
    point3 = point1 + point2  # This will be LatticePoint(x=4, y=7)
    point4 = point1 - point2  # This will be LatticePoint(x=2, y=3)

    print(point4, point3)
