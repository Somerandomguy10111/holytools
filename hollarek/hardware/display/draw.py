from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt
from PyQt5.QtCore import QTimer

class Indicator(QWidget):
    def __init__(self, visual_size : int = 30, flare_duration : float = 2):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint | Qt.WindowTransparentForInput)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.resize(1080, 1920)

        self.visual = self.get_visual(size=visual_size)
        self.flare_duration : float = flare_duration

        self.opacity_effect = QGraphicsOpacityEffect(self.visual)
        self.opacity_effect.setOpacity(0)
        self.visual.setGraphicsEffect(self.opacity_effect)

        self.flare_up = self.get_flare_up()
        self.flare_down = self.get_flare_down()
        self.flare_up.finished.connect(self.flare_down.start)

    # ----------------------------------------------

    def flare(self, x,y):
        self.visual.move(x, y)
        self.flare_up.start()

    # ----------------------------------------------

    def get_visual(self, size : int):
        visual = QWidget(self)
        visual.setStyleSheet("background-color: red; border-radius: 15px;")
        visual.resize(size, size)
        return visual

    def get_flare_up(self):
        anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim.setStartValue(0)
        anim.setEndValue(1)
        anim.setDuration(int(self.flare_duration*1000/2.))
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        return anim

    def get_flare_down(self):
        anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        anim.setStartValue(1)
        anim.setEndValue(0)
        anim.setDuration(int(self.flare_duration*1000/2.))
        anim.setEasingCurve(QEasingCurve.InOutQuad)
        return anim

if __name__ == "__main__":
    def main():
        app = QApplication([])

        window = Indicator()
        window.show()

        def trigger_flare():
            print(f'Triggered flare')
            window.flare(500, 500)

        # countdown = Countdown(duration=2, on_expiration=trigger_flare)
        # countdown.start()
        timer = QTimer()
        timer.timeout.connect(trigger_flare)
        timer.setSingleShot(True)  # Ensure the timer only triggers once

        timer.start(2000)
        # app.exec_()

        app.exec_()

    main()
