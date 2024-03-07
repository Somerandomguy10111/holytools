import time

import pyautogui
from hollarek.hardware.display import Display, LatticePoint, ClickIndicator
from multiprocessing import Process, Pipe
from hollarek.hardware.display import Click, Grid


class Mouse:
    def __init__(self):
        self.click_indicator : ClickIndicator = ClickIndicator()
        self.parent_conn, child_conn = Pipe()
        self.p = Process(target=self.click_indicator.start, args=(child_conn,))
        self.p.start()

    def click(self, pixel_x : int, pixel_y : int, on_primary_display: bool = True, visualize : bool = True):
        point = LatticePoint(pixel_x, pixel_y)
        display = Display.get_primary() if on_primary_display else Display.get_secondary()
        if not display.in_bounds(point):
            raise ValueError(f"Point {point} is outside of the display bounds")
        rel_to_primary = display.map_to_virtual_display(pixel=point)

        pyautogui.click(rel_to_primary.x, rel_to_primary.y)

        if visualize:
            print(f'Visualized click')
            click = Click(point=point, display_index=0 if on_primary_display else 1)
            self.parent_conn.send(click.to_str())

    def __del__(self):
        self.p.join()

if __name__ == "__main__":
    # mouse = Mouse()
    # # mouse.click(500, 500, on_primary_display= True)
    # mouse.click(500, 500, on_primary_display= False)

    # time.sleep(100)


    # while True:
    #     time.sleep(0.1)
    #     print(pyautogui.position())

    from hollarek.hardware.display import Display

    display = Display.get_primary()
    img = display.get_screenshot(grid=Grid(25,25))
    img.show()
