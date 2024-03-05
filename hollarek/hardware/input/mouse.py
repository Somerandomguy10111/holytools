import time

import pyautogui
from hollarek.hardware.display import Display, LatticePoint, ClickIndicator
from multiprocessing import Process, Pipe


class Mouse:
    def __init__(self):
        self.click_indicator : ClickIndicator = ClickIndicator()
        self.parent_conn, child_conn = Pipe()
        self.p = Process(target=self.click_indicator.start)
        self.p.start()

    def click(self, pixel_x : int, pixel_y : int, on_primary_display: bool = True, visualize : bool = True):
        point = LatticePoint(pixel_x, pixel_y)
        display = Display.get_primary() if on_primary_display else Display.get_secondary()
        if not display.in_bounds(point):
            raise ValueError(f"Point {point} is outside of the display bounds")
        rel_to_primary = display.get_relative_to_primary(pixel=point)

        pyautogui.click(rel_to_primary.x, rel_to_primary.y)

        if visualize:
            print(f'Visualized click')
            # self.click_indicator.visualize_click(rel_to_primary.x, rel_to_primary.y, on_primary_display)
            self.parent_conn.send('flare')  # Trigger flare

    def __del__(self):
        self.p.join()

if __name__ == "__main__":
    # primary = Display.get_primary()
    # secondary = Display.get_secondary()
    #
    # print(f'primary display coordinates are: {primary.x}, {primary.y}')
    # print(f'secondary display coordinates are: {secondary.x}, {secondary.y}')
    #
    # secondary_display = Display.get_secondary()
    # print(secondary_display.get_relative_to_primary(pixel=LatticePoint(0, 0)))
    #
    mouse = Mouse()
    time.sleep(1)
    mouse.click(100, 100)

    time.sleep(100)