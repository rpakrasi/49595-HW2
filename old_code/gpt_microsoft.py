import argparse
import json
import time

# ~/venv/bin/pip install openai
import openai

from duckiebot_control import DuckiebotKeyboardController, DuckiebotTerminalLauncher
from duckiebot_launcher import (
    DUCKIEBOT_NAME,
    GAIN_STEP,
    MODE_COMPETITION,
    MODE_TEST,
    run_mode,
)
import keys
import speech_to_text_microsoft


done = False
written = True

client = openai.AzureOpenAI(azure_endpoint=keys.azure_openai_endpoint,
                            api_key=keys.azure_openai_key,
                            api_version=keys.azure_openai_api_version)
launcher = DuckiebotTerminalLauncher(DUCKIEBOT_NAME)
controller = DuckiebotKeyboardController(gain_step=GAIN_STEP)

INTENT_SYSTEM_PROMPT = """You map user voice commands to one Duckiebot action.
Return ONLY valid JSON with this schema:
{"action": string, "duration": number|null, "target_gain": number|null}

Allowed actions:
- toggle_autopilot
- emergency_stop
- drive_forward (continuous until release_forward)
- drive_backward (continuous until release_backward)
- turn_left (continuous until release_left)
- turn_right (continuous until release_right)
- release_forward
- release_backward
- release_left
- release_right
- increase_trim
- decrease_trim
- save_gain_and_trim
- set_gain
- none

Rules:
- For drive/turn: use duration=null to start continuous motion, use release_* actions to stop.
- Use target_gain only for set_gain.
- "go forward" = drive_forward with duration:null.
- "stop" = release_forward, release_backward, release_left, release_right as appropriate.
- If unsure, return {"action":"none","duration":null,"target_gain":null}.
"""


def gpt_intent(request):
    chat = client.chat.completions.create(
        model="gpt-4",
        temperature=0,
        messages=[
            {"role": "system", "content": INTENT_SYSTEM_PROMPT},
            {"role": "user", "content": request},
        ],
    )
    return chat.choices[0].message.content


def parse_intent(raw_response):
    try:
        return json.loads(raw_response)
    except Exception:
        start = raw_response.find("{")
        end = raw_response.rfind("}")
        if start != -1 and end != -1 and end > start:
            try:
                return json.loads(raw_response[start:end + 1])
            except Exception:
                pass
    return {"action": "none", "duration": None, "target_gain": None}


def execute_intent(intent):
    action = intent.get("action", "none")
    duration = intent.get("duration")
    target_gain = intent.get("target_gain")

    if action == "toggle_autopilot":
        controller.toggle_autopilot()
    elif action == "emergency_stop":
        controller.emergency_stop()
    elif action == "drive_forward":
        controller.drive_forward(duration)  # None for continuous, float for duration
    elif action == "drive_backward":
        controller.drive_backward(duration)
    elif action == "turn_left":
        controller.turn_left(duration)
    elif action == "turn_right":
        controller.turn_right(duration)
    elif action == "release_forward":
        controller.release_forward()
    elif action == "release_backward":
        controller.release_backward()
    elif action == "release_left":
        controller.release_left()
    elif action == "release_right":
        controller.release_right()
    elif action == "increase_trim":
        controller.increase_trim()
    elif action == "decrease_trim":
        controller.decrease_trim()
    elif action == "save_gain_and_trim":
        controller.save_gain_and_trim()
    elif action == "set_gain" and target_gain is not None:
        controller.set_gain(float(target_gain))

    return action



def process_utterance(said):
    global done
    print("Processing utterance: ...")
    if written:
        print(said)
    if "bye" in said.lower() or "exit" in said.lower():
        done = True
    else:
        raw_intent = gpt_intent(said)
        intent = parse_intent(raw_intent)
        action = execute_intent(intent)
        print(f"Action: {action}")


def parse_args(argv=None):
    parser = argparse.ArgumentParser(description="GPT voice dispatcher")
    parser.add_argument(
        "--mode",
        choices=[MODE_TEST, MODE_COMPETITION],
        default=MODE_TEST,
        help="Startup mode before voice dispatch",
    )
    return parser.parse_args(argv)


def main(argv=None):
    global done
    args = parse_args(argv)

    # Reuse launcher orchestration to keep one source of truth for setup.
    run_mode(args.mode, launcher, controller)

    speech_to_text_microsoft.process_utterance = process_utterance
    speech_to_text_microsoft.start()
    while not done:
        time.sleep(0.1)
    speech_to_text_microsoft.stop()


if __name__ == "__main__":
    main()
