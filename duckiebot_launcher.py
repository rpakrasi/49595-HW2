#!/usr/bin/env python3
"""
Script to launch Duckiebot keyboard control.
Starts keyboard_control for duckiebot9.
Uses the default macOS Terminal application.
"""

import subprocess
import sys

DUCKIEBOT_NAME = "duckiebot9"

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

def main():
    """Main execution flow."""
    print(f"🤖 Duckiebot Launcher - Searching for {DUCKIEBOT_NAME}")
    print("-" * 50)

    run_keyboard_control()
    print("\n✨ Setup complete! Check the Terminal window for the controller.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
