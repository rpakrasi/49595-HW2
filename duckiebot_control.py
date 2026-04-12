#!/usr/bin/env python3
"""Reusable Duckiebot terminal launch and keyboard control helpers."""

import subprocess
import time

import pyautogui


class DuckiebotTerminalLauncher:
    """Launches Duckiebot commands in separate macOS Terminal windows."""

    def __init__(self, duckiebot_name):
        self.duckiebot_name = duckiebot_name

    def _run_terminal_command(self, command):
        apple_script = f"""
        tell application "Terminal"
            activate
            do script "{command}"
        end tell
        """
        subprocess.run(["osascript", "-e", apple_script], check=True)

    def run_keyboard_control(self):
        command = f"dts duckiebot keyboard_control {self.duckiebot_name} --browser"
        self._run_terminal_command(command)
        print(f"\n✓ Keyboard control launched for {self.duckiebot_name}")
        print("  Browser should open with the controller interface")

    def run_lane_following_demo(self):
        command = (
            "dts duckiebot demo --demo_name lane-following "
            f"--duckiebot_name {self.duckiebot_name} --debug"
        )
        self._run_terminal_command(command)
        print(f"\n✓ Lane-following demo launched for {self.duckiebot_name}")


class DuckiebotKeyboardController:
    """Sends keyboard-control inputs via pyautogui."""

    def __init__(self, gain_step=0.1):
        self.gain_step = gain_step

    def focus_controller_window(self, wait_seconds=3):
        time.sleep(wait_seconds)
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(screen_width // 2, screen_height // 2)
        time.sleep(0.5)

    def press_key(self, key_name, duration_seconds=0.15):
        pyautogui.press(key_name)
        time.sleep(duration_seconds)

    def set_gain(self, target_gain, current_gain=0.0):
        steps = round((target_gain - current_gain) / self.gain_step)

        if steps > 0:
            for _ in range(steps):
                pyautogui.press("x")
                time.sleep(0.15)
        elif steps < 0:
            for _ in range(abs(steps)):
                pyautogui.press("z")
                time.sleep(0.15)

    def turn_left(self, duration_seconds):
        pyautogui.keyDown("a")
        time.sleep(duration_seconds)
        pyautogui.keyUp("a")

    def turn_right(self, duration_seconds):
        pyautogui.keyDown("d")
        time.sleep(duration_seconds)
        pyautogui.keyUp("d")

    def drive_forward(self, duration_seconds):
        pyautogui.keyDown("w")
        time.sleep(duration_seconds)
        pyautogui.keyUp("w")

    def drive_backward(self, duration_seconds):
        pyautogui.keyDown("s")
        time.sleep(duration_seconds)
        pyautogui.keyUp("s")

    def increase_trim(self):
        self.press_key("v")

    def decrease_trim(self):
        self.press_key("c")

    def save_gain_and_trim(self):
        self.press_key("space")

    def toggle_autopilot(self):
        self.press_key("f")

    def emergency_stop(self):
        self.press_key("e")
