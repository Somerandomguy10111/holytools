from dataclasses import dataclass
import pyautogui
from screeninfo import Monitor
import time
from hollarek.hardware.display import get_primary_monitor, get_secondary_monitor


@dataclass
class Grid:
    x_length: int
    y_length: int

    @classmethod
    def create_display_grid(cls, monitor : Monitor = get_primary_monitor(), small_dim : int = 100):
        scale_factor = small_dim / min(monitor.width, monitor.height)
        x_length = int(monitor.width * scale_factor)
        y_length = int(monitor.height * scale_factor)

        return cls(x_length=x_length, y_length=y_length)

    def __str__(self):
        return f"Grid(x_length={self.x_length}, y_length={self.y_length})"

@dataclass
class LatticePoint:
    x: int
    y: int


class Clicker:
    def __init__(self, natural_grid: Grid = Grid.create_display_grid()):
        self.natural_grid = natural_grid

    def click(self, lattice_point: LatticePoint, monitor : Monitor= get_primary_monitor()):
        pixel_x = round(lattice_point.x * monitor.width / self.natural_grid.x_length)
        pixel_y = round(lattice_point.y * monitor.height / self.natural_grid.y_length)

        if 0 <= pixel_x < monitor.width and 0 <= pixel_y < monitor.height:
            pyautogui.click(monitor.x + pixel_x, monitor.y + pixel_y)
        else:
            raise ValueError("Lattice point translates to a position outside the monitor boundaries")


    def get_gridded_screenshot(self):
        pass


my_grid = Grid(x_length=10, y_length=5)
my_point = LatticePoint(x=3, y=1)

print(my_grid)
print(my_point)

from hollarek.hardware.display.display import get_primary_monitor
print(Grid.create_display_grid(monitor=get_secondary_monitor()))