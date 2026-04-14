#!/usr/bin/env python3
"""
Script to launch Duckiebot keyboard control.
Starts keyboard_control for duckiebot9.
Uses the default macOS Terminal application.
"""

import argparse
import time
import sys

from duckiebot_control import DuckiebotKeyboardController, DuckiebotTerminalLauncher

DUCKIEBOT_NAME = "duckiebot9"
GAIN_STEP = 0.1
MODE_TEST = "test"
MODE_COMPETITION = "competition"


def run_test_mode(launcher, controller):
    """Current scripted testing flow."""
    print(f"🤖 Duckiebot Launcher - Searching for {DUCKIEBOT_NAME}")
    print("-" * 50)

    launcher.run_keyboard_control()
    controller.focus_controller_window()
    print("\n✨ Setup complete! Check the Terminal window for the controller.")


def run_competition_mode(launcher, controller):
    """Competition flow with lane-following enabled by default."""
    print(f"🏁 Competition mode for {DUCKIEBOT_NAME}")
    print("-" * 50)

    launcher.run_lane_following_demo()
    print("\nWaiting for lane-following demo to be fully ready...")
    try:
        input("Press Enter when lane-following is up, then keyboard control will launch: ")
    except EOFError:
        # Fallback for non-interactive runs.
        time.sleep(8)
    launcher.run_keyboard_control()
    controller.focus_controller_window()
    controller.toggle_autopilot()
    print("\n✨ Lane following enabled. Voice start/stop can now toggle autopilot.")


def run_mode(mode, launcher, controller):
    """Run the requested launcher mode with shared orchestration logic."""
    if mode == MODE_COMPETITION:
        run_competition_mode(launcher, controller)
    else:
        run_test_mode(launcher, controller)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Duckiebot launcher")
    parser.add_argument(
        "--mode",
        choices=[MODE_TEST, MODE_COMPETITION],
        default=MODE_TEST,
        help="Run mode: test or competition",
    )
    return parser.parse_args(argv)


def main(argv=None):
    """Main execution flow."""
    args = parse_args(argv)
    launcher = DuckiebotTerminalLauncher(DUCKIEBOT_NAME)
    controller = DuckiebotKeyboardController(gain_step=GAIN_STEP)

    run_mode(args.mode, launcher, controller)

    return 0


if __name__ == "__main__":
    sys.exit(main())
