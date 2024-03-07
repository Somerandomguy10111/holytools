import time

import pyautogui
from hollarek.hardware.display import Display, LatticePoint, ClickIndicator, Indicator
from multiprocessing import Process, Pipe
from hollarek.hardware.display import Click, Grid
from typing import Optional

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
        rel_to_primary = display.to_virtual_display(pixel=point)

        pyautogui.click(rel_to_primary.x, rel_to_primary.y)

        if visualize:
            print(f'Visualized click')
            click = Click(point=point, display_index=0 if on_primary_display else 1)
            self.parent_conn.send(click.to_str())

    def __del__(self):
        self.p.join()


class TextMouse:
    def __init__(self, input_grid: Grid = Grid(x_size=25, y_size=25)):
        self.mouse : Mouse = Mouse()
        self.input_grid : Grid = input_grid
        self.primary : Display = Display.get_primary()
        self.secondary : Optional[Display] = Display.get_secondary()

    def get_view(self, on_primary_display : bool = True):
        display = self.primary if on_primary_display else self.secondary
        return display.get_screenshot(grid=self.input_grid)

    def click(self, cell_num : int, on_primary_display : bool = True):
        pt = self.input_grid.get_pt(num=cell_num)
        display = self.primary if on_primary_display else self.secondary
        if not display:
            raise ValueError("There is no secondary display")
        mapper = display.get_mapper(grid=self.input_grid)
        px = mapper.map_pt(point=pt)
        self.mouse.click(pixel_x=px.x, pixel_y=px.y, on_primary_display=on_primary_display, visualize=True)



if __name__ == "__main__":
    # mouse = Mouse()
    # # mouse.click(500, 500, on_primary_display= True)
    # mouse.click(500, 500, on_primary_display= False)

    # time.sleep(100)


    # while True:
    #     time.sleep(0.1)
    #     print(pyautogui.position())

    # from hollarek.hardware.display import Display

    # teset = Display.get_primary()
    # img = teset.get_screenshot(grid=Grid(25, 25))
    # img.show()
    text_mouse = TextMouse()
    # #
    while True:
        view = text_mouse.get_view()
        view.show()
        num = int(input(f'Click on cell:'))
        text_mouse.click(num)
        time.sleep(1)

    # from PyQt5.QtGui import *
    # from PyQt5.QtWidgets import *
    # from PyQt5.QtCore import *
    #
    # app = QApplication([])
    # indicator = Indicator()
    # indicator.show()
    # indicator.flare(100,100)
    #
    # # Set up a QTimer to trigger the flare
    # timer = QTimer()
    # timer.singleShot(1000, lambda: indicator.flare(300, 300))  # Set for 5000 milliseconds (5 seconds)
    # app.exec_()