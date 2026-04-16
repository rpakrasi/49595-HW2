import argparse
import signal
import time

import speech_to_text_microsoft
from duckiebot_controller_v2 import DuckiebotKeyboardControllerV2
from terminal_launchers import DuckiebotTerminalLauncher

gain = 0.1
controller = DuckiebotKeyboardControllerV2(gain=gain)
done = False


def execute_intent(intent: str):
    intent = intent.lower()
    if "stop" in intent:
        controller.emergency_stop()
    elif "autopilot" in intent or "auto pilot" in intent:
        controller.toggle_autopilot()
    elif "left short" in intent:
        controller.turn_left(0.45)
    elif "right short" in intent:
        controller.turn_right(0.45)
    elif "left long" in intent:
        controller.turn_left(0.9)
    elif "right long" in intent:
        controller.turn_right(0.9)
    elif "straight" in intent or "forward" in intent:
        controller.drive_forward()
    elif "backward" in intent:
        controller.drive_backward()
    elif "turn left" in intent:
        controller.turn_and_keep_moving("a")
    elif "turn right" in intent:
        controller.turn_and_keep_moving("d")
    elif "left circle" in intent:
        controller.circle("a")
    elif "right circle" in intent:
        controller.circle("d")
    elif "left" in intent:
        controller.turn_tiny("a")
    elif "right" in intent:
        controller.turn_tiny("d")
    elif "super speed" in intent:
        controller.set_gain(2)
    elif "fastest" in intent:
        controller.set_gain(1.6)
    elif "faster" in intent:
        controller.set_gain(1.3)
    elif "fast" in intent:
        controller.set_gain(1)
    elif "slowest" in intent:
        controller.set_gain(0.1)
    elif "slower" in intent:
        controller.set_gain(0.3)
    elif "slow" in intent:
        controller.set_gain(0.6)


def process_utterance(said):
    global done
    print("Processing utterance: ", said)
    if "bye" in said.lower() or "exit" in said.lower():
        done = True
    else:
        execute_intent(said)


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="Duckiebot Voice Controller")
    parser.add_argument(
        "--launch_keyboard",
        action="store_true",
        help="Launch the keyboard control interface before starting voice control",
    )
    return parser.parse_args(argv)


def main():
    global done
    done = False

    args = parse_args()

    if args.launch_keyboard:
        launcher = DuckiebotTerminalLauncher()
        launcher.launch_all()

    def signal_handler(sig, frame):
        global done
        done = True

    signal.signal(signal.SIGINT, signal_handler)

    print(f"Starting. Gain set to: {gain}")

    try:
        speech_to_text_microsoft.process_utterance = process_utterance
        speech_to_text_microsoft.start()

        while not done:
            time.sleep(0.05)

    except Exception as e:
        print(f"An unexpected error occurred: {e}")
    finally:
        speech_to_text_microsoft.stop()


if __name__ == "__main__":
    main()
