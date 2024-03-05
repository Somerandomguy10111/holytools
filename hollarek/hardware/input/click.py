from dataclasses import dataclass
import pyautogui
from hollarek.hardware.display import Display


@dataclass
class Grid:
    x_length: int
    y_length: int

    @classmethod
    def create_display_grid(cls, display : Display = Display.get_primary(), small_dim : int = 100):
        scale_factor = small_dim / min(display.width, display.height)
        x_length = int(display.width * scale_factor)
        y_length = int(display.height * scale_factor)

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

    def click(self, lattice_point: LatticePoint, display : Display = Display.get_primary()):
        pixel_x = round(lattice_point.x * display.width / self.natural_grid.x_length)
        pixel_y = round(lattice_point.y * display.height / self.natural_grid.y_length)

        if 0 <= pixel_x < display.width and 0 <= pixel_y < display.height:
            pyautogui.click(display.x + pixel_x, display.y + pixel_y)
        else:
            raise ValueError("Lattice point translates to a position outside the display boundaries")


    def get_gridded_screenshot(self):
        pass


my_grid = Grid(x_length=10, y_length=5)
my_point = LatticePoint(x=3, y=1)

print(my_grid)
print(my_point)