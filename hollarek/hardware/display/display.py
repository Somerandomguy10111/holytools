from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from PIL import Image, ImageDraw
from mss import mss
from screeninfo import get_monitors
from screeninfo import Monitor as BaseMonitor
from .types import Grid, LatticePoint

# ----------------------------------------------


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

    # ----------------------------------------------
    # screenshot

    def get_screenshot(self, grid : Optional[Grid] = None):
        with mss() as sct:
            monitor_dict = {"top": self.y, "left": self.x, "width": self.width, "height": self.height}
            sct_img = sct.grab(monitor_dict)
            image = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        if grid:
            image = self._draw_grid(image, grid)

        return image


    def _draw_grid(self, image, grid):
        display_mapper = DisplayMapper(display=self, input_grid=grid)
        for x in range(0, display_mapper.input_grid.x_size + 1):
            x_px = display_mapper.map_horizontal(x=x)
            draw_vertical_line(image, x_px)
        for y in range(0, display_mapper.input_grid.y_size + 1):
            y_px = display_mapper.map_vertical(y=y)
            draw_horizontal_line(image, y_px)
        return image



@dataclass
class DisplayMapper:
    display : Display
    input_grid : Grid

    def get_pixel(self, point : LatticePoint) -> LatticePoint:
        if not self.input_grid.is_in_bounds(lattice_point=point):
            raise ValueError(f"Lattice point {point} is outside of the grid bounds")
        return LatticePoint(x=self.map_horizontal(point.x), y=self.map_vertical(point.y))

    def map_horizontal(self, x : int) -> int:
        return round(x * self.display.width / self.input_grid.x_size)

    def map_vertical(self, y : int) -> int:
        return round(y * self.display.height / self.input_grid.y_size)


def draw_horizontal_line(img, y_pos, line_color=(255, 0, 0), line_width=1):
    draw = ImageDraw.Draw(img)
    draw.line([(0, y_pos), (img.width, y_pos)], fill=line_color, width=line_width)


def draw_vertical_line(img, x_pos, line_color=(255, 0, 0), line_width=1):
    draw = ImageDraw.Draw(img)
    draw.line([(x_pos, 0), (x_pos, img.height)], fill=line_color, width=line_width)
