from __future__ import annotations

from dataclasses import dataclass
from enum import Enum

from PIL import ImageDraw, Image, ImageFont
from PIL.Image import Image as PILImage
from .types import Grid, LatticePoint, Vector


class Orientation(Enum):
    HORIZONTAL = 0
    VERTICAL = 1


class EditableImage:
    def __init__(self, img : PILImage, mapper : PixelMapper):
        self.pil_image : PILImage = img.convert('RGBA')

        ImageDraw.Draw(self.pil_image)
        self.mapper : PixelMapper = mapper
        self.overlay = Image.new('RGBA', self.pil_image.size, (255, 255, 255, 0))
        self.overlay = self.overlay.convert('RGBA')
        self.overlay_draw = ImageDraw.Draw(self.overlay)


    def get_grid_overlay(self) -> PILImage:
        self.draw_cell_labels()
        self.draw_grid_lines()
        print(self.pil_image.mode, self.overlay.mode)
        return Image.alpha_composite(self.pil_image, self.overlay)


    def draw_cell_labels(self):
        grid = self.mapper.input_grid
        for cell_number, lattice_vector in enumerate(grid.get_lattice_vectors(), start=1):
            center = self.mapper.get_pixel(lattice_vector + Vector(x=0.5, y=0.5))
            hex_number = hex(cell_number)[2:].upper()
            self.draw_text(text=hex_number, point=center, font_size=int(400 / grid.x_size))


    def draw_grid_lines(self):
        for x in range(0, self.mapper.input_grid.x_size + 1):
            x_px = self.mapper.map_horizontal(x=x)
            self.draw_line(coordinate=x_px, orientation=Orientation.VERTICAL)
        for y in range(0, self.mapper.input_grid.y_size + 1):
            y_px = self.mapper.map_vertical(y=y)
            self.draw_line(coordinate=y_px, orientation=Orientation.HORIZONTAL)


    def draw_line(self, coordinate : int, orientation : Orientation, opacity=128):
        color_vector = (255,0,0, opacity)
        if orientation == Orientation.HORIZONTAL:
            start_pos = (0, coordinate)
            end_pos = (self.overlay.width, coordinate)
        else:
            start_pos = (coordinate, 0)
            end_pos = (coordinate, self.overlay.height)

        self.overlay_draw.line([start_pos, end_pos], fill=color_vector, width=1)


    def draw_text(self, text : str, point : LatticePoint, font_size=20, opacity = 128):
        font = ImageFont.load_default(size=font_size)
        color = (0, 0, 0, opacity)
        delta = LatticePoint(font_size//2, font_size//2)
        centered_point = point - delta
        self.overlay_draw.text(centered_point.as_tuple(), text, fill=color, font=font)


@dataclass
class PixelMapper:
    input_grid : Grid
    output_grid : Grid

    def get_pixel(self, point : LatticePoint) -> LatticePoint:
        if not self.input_grid.is_in_bounds(point=point):
            raise ValueError(f"Lattice point {point} is outside of the grid bounds")
        return LatticePoint(x=self.map_horizontal(point.x), y=self.map_vertical(point.y))

    def map_horizontal(self, x : int) -> int:
        if not self.input_grid.in_horizontal_bounds(x=x):
            raise ValueError(f"X value {x} is outside of the grid bounds")
        return round(x * self.output_grid.x_size / self.input_grid.x_size)

    def map_vertical(self, y : int) -> int:
        if not self.input_grid.is_in_vertical_bounds(y=y):
            raise ValueError(f"Y value {y} is outside of the grid bounds")
        return round(y * self.output_grid.y_size / self.input_grid.y_size)
