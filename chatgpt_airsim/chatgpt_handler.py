import openai
import re
import argparse
import json


# Appends the user's prompt to the history and sends it to chatGPT
# Also sends the chat history to give it context
# Appends the response from chatGPT and returns the latest response to the user
def ask(prompt, chat_history):
    chat_history.append(
        {
            "role": "user",
            "content": prompt,
        }
    )
    # Currently set to gpt-3.5-turbo, but we can use gpt-4 and see how effective it is
    # temperature is set to 0, we can alter this potentially to see changes
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=chat_history,
        temperature=0
    )
    chat_history.append(
        {
            "role": "assistant",
            "content": completion.choices[0].message.content,
        }
    )
    return chat_history[-1]["content"]


# takes the generated response and extracts the block of code using the regex object
def extract_python_code(content, code_block_regex):
    code_blocks = code_block_regex.findall(content)
    if code_blocks:
        full_code = "\n".join(code_blocks)

        if full_code.startswith("python"):
            full_code = full_code[7:]

        return full_code
    else:
        return None


def initialize_chatgpt():
    # handles arguments when running the script
    # defaults the initial prompts to those in the following txt files
    parser = argparse.ArgumentParser()
    parser.add_argument("--prompt", type=str, default="prompts/airsim_basic.txt")
    parser.add_argument("--sysprompt", type=str, default="system_prompts/airsim_basic.txt")
    args = parser.parse_args()

    # loads the ChatGPT API Key
    with open("config.json", "r") as f:
        config = json.load(f)

    print("Initializing ChatGPT...")
    openai.api_key = config["OPENAI_API_KEY"]

    # Stores the sysprompt, most likely system_prompts/airsim_basic.txt
    with open(args.sysprompt, "r") as f:
        sysprompt = f.read()

    # list of chatGPT chat history, starting with the system prompt and then alternating with user and the chatgpt
    # assistant Example is given below
    chat_history = [
        {
            "role": "system",
            "content": sysprompt
        },
        {
            "role": "user",
            "content": "move the drones to the crowd of people"
        },
        {
            "role": "assistant",
            "content": """```python
    goalPos = aw.get_position('crowd')
    ```

    This code calls the aw.get_position() method and passes in 'crowd' to get the position of the crowd. Then it stores the output in goalPos which is used to calculate the goal velocity vector."""
        }
    ]

    # creates regex to find the code block within triple quotes
    code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)

    # reads the prompt specified by user, most likely prompts/airsim_basic.txt
    with open(args.prompt, "r") as f:
        prompt = f.read()

    # first asks the initial prompt, then starts the program for the user
    ask(prompt, chat_history)

    print("Done.")

    return chat_history, code_block_regex
