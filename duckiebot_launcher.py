#!/usr/bin/env python3
"""
Script to launch Duckiebot keyboard control.
Starts keyboard_control for duckiebot9.
Uses the default macOS Terminal application.
"""

import time
import subprocess
import sys

import pyautogui

DUCKIEBOT_NAME = "duckiebot9"
GAIN_STEP = 0.1


def run_keyboard_control():
    """
    Open a new Terminal window and run the keyboard_control command.
    """
    apple_script = f"""
    tell application "Terminal"
        activate
        do script "dts duckiebot keyboard_control {DUCKIEBOT_NAME} --browser"
    end tell
    """
    
    subprocess.run(["osascript", "-e", apple_script], check=True)
    print(f"\n✓ Keyboard control launched for {DUCKIEBOT_NAME}")
    print("  Browser should open with the controller interface")


def focus_controller_window():
    """
    Bring the controller browser window to the front by clicking in it.
    """
    time.sleep(3)
    screen_width, screen_height = pyautogui.size()
    pyautogui.click(screen_width // 2, screen_height // 2)
    time.sleep(0.5)


def set_gain(target_gain):
    """
    Adjust the keyboard controller gain to a target value.
    The controller changes gain in 0.1 increments with x/z.
    """
    current_gain = 0.0
    steps = round((target_gain - current_gain) / GAIN_STEP)

    if steps > 0:
        for _ in range(steps):
            pyautogui.press("x")
            time.sleep(0.15)
    elif steps < 0:
        for _ in range(abs(steps)):
            pyautogui.press("z")
            time.sleep(0.15)


def drive_forward(duration_seconds):
    """
    Hold W to drive forward for a fixed amount of time, then release.
    """
    pyautogui.keyDown("w")
    time.sleep(duration_seconds)
    pyautogui.keyUp("w")

def main():
    """Main execution flow."""
    print(f"🤖 Duckiebot Launcher - Searching for {DUCKIEBOT_NAME}")
    print("-" * 50)

    run_keyboard_control()
    focus_controller_window()
    set_gain(0.1)
    drive_forward(1)
    print("\n✨ Setup complete! Check the Terminal window for the controller.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
