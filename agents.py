from openai import OpenAI

import re
import json
import prompts

from keys import get_key

pattern = r'\[.*?\]'

class Agent:
    identifier = ""
    latest = ""
    position = None
    memory = [{"role": "system", "content": prompts.Utility.agent_role}]
    position_history = []
    active = True

    def __init__(self, identifier, position, active=True):
        self.identifier = identifier
        self.position = position
        self.position_history = [position]
        self.client = OpenAI(api_key=get_key())
        self.active = active

    async def prompt(self, message, model, memory_limit):
        self.memory.append({"role": "user", "content": message})

        if self.active:
            # avoid running into a token limit, get the first two
            # prompts (context, and description) and last few prompts as specified in the arguments (latest pos history)
            summarized_history = self.memory
            if len(summarized_history) > 2 + memory_limit:
                summarized_history = self.memory[:2] + self.memory[-memory_limit:]

            completion = self.client.chat.completions.create(model=model, messages=summarized_history)

            self.memory.append({"role": "assistant", "content": completion.choices[0].message.content})
            self.latest = completion.choices[0].message.content

        else:  # zombie agent
            invented = "Reasoning: STATIC AGENT\nPosition: {}".format(self.position)  # formatting an array already adds the brackets oops
            self.memory.append({"role": "assistant", "content": invented})
            self.latest = invented

    def update(self):
        # let's account for weird formatting
        # we need to find the position coordinates, and take the last one in case the
        # llm just doing calculations
        # "Position: [1+1, 2+2] = [4, 4] (this is the position)"
        #                         ^^^^^^ what we are interested in
        exact_position = json.loads(re.findall(pattern, self.latest.split("\nPosition: ")[1])[-1])
        self.position = [  # round position to two decimal places
            round(exact_position[0], 2),
            round(exact_position[1], 2)
        ]
        self.position_history.append(self.position)

    def __str__(self):
        return "[{} Agent2D: (x: {}, y: {})]".format(self.identifier, self.position[0], self.position[1])
