import time

# ~/venv/bin/pip install openai
import openai

import keys
import speech_to_text_microsoft


done = False
written = True
client = openai.AzureOpenAI(azure_endpoint=keys.azure_openai_endpoint,
                            api_key=keys.azure_openai_key,
                            api_version=keys.azure_openai_api_version)
discourse = [{"role": "system",
              "content":
                  "I am an instructor of the Purdue experimental undergraduate course in Electrical and Computer Engineering on Natural Language Processing"}]


def gpt(request):
    discourse.append({"role": "user", "content": request})
    chat = client.chat.completions.create(
        messages=discourse, model="gpt-4")
    reply = chat.choices[0].message.content
    discourse.append({"role": "assistant", "content": reply})
    return reply



def process_utterance(said):
    global done
    print("Processing utterance: ...")
    if written:
        print(said)
    if "bye" in said:
        done = True
    else:
        response = gpt(said)
        print(response)


speech_to_text_microsoft.process_utterance = process_utterance

speech_to_text_microsoft.start()
while not done:
    time.sleep(0.1)

speech_to_text_microsoft.stop()
