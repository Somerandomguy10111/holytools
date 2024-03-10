import pyautogui
from hollarek.events import InputWaiter, Countdown
from pynput.keyboard import Key
from pynput import keyboard
import time

class Keyboard:
    @staticmethod
    def type(msg: str):
        pyautogui.write(msg, interval=0.02)  # You can adjust the typing interval as needed


if __name__ == "__main__":
    print(f'Will now type something')
    time.sleep(2)
    Keyboard.type("Hello, this is a test typing.")



class KeyboardListener:
    def __init__(self):
        self.listener = keyboard.Listener(on_press=self._add_pressed, on_release=self._remove_pressed)
        self.pressed_buttons : set[Key] = set()
        self.press_waiters : list[InputWaiter] = []
        self.release_waiters : list[InputWaiter] = []

    def wait_on_hold(self, key : Key, duration):
        def check_key_pressed():
            return key in self.pressed_buttons

        while True:
            press_waiter = self._register_press_waiter(target_value=key)
            press_waiter.read()
            countdown = Countdown(duration=duration, on_expiration=check_key_pressed)
            countdown.start()
            still_held = countdown.finish()
            if still_held:
                break

    def wait_on_press(self, key : Key):
        waiter = self._register_press_waiter(target_value=key)
        waiter.read()

    def get_next_key(self) -> Key:
        waiter = InputWaiter()
        self.press_waiters.append(waiter)
        return waiter.read()

    # ---------------------------------------------------------

    def _add_pressed(self, key: Key):
        for waiter in self.press_waiters:
            waiter.write(key)
        self._remove_finished_waiters()
        self.pressed_buttons.add(key)

    def _remove_pressed(self, key : Key):
        if key in self.pressed_buttons:
            self.pressed_buttons.remove(key)
        for waiter in self.release_waiters:
            waiter.write(key)
        self._remove_finished_waiters()


    def _remove_finished_waiters(self):
        for waiter in self.press_waiters:
            if waiter.input_found:
                self.press_waiters.remove(waiter)

    def _register_press_waiter(self, target_value : Key) -> InputWaiter:
        waiter = InputWaiter(target_value)
        self.press_waiters.append(waiter)
        return waiter

    # def _register_release_waiter(self, target_value : Key) -> InputWaiter:
    #     waiter = InputWaiter(target_value)
    #     self.release_waiters.append(waiter)
    #     return waiter
    #
