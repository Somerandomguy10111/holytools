import pyautogui
from hollarek.hardware.display import Display, LatticePoint


class Mouse:
    @staticmethod
    def click(pixel_x : int, pixel_y : int, on_primary_display: bool, visuals : bool = False):
        point = LatticePoint(pixel_x, pixel_y)
        display = Display.get_primary() if on_primary_display else Display.get_secondary()

        if not display.in_bounds(point):
            raise ValueError(f"Point {point} is outside of the display bounds")

        rel_to_primary = display.map_relative_to_primary(pixel=point)
        pyautogui.click(rel_to_primary.x, rel_to_primary.y)


if __name__ == "__main__":
    primary = Display.get_primary()
    secondary = Display.get_secondary()

    print(f'primary display coordinates are: {primary.x}, {primary.y}')
    print(f'secondary display coordinates are: {secondary.x}, {secondary.y}')

    secondary_display = Display.get_secondary()
    print(secondary_display.map_relative_to_primary(pixel=LatticePoint(0, 0)))