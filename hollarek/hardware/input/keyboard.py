import pyautogui
import time

class Keyboard:
    @staticmethod
    def type(msg: str):
        pyautogui.write(msg, interval=0.02)  # You can adjust the typing interval as needed


if __name__ == "__main__":
    print(f'Will now type something')
    time.sleep(2)
    Keyboard.type("Hello, this is a test typing.")
