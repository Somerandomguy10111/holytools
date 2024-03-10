import pyautogui
import time
from hollarek.events import InputWaiter
from pynput import keyboard
import time
from pynput.keyboard import Key

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
        self.waiters : list[InputWaiter] = []


    def wait_on_press(self, key : Key):
        self.register_waiter()




    # def wait_hold(self, key : Key):


    def get_next_key(self) -> Key:
        waiter = InputWaiter()
        self.waiters.append(waiter)
        return waiter.read()

    # ---------------------------------------------------------

    def _add_pressed(self, key: Key):
        for waiter in self.waiters:
            waiter.write(key)
        self.waiters = []
        self.pressed_buttons.add(key)


    def _remove_pressed(self, key : Key):
        if key in self.pressed_buttons:
            self.pressed_buttons.remove(key)

    def register_waiter(self, target_value : Key) -> InputWaiter:
        waiter = InputWaiter(target_value)
        self.waiters.append(waiter)
        return waiter

#     def on_press(self, key):
#         if key == keyboard.Key.esc:
#             self.start_time = time.time()  # Record the time when Esc is pressed
#             print(f'Esc pressed at {self.start_time}')
#
#     def on_release(self, key):
#         if key == keyboard.Key.esc and self.start_time:
#             elapsed_time = time.time() - self.start_time
#             if elapsed_time >= 1:  # Check if Esc was held for at least 1 second
#                 return False
#             self.start_time = None  # Reset start time if Esc was not held long enough
#
# def wait_for_esc_pressed_for_1_sec():
#     listener = KeyboardListener()
#     with keyboard.Listener(on_press=listener.on_press) as listener:
#         listener.join()
#
# # Call the function
# wait_for_esc_pressed_for_1_sec()
