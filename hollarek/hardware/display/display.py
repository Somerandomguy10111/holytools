from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from PIL import Image, ImageDraw
from mss import mss
from screeninfo import get_monitors
from screeninfo import Monitor as BaseMonitor


class Display(BaseMonitor):
    @classmethod
    def get_primary(cls) -> Optional[Display]:
        for monitor in get_monitors():
            if monitor.is_primary:
                return cls.from_base(base_monitor=monitor)
        return None

    @classmethod
    def get_secondary(cls) -> Optional[Display]:
        for monitor in get_monitors():
            if not monitor.is_primary:
                return cls.from_base(base_monitor=monitor)
        return None

    @classmethod
    def from_base(cls, base_monitor : BaseMonitor) -> Display:
        return cls(x=base_monitor.x, y=base_monitor.y, width=base_monitor.width, height=base_monitor.height, is_primary=base_monitor.is_primary)


    def get_screenshot(self, grid : Optional[Grid] = None):
        with mss() as sct:
            monitor_dict = {"top": self.y, "left": self.x, "width": self.width, "height": self.height}
            sct_img = sct.grab(monitor_dict)
            image = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        if grid:
            grid_mapper = DisplayMapper(display=self, natural_grid=grid)
            image = self.draw_grid(image, grid_mapper)

        return image

    @staticmethod
    def draw_grid(image, display_mapper : DisplayMapper):
        natural_x = range(0, display_mapper.natural_grid.x_size+1)
        natural_y = range(0, display_mapper.natural_grid.y_size+1)
        x_pixel_list = [display_mapper.get_px_x(x) for x in natural_x]
        y_pixel_list = [display_mapper.get_px_y(y) for y in natural_y]

        for x_px in x_pixel_list:
            draw_vertical_line(image, x_px)
        for y_px in y_pixel_list:
            draw_horizontal_line(image, y_px)
        return image


@dataclass
class Grid:
    x_size : int
    y_size : int

    def in_bounds(self, lattice_point : LatticePoint) -> bool:
        return 0 <= lattice_point.x <= self.x_size and 0 <= lattice_point.y <= self.y_size


@dataclass
class LatticePoint:
    x: int
    y: int


@dataclass
class DisplayMapper:
    display : Display
    natural_grid : Grid

    @classmethod
    def create_default(cls, display : Display = Display.get_primary(), small_dim : int = 100) -> DisplayMapper:
        scale_factor = small_dim / min(display.width, display.height)
        x_length = int(display.width * scale_factor)
        y_length = int(display.height * scale_factor)
        grid = Grid(x_size=x_length, y_size=y_length)

        return cls(display=display, natural_grid=grid)

    def get_pixel(self, natural_point : LatticePoint) -> LatticePoint:
        if not self.natural_grid.in_bounds(lattice_point=natural_point):
            raise ValueError(f"Lattice point {natural_point} is outside of the grid bounds")
        pixel_x = round(natural_point.x * self.display.width / self.natural_grid.x_size)
        pixel_y = round(natural_point.y * self.display.height / self.natural_grid.y_size)
        return LatticePoint(x=pixel_x, y=pixel_y)

    def get_px_x(self, natural_x : int) -> int:
        return round(natural_x * self.display.width / self.natural_grid.x_size)

    def get_px_y(self, natural_y : int) -> int:
        return round(natural_y * self.display.height / self.natural_grid.y_size)







def draw_horizontal_line(img, y_pos, line_color=(255, 0, 0), line_width=1):
    draw = ImageDraw.Draw(img)
    draw.line([(0, y_pos), (img.width, y_pos)], fill=line_color, width=line_width)


def draw_vertical_line(img, x_pos, line_color=(255, 0, 0), line_width=1):
    draw = ImageDraw.Draw(img)
    draw.line([(x_pos, 0), (x_pos, img.height)], fill=line_color, width=line_width)
