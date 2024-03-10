import time

import pyautogui
from hollarek.events import InputWaiter, Countdown
from pynput.keyboard import Key as PynputKey
from pynput.keyboard import KeyCode
from pynput import keyboard
from typing import Union

class Keyboard:
    @staticmethod
    def type(msg: str):
        pyautogui.write(msg, interval=0.02)

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
        def check_key_pressed():
            return key in self.pressed_buttons

        while True:
            press_waiter = self._register_press_waiter(target_value=key)
            press_waiter.get()
            if self.verbose:
                print(f'Press of key \"{key}\" registered. Hold for {duration} to finsh')
            countdown = Countdown(duration=duration, on_expiration=check_key_pressed)
            countdown.start()
            still_held = countdown.finish()
            if still_held:
                break

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
    listener = KeyboardListener(verbose=True)

    def press_a():
        Keyboard.type(msg='a')

    Countdown = Countdown(duration=3, on_expiration=press_a)
    Countdown.start()

    time.sleep(10)
    # listener.wait_on_hold(key=KeyCode(char='a'),duration=2)
