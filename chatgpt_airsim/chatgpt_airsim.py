import openai
import re
import argparse
from airsim_wrapper import *
import math
import numpy as np
import os
import json
import time
from pynput import keyboard

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

# list of chatGPT chat history, starting with the system prompt and then alternating with user and the chatgpt assistant
# Example is given below
chat_history = [
    {
        "role": "system",
        "content": sysprompt
    },
    {
        "role": "user",
        "content": "move 10 units up"
    },
    {
        "role": "assistant",
        "content": """```python
aw.fly_to([aw.get_drone_position()[0], aw.get_drone_position()[1], aw.get_drone_position()[2]+10])
```

This code uses the `fly_to()` function to move the drone to a new position that is 10 units up from the current position. It does this by getting the current position of the drone using `get_drone_position()` and then creating a new list with the same X and Y coordinates, but with the Z coordinate increased by 10. The drone will then fly to this new position using `fly_to()`."""
    }
]


# Appends the user's prompt to the history and sends it to chatGPT
# Also sends the chat history to give it context
# Appends the response from chatGPT and returns the latest response to the user
def ask(prompt):
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


print(f"Done.")

# creates regex to find the code block within triple quotes
code_block_regex = re.compile(r"```(.*?)```", re.DOTALL)


# takes the generated response and extracts the block of code using the regex object
def extract_python_code(content):
    code_blocks = code_block_regex.findall(content)
    if code_blocks:
        full_code = "\n".join(code_blocks)

        if full_code.startswith("python"):
            full_code = full_code[7:]

        return full_code
    else:
        return None


# class attributes for ANSI escape sequences for colors
# essentially just changes the color of the terminal for the user
class colors:  # You may need to change color settings
    RED = "\033[31m"
    ENDC = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


# obtain list of drones
with open('settings.json', 'r') as file:
    settings = json.load(file)

# Initialize an empty list for drone names
drone_names = []

# Iterate through each vehicle in the "Vehicles" section
for vehicle_name, attributes in settings.get("Vehicles", {}).items():
    # Check if the vehicle type is "SimpleFlight" or "PhysXCar"
    if attributes.get("VehicleType") == "SimpleFlight":
        # Add drone name
        drone_names.append(vehicle_name)

# Initializes the AirSim Wrapper with the drones in environment
print(f"Initializing AirSim...")
aw = AirSimWrapper(drone_names)
aw.start_keyboard_listener()
print(f"Done.")

# reads the prompt specified by user, most likely prompts/airsim_basic.txt
with open(args.prompt, "r") as f:
    prompt = f.read()

# first asks the initial prompt, then starts the program for the user
ask(prompt)
print("Welcome to the AirSim chatbot! I am ready to help you with your AirSim questions and commands.")

# infinite loop for user commands
while True:
    # user input prompts are denoted as yellow
    question = input(colors.YELLOW + "AirSim> " + colors.ENDC)

    # use !quit or !exit to stop the program
    if question == "!quit" or question == "!exit":
        break

    # use !clear to clear the terminal
    if question == "!clear":
        os.system("cls")
        continue

    # obtain the response from ChatGPT after asking the user input
    response = ask(question)

    # prints the response
    print(f"\n{response}\n")

    # extracts python code, checks if it exists, and executes it until finished
    code = extract_python_code(response)
    if code is not None:
        print("Please wait while I run the code in AirSim...")
        exec(extract_python_code(response))
        print("Done!\n")