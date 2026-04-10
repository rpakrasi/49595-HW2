#!/usr/bin/env python3
"""
Script to launch Duckiebot keyboard control.
Starts keyboard_control for duckiebot9.
Uses the default macOS Terminal application by default, with a Windows mode
that runs the command inside Ubuntu/WSL.
"""

import argparse
import shutil
import subprocess
import sys

DUCKIEBOT_NAME = "duckiebot9"

def open_terminal_and_discover(windows_mode):
    """
    Open the platform terminal and start keyboard control.
    """
    command = f"dts duckiebot keyboard_control {DUCKIEBOT_NAME} --browser"

    if windows_mode:
        if sys.platform != "win32":
            print("❌ Windows mode was requested, but this script is not running on Windows.")
            return False

        wsl_command = ["wsl", "-d", "Ubuntu", "--", "bash", "-lc", command]

        if shutil.which("wt"):
            subprocess.Popen(["wt", "new-tab", "wsl", "-d", "Ubuntu", "--", "bash", "-lc", command])
        else:
            subprocess.Popen(wsl_command)
        print("✓ Windows terminal opened and keyboard control started in Ubuntu/WSL")
    else:
        apple_script = f"""
        tell application "Terminal"
            activate
            do script "{command}"
        end tell
        """

        subprocess.run(["osascript", "-e", apple_script], check=True)
        print("✓ Terminal opened and keyboard control started")

    return True

def parse_args():
    parser = argparse.ArgumentParser(description="Duckiebot discovery and keyboard control launcher")
    parser.add_argument(
        "--windows",
        action="store_true",
        help="Use Windows shell commands instead of macOS Terminal",
    )
    return parser.parse_args()


def main():
    """Main execution flow."""
    args = parse_args()
    windows_mode = args.windows

    print(f"🤖 Duckiebot Launcher - Searching for {DUCKIEBOT_NAME}")
    print("-" * 50)

    if not open_terminal_and_discover(windows_mode):
        return 1

    print("\n✨ Setup complete! Check the terminal window for the controller.")
    return 0

if __name__ == "__main__":
    sys.exit(main())
