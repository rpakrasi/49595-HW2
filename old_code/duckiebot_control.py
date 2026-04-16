#!/usr/bin/env python3
"""Reusable Duckiebot terminal launch and keyboard control helpers."""

import subprocess
import time
import threading

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
        self._window_focused = False
        self._held_keys = set()  # Track currently held keys
        self._pulsing_keys = set()  # Track keys that should pulse
        self._pulse_threads = {}  # Track active pulse threads
        self._pulse_stop_event = threading.Event()  # Flag to stop pulsing

    def _ensure_controller_window_focus(self):
        if not self._window_focused:
            self.focus_controller_window()

    def focus_controller_window(self, wait_seconds=3):
        time.sleep(wait_seconds)
        screen_width, screen_height = pyautogui.size()
        pyautogui.click(screen_width // 2, screen_height // 2)
        time.sleep(0.5)
        self._window_focused = True

    def press_key(self, key_name, duration_seconds=0.15):
        self._ensure_controller_window_focus()
        pyautogui.press(key_name)
        time.sleep(duration_seconds)

    def set_gain(self, target_gain, current_gain=0.0):
        self._ensure_controller_window_focus()
        steps = round((target_gain - current_gain) / self.gain_step)

        if steps > 0:
            for _ in range(steps):
                pyautogui.press("x")
                time.sleep(0.15)
        elif steps < 0:
            for _ in range(abs(steps)):
                pyautogui.press("z")
                time.sleep(0.15)

    def _start_pulsing(self, key):
        """Start continuous pulsing of a key in a background thread."""
        def pulse():
            while key in self._pulsing_keys:
                pyautogui.press(key)
                time.sleep(0.15)
        
        thread = threading.Thread(target=pulse, daemon=True)
        thread.start()
        self._pulse_threads[key] = thread
        self._pulsing_keys.add(key)

    def _stop_pulsing(self, key):
        """Stop pulsing a specific key."""
        if key in self._pulsing_keys:
            self._pulsing_keys.discard(key)

    def _stop_all_pulsing(self):
        """Stop all pulsing keys."""
        self._pulsing_keys.clear()

    def turn_left(self, duration_seconds=None):
        self._ensure_controller_window_focus()
        if duration_seconds is None:
            # Continuous pulse mode
            if "a" not in self._pulsing_keys:
                self._start_pulsing("a")
        else:
            pyautogui.keyDown("a")
            time.sleep(duration_seconds)
            pyautogui.keyUp("a")

    def turn_right(self, duration_seconds=None):
        self._ensure_controller_window_focus()
        if duration_seconds is None:
            # Continuous pulse mode
            if "d" not in self._pulsing_keys:
                self._start_pulsing("d")
        else:
            pyautogui.keyDown("d")
            time.sleep(duration_seconds)
            pyautogui.keyUp("d")

    def drive_forward(self, duration_seconds=None):
        self._ensure_controller_window_focus()
        if duration_seconds is None:
            # Continuous hold mode
            pyautogui.keyDown("w")
            self._held_keys.add("w")
        else:
            pyautogui.keyDown("w")
            time.sleep(duration_seconds)
            pyautogui.keyUp("w")

    def drive_backward(self, duration_seconds=None):
        self._ensure_controller_window_focus()
        if duration_seconds is None:
            # Continuous hold mode
            pyautogui.keyDown("s")
            self._held_keys.add("s")
        else:
            pyautogui.keyDown("s")
            time.sleep(duration_seconds)
            pyautogui.keyUp("s")

    def release_forward(self):
        """Release the forward key if held."""
        if "w" in self._held_keys:
            pyautogui.keyUp("w")
            self._held_keys.discard("w")

    def release_backward(self):
        """Release the backward key if held."""
        if "s" in self._held_keys:
            pyautogui.keyUp("s")
            self._held_keys.discard("s")

    def release_left(self):
        """Release the left turn pulse if active."""
        self._stop_pulsing("a")

    def release_right(self):
        """Release the right turn pulse if active."""
        self._stop_pulsing("d")

    def release_all(self):
        """Release all currently held keys and pulsing keys."""
        for key in list(self._held_keys):
            pyautogui.keyUp(key)
        self._held_keys.clear()
        self._stop_all_pulsing()

    def increase_trim(self):
        self.press_key("v")

    def decrease_trim(self):
        self.press_key("c")

    def save_gain_and_trim(self):
        self.press_key("space")

    def toggle_autopilot(self):
        self.press_key("f")

    def emergency_stop(self):
        self.release_all()  # Release all held keys first
        self.press_key("e")