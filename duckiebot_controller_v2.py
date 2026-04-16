import time

import pyautogui

keyboard_set = {"w", "s", "a", "d"}  # Keys we will use for control


class DuckiebotKeyboardControllerV2:
    def __init__(self, gain=0.1):
        self.gain = gain
        self.is_in_autopilot = False

    def circle(self, key):
        self._release_all()
        self.set_gain(0.3)
        print("> Moving in circles.")
        pyautogui.keyDown("w")
        for _ in range(10):
            pyautogui.keyDown(key)
            time.sleep(0.15)
            pyautogui.keyUp(key)
            time.sleep(0.9)

    def turn_left(self, duration):
        self._turn_and_stop("a", duration)

    def turn_right(self, duration):
        self._turn_and_stop("d", duration)

    def drive_forward(self):
        self._release_all()
        print("> Moving forward.")
        pyautogui.keyDown("w")

    def drive_backward(self):
        self._release_all()
        print("> Moving backwards.")
        pyautogui.keyDown("s")

    def set_gain(self, new_gain):
        old_gain = self.gain
        steps = int(round(new_gain - old_gain, 1) * 10)
        if steps > 0:
            for _ in range(steps):
                pyautogui.press("x")
                self.gain += 0.1
        elif steps < 0:
            for _ in range(abs(steps)):
                pyautogui.press("z")
                self.gain -= 0.1
        print(f"> Changing gain from {old_gain:.2f} to {self.gain:.2f}")

    def emergency_stop(self):
        self._release_all()

    def _release_all(self):
        for key in keyboard_set:
            pyautogui.keyUp(key)
        if self.is_in_autopilot:
            pyautogui.keyDown("f")
            self.is_in_autopilot = False

    def turn_and_keep_moving(self, key):
        self._release_all()
        self.set_gain(0.2)
        print("> Turning.")
        pyautogui.keyDown("w")
        pyautogui.keyDown(key)
        time.sleep(1.3)
        pyautogui.keyUp(key)

    def _turn_and_stop(self, key, duration):
        self._release_all()
        self.set_gain(0.2)
        print("> Turning and stopping.")
        pyautogui.keyDown("w")
        pyautogui.keyDown(key)
        time.sleep(duration)
        pyautogui.keyUp(key)
        pyautogui.keyUp("w")

    def turn_tiny(self, key):
        print("> Turning very shortly.")
        pyautogui.keyDown(key)
        time.sleep(0.15)
        pyautogui.keyUp(key)

    def toggle_autopilot(self):
        pyautogui.press("f")
        self.is_in_autopilot = True
