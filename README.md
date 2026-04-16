# 49595-HW2

## Project parts
- `duckiebot_launcher.py`: Main entrypoint with mode-based orchestration (`test` or `competition`).
- `duckiebot_controller_v2.py`: Reusable classes for launching Duckietown commands and sending keyboard actions.
- `speech_to_text_microsoft.py`: Azure Speech-to-Text listener that captures microphone utterances.
- `main.py`: Sends text prompts and convert them to duckiebot commands.
- `keys.py`: Stores API keys and endpoint configuration.

## How to run
### Step 1: Setting up the environment
1. Install the required dependencies.
2. Add the `keys.py` file from HW1 to this project directory.

### Step 2: Launching the voice command program

If you want the program to launch the keyboard control browser beforehand:
`python main.py --launch_keyboard`

If the keyboard browser is already open::
`python main.py`

### Step 3: Controlling the bot
Make sure the keyboard browser is focused, then speak commands like "move forward", "turn left", "stop", etc. The program will convert your speech to text, and then execute the corresponding keyboard actions to control the Duckiebot in the simulator.