from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from PIL import Image, ImageDraw, ImageFont
from mss import mss
from screeninfo import get_monitors
from screeninfo import Monitor as BaseMonitor
from .types import Grid, LatticePoint
from PIL.Image import Image as PILImage
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
    # navigation

    def map_to_virtual_display(self, pixel : LatticePoint) -> LatticePoint:
        origin = LatticePoint(x=self.x, y = self.y)
        return origin + pixel

    def in_bounds(self, pixel : LatticePoint):
        return 0 <= pixel.x <= self.width and 0 <= pixel.y <= self.height

    def is_horizontal(self):
        return self.width > self.height

    def is_vertical(self):
        return self.height > self.width

    # ----------------------------------------------
    # screenshot

    def get_screenshot(self, grid : Optional[Grid] = None):
        with mss() as sct:
            monitor_dict = {"top": self.y, "left": self.x, "width": self.width, "height": self.height}
            sct_img = sct.grab(monitor_dict)
            image = Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')
        if grid:
            overlay = self.draw_grid_lines(size = image.size, grid=grid)
            self.draw_cell_labels(overlay, grid)
            image = Image.alpha_composite(image.convert('RGBA'), overlay)

        return image


    def draw_grid_lines(self, size : (int, int), grid : Grid) -> PILImage:
        display_mapper = DisplayMapper(display=self, input_grid=grid)
        overlay = Image.new('RGBA', size, (255, 255, 255, 0))  # Completely transparent
        if overlay.mode != 'RGBA':
            overlay = overlay.convert('RGBA')
        for x in range(0, display_mapper.input_grid.x_size + 1):
            x_px = display_mapper.map_horizontal(x=x)
            draw_vertical_line(overlay, x_px)
        for y in range(0, display_mapper.input_grid.y_size + 1):
            y_px = display_mapper.map_vertical(y=y)
            draw_horizontal_line(overlay, y_px)
        return overlay

    def draw_cell_labels(self, image: PILImage, grid: Grid):
        display_mapper = DisplayMapper(display=self, input_grid=grid)
        ImageDraw.Draw(image)
        for (x,y) in [(x,y) for x in range(grid.x_size) for y in range(grid.y_size)]:
            x_px_left = display_mapper.map_horizontal(x)
            x_px_right = display_mapper.map_horizontal(x + 1)
            y_px_top = display_mapper.map_vertical(y)
            y_px_bottom = display_mapper.map_vertical(y + 1)
            center_x = (x_px_left + x_px_right) // 2
            center_y = (y_px_top + y_px_bottom) // 2

            cell_number = y * grid.x_size + x + 1  # Calculate the cell number as before
            hex_number = hex(cell_number)[2:].upper()  # Convert to hex, remove "0x", convert to uppercase
            self.draw_text(text=str(hex_number), image=image, x_pos=center_x, y_pos=center_y, font_size=int(400/grid.x_size))


    @staticmethod
    def draw_text(text : str, image : PILImage, x_pos : int, y_pos : int, font_size=20, opacity = 128):
        font = ImageFont.load_default(size=font_size)

        draw = ImageDraw.Draw(image)
        color = (0, 0, 0, opacity)
        centered_x = x_pos - font_size // 2
        centered_y = y_pos - font_size // 2
        draw.text((centered_x, centered_y), text, fill=color, font=font)


@dataclass
class DisplayMapper:
    input_grid : Grid
    display : Display

    def get_pixel(self, point : LatticePoint) -> LatticePoint:
        if not self.input_grid.is_in_bounds(point=point):
            raise ValueError(f"Lattice point {point} is outside of the grid bounds")
        return LatticePoint(x=self.map_horizontal(point.x), y=self.map_vertical(point.y))

    def map_horizontal(self, x : int) -> int:
        if not self.input_grid.in_horizontal_bounds(x=x):
            raise ValueError(f"X value {x} is outside of the grid bounds")
        return round(x * self.display.width / self.input_grid.x_size)

    def map_vertical(self, y : int) -> int:
        if not self.input_grid.is_in_vertical_bounds(y=y):
            raise ValueError(f"Y value {y} is outside of the grid bounds")
        return round(y * self.display.height / self.input_grid.y_size)





def draw_horizontal_line(img, y_pos, line_color=(255, 0, 0), line_width=1, opacity=128):
    draw = ImageDraw.Draw(img)
    # Adjust line color to include opacity
    line_color_with_opacity = (line_color[0], line_color[1], line_color[2], opacity)
    # Draw the line with the specified translucent color and line width
    draw.line([(0, y_pos), (img.width, y_pos)], fill=line_color_with_opacity, width=line_width)

def draw_vertical_line(img, x_pos, line_color=(255, 0, 0), line_width=1, opacity=128):
    draw = ImageDraw.Draw(img)
    # Adjust line color to include opacity
    line_color_with_opacity = (line_color[0], line_color[1], line_color[2], opacity)
    # Draw the line with the specified translucent color and line width
    y_start = 0
    y_end = img.height
    draw.line([(x_pos, y_start), (x_pos, y_end)], fill=line_color_with_opacity, width=line_width)
