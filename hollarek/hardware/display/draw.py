from PyQt5.QtWidgets import QApplication, QWidget, QGraphicsOpacityEffect
from PyQt5.QtCore import QPropertyAnimation, QEasingCurve, Qt


class Window(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)  # Make the window frameless
        self.setAttribute(Qt.WA_TranslucentBackground)  # Make the window background transparent
        self.resize(600, 600)

        self.child = QWidget(self)
        self.child.setStyleSheet("background-color: red; border-radius: 15px;")
        self.child.resize(100, 100)
        self.child.move(250, 250)  # Center the child initially

        # Set up opacity effect
        self.opacity_effect = QGraphicsOpacityEffect(self.child)
        self.child.setGraphicsEffect(self.opacity_effect)

        # Create animation for the opacity effect
        self.anim = QPropertyAnimation(self.opacity_effect, b"opacity")
        self.anim.setEndValue(0)  # Fade out to completely transparent
        self.anim.setStartValue(1)  # Start fully opaque
        self.anim.setDuration(1500)  # Duration of the animation
        self.anim.setEasingCurve(QEasingCurve.InOutQuad)  # Smooth in-out transition
        self.anim.start()


if __name__ == "__main__":
    def main():
        app = QApplication([])

        window = Window()
        window.show()

        app.exec_()


    main()
