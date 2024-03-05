import pyautogui
from hollarek.hardware.display import Display
from hollarek.hardware.display.display import Grid, LatticePoint


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