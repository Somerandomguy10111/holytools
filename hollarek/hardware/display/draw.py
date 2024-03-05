import threading

from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QTimer, QSize
import math
import sys


class Indicator(QWidget):
    def __init__(self, monitor_index: int = 0, min_radius: int = 15, max_radius: int = 30, flare_duration: float = 0.75):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)

        screens = QApplication.screens()
        if monitor_index < 0 or monitor_index >= len(screens):
            raise ValueError(f"Invalid monitor index: {monitor_index}. Available screens: {len(screens)}")

        screen = screens[monitor_index]
        geometry = screen.geometry()
        self.move(geometry.x(), geometry.y())  # Move the window to the screen
        self.screen_width = geometry.width()
        self.screen_height = geometry.height()
        self.resize(self.screen_width, self.screen_height)

        self.visual = self._get_visual(size=2 * min_radius)  # Start with the min_radius
        self.flare_duration: float = flare_duration
        self.min_radius = min_radius
        self.max_radius = max_radius

        self.opacity_effect = QGraphicsOpacityEffect(self.visual)
        self.opacity_effect.setOpacity(0)  # Start fully transparent
        self.visual.setGraphicsEffect(self.opacity_effect)

        # Use the unified method to get animations
        self.flare_up = self._get_flare_animation(start=True)
        self.flare_down = self._get_flare_animation(start=False)
        self.flare_up.finished.connect(self.flare_down.start)
        self.size_expansion = self._get_size_expansion_animation()
        self.size_expansion.valueChanged.connect(self._update_visual_shape)

        self.old_size = min_radius*2
        self.delta = 0


    # ----------------------------------------------

    def flare(self, x, y):
        self.visual.move(x - self.max_radius, y - self.max_radius)  # Center the visual
        self.flare_up.start()
        self.size_expansion.start()  # Start size expansion alongside the flare animation

    # ----------------------------------------------

    def _get_visual(self, size: int):
        visual = QWidget(self)
        # Set border-radius to half the size of the widget to make it a circle
        visual.setStyleSheet(f"background-color: red; border-radius: {size // 2}px;")
        visual.resize(size, size)
        return visual

    def _get_flare_animation(self, start: bool):
        anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim.setStartValue(0 if start else 0.75)
        anim.setEndValue(0.75 if start else 0)
        ms_duration = self.flare_duration * 1000
        duration = ms_duration * 0.4 if start else ms_duration*0.6
        anim.setDuration(int(duration))
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        return anim

    def _get_size_expansion_animation(self):
        anim = QPropertyAnimation(self.visual, b'size')
        anim.setStartValue(QSize(2 * self.min_radius, 2 * self.min_radius))
        anim.setEndValue(QSize(2 * self.max_radius, 2 * self.max_radius))
        anim.setDuration(int(self.flare_duration * 1000))  # Match the total duration of flare up and down
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        return anim

    def _update_visual_shape(self, new_size):
        new_radius = min(new_size.width(), new_size.height()) // 2
        self.visual.setStyleSheet(f"background-color: red; border-radius: {new_radius}px;")
        self.delta += (new_radius*2-self.old_size)/2
        rounded_delta = round(self.delta)
        self.visual.move(self.visual.x()-int(rounded_delta), self.visual.y()-int(rounded_delta))
        self.delta = self.delta-rounded_delta
        self.old_size = new_radius * 2




class ClickIndicator:
    def __init__(self):
        pass

    # def visualize_click(self, x : int, y : int, on_primary : bool):
    #     monitor_index = 0 if on_primary else 1
    #     indicator = self.indicator_map[monitor_index]
    #     indicator.flare(x, y)

    @staticmethod
    def start():
        app = QApplication([])
        indicator = Indicator()
        indicator.show()

        # indicator_map : dict[int, Indicator] = {}
        # for index, monitor in enumerate(QApplication.screens()):
        #     indicator = Indicator(monitor_index=index)
        #     indicator_map[index] = indicator
        #     indicator.show()

        # Set up a QTimer to trigger the flare
        timer = QTimer()
        timer.singleShot(300, lambda: indicator.flare(100, 100))  # Set for 5000 milliseconds (5 seconds)

        app.exec_()

    # def handle_msg(self, msg : str):


        # while True:
        #     if conn.poll():  # Check if there is a message
        #         msg = conn.recv()  # Receive the message
        #         print(f'recieved mesage : {msg}')
        #         if msg == 'flare':
        #             primary = self.indicator_map[0]
        #             timer = QTimer()
        #             timer.singleShot(50, lambda: primary.flare(100, 100))  # Set for 5000 milliseconds (5 seconds)
        #         elif msg == 'exit':
        #             break

def good():
    app = QApplication([])
    indicator = Indicator()
    indicator.show()

    # Set up a QTimer to trigger the flare
    timer = QTimer()
    timer.singleShot(300, lambda: indicator.flare(100, 100))  # Set for 5000 milliseconds (5 seconds)

    app.exec_()



if __name__ == "__main__":
    from multiprocessing import Process
    p = Process(target=good)
    p.start()