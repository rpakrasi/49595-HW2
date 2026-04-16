import subprocess
import time


class DuckiebotTerminalLauncher:
    """Launches Duckiebot commands in separate macOS Terminal windows."""

    def __init__(self, duckiebot_name="duckiebot9"):
        self.duckiebot_name = duckiebot_name

    def launch_all(self):
        self.__run_lane_following_demo()
        print("\nWaiting for lane-following demo to be fully ready...")
        try:
            input("Press Enter when lane-following is up ('GREEN'), then keyboard control will launch: ")
        except EOFError:
            # Fallback for non-interactive runs.
            time.sleep(8)
        self.__run_keyboard_control()

    def __run_terminal_command(self, command):
        apple_script = f"""
        tell application "Terminal"
            activate
            do script "{command}"
        end tell
        """
        subprocess.run(["osascript", "-e", apple_script], check=True)

    def __run_keyboard_control(self):
        command = f"dts duckiebot keyboard_control {self.duckiebot_name} --browser"
        self.__run_terminal_command(command)
        print(f"\n✓ Keyboard control launched for {self.duckiebot_name}")
        print("  Browser should open with the controller interface")

    def __run_lane_following_demo(self):
        command = (
            "dts duckiebot demo --demo_name lane-following "
            f"--duckiebot_name {self.duckiebot_name} --debug"
        )
        self.__run_terminal_command(command)
        print(f"\n✓ Lane-following demo launched for {self.duckiebot_name}")
