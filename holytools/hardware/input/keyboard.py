import time

from holytools.events import InputWaiter
from pynput.keyboard import Key as PynputKey
from pynput.keyboard import KeyCode
from pynput.keyboard import Controller as KeyboardController
from pynput import keyboard
from typing import Union
import atexit

class Keyboard:
    def __init__(self):
        self._keyboard = KeyboardController()

        def del_keyboard():
            del self._keyboard
        atexit.register(del_keyboard)

    def type(self, msg: str):
        for char in msg:
            self._keyboard.type(char)  # Type the character
            time.sleep(0.02)  # Interval between keys


Key = Union[PynputKey, KeyCode]


class KeyboardListener:
    def __init__(self, verbose : bool = False):
        self.verbose = verbose

        self.listener = keyboard.Listener(on_press=self._on_press, on_release=self._on_release)
        self.listener.start()
        self.pressed_buttons : set[Key] = set()
        self.press_waiters : list[InputWaiter] = []
        self.release_waiters : list[InputWaiter] = []

    def wait_on_hold(self, key : Key, duration : float):
        while True:
            press_waiter = self._register_press_waiter(target_value=key)
            press_waiter.get()
            if self.verbose:
                print(f'Press of key \"{key}\" registered. Hold for {duration} to finsh')

            time.sleep(duration)
            still_held  = self.check_key_pressed(key=key)
            if still_held:
                break

    def check_key_pressed(self, key : Key):
        return key in self.pressed_buttons

    def wait_on_press(self, key : Key):
        waiter = self._register_press_waiter(target_value=key)
        waiter.get()

    def get_next_key(self) -> Key:
        waiter = InputWaiter()
        self.press_waiters.append(waiter)
        return waiter.get()

    # ---------------------------------------------------------

    def _on_press(self, key: Key):
        if self.verbose:
            print(f'key press registered {key}')
        for waiter in self.press_waiters:
            waiter.write(key)
        self._remove_finished_waiters()
        self.pressed_buttons.add(key)


    def _on_release(self, key : Key):
        if self.verbose:
            print(f'key release registered {key}')
        if key in self.pressed_buttons:
            self.pressed_buttons.remove(key)
        for waiter in self.release_waiters:
            waiter.write(key)
        self._remove_finished_waiters()


    def _remove_finished_waiters(self):
        for waiter in self.press_waiters:
            if waiter.is_done:
                self.press_waiters.remove(waiter)
        for waiter in self.release_waiters:
            if waiter.is_done:
                self.release_waiters.remove(waiter)

    def _register_press_waiter(self, target_value : Key) -> InputWaiter:
        waiter = InputWaiter(target_value)
        self.press_waiters.append(waiter)
        return waiter


if __name__ == "__main__":
    # listener = KeyboardListener(verbose=True)
    test_keyboard = Keyboard()
    listener = KeyboardListener(verbose=True)
    listener.wait_on_hold(key=KeyCode.from_char(char='a'), duration=20)
