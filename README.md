# 49595-HW2

## Project parts
- `duckiebot_launcher.py`: Main entrypoint with mode-based orchestration (`test` or `competition`).
- `duckiebot_control.py`: Reusable classes for launching Duckietown commands and sending keyboard actions.
- `speech_to_text_microsoft.py`: Azure Speech-to-Text listener that captures microphone utterances.
- `gpt_microsoft.py`: Sends text prompts to the model and handles model responses.
- `keys.py`: Stores API keys and endpoint configuration.

## Use this for test mode:
`python gpt_microsoft.py --mode test`

## Use this for competition mode later:
`python gpt_microsoft.py --mode competition`