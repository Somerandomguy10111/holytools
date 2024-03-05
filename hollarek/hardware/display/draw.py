from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt, QTimer, QSize
import math


class Indicator(QWidget):
    def __init__(self, min_radius: int = 15, max_radius: int = 30, flare_duration: float = 0.75):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.screen_width = 1080
        self.screen_height = 1920
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


if __name__ == "__main__":
    def main():
        app = QApplication([])

        indicator = Indicator()
        indicator.show()

        def trigger_flare():
            print('Triggered flare')
            indicator.flare(500, 500)

        timer = QTimer()
        timer.timeout.connect(trigger_flare)
        timer.setSingleShot(True)
        timer.start(500)

        app.exec_()

    main()
