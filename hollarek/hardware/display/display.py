from __future__ import annotations

from dataclasses import dataclass
from typing import Optional
from PIL import Image
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
            return Image.frombytes('RGB', sct_img.size, sct_img.bgra, 'raw', 'BGRX')


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

