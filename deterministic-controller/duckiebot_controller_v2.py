import time

import pyautogui

keyboard_set = {"w", "a", "s", "d", "z", "x"}  # Keys we will use for control


class DuckiebotKeyboardControllerV2:
    def __init__(self, gain=0.1):
        self.gain = gain

    def turn_left_long_curve(self):
        self._turn_long_curve("a")

    def turn_right_long_curve(self):
        self._turn_long_curve("d")

    def circle(self, key):
        self._release_all()
        self.set_gain(0.4)
        pyautogui.keyDown("w")
        print("Moving in circles.")
        for _ in range(18):  # TODO adjust to go in a circle with 55cm radius
            pyautogui.keyDown(key)
            time.sleep(0.4)  # TODO adjust to go in a circle with 55cm radius
            pyautogui.keyUp(key)
            time.sleep(0.7)  # TODO adjust to go in a circle with 55cm radius

    def turn_left(self):
        self._turn_short_curve("a")

    def turn_right(self):
        self._turn_short_curve("d")

    def drive_forward(self):
        self._release_all()
        pyautogui.keyDown("w")
        print("Moving forward.")

    def drive_backward(self):
        self._release_all()
        pyautogui.keyDown("s")
        print("Moving backwards.")

    def set_gain(self, new_gain):
        old_gain = self.gain
        steps = int((new_gain - old_gain) * 10)
        if steps > 0:
            for _ in range(steps):
                pyautogui.press("x")
                self.gain += 0.1
        elif steps < 0:
            for _ in range(abs(steps)):
                pyautogui.press("z")
                self.gain -= 0.1
        print(f"Changing gain from {old_gain:.2f} to {self.gain:.2f}")

    def emergency_stop(self):
        self._release_all()

    @staticmethod
    def _release_all():
        for key in keyboard_set:
            pyautogui.keyUp(key)

    def _turn_long_curve(self, key):
        self._release_all()
        self.set_gain(0.4)
        pyautogui.keyDown("w")
        pyautogui.keyDown(key)
        time.sleep(0.9) # TODO adjust this to make it 90 degrees
        pyautogui.keyUp(key)
        print("Turning long curve.")

    def _turn_short_curve(self, key):
        self._release_all()
        self.set_gain(0.4)
        pyautogui.keyDown("w")
        pyautogui.keyDown(key)
        time.sleep(0.45) # TODO adjust this to make it 45 degrees
        pyautogui.keyUp(key)
        print("Turning short curve.")

    def turn_tiny(self, key):
        pyautogui.keyDown(key)
        time.sleep(0.15)
        pyautogui.keyUp(key)
        print("Turning very shortly.")
