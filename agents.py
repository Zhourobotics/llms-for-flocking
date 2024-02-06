from openai import OpenAI

import json
import prompts

from keys import get_key


class FlockingAgent:
    identifier = ""
    latest = ""
    position = None
    memory = [{"role": "system", "content": prompts.Flocking.agent_role}]
    position_history = []

    def __init__(self, identifier, position):
        self.identifier = identifier
        self.position = position
        self.position_history = [position]
        self.client = OpenAI(api_key=get_key())

    async def prompt(self, message, model, memory_limit):
        self.memory.append({"role": "user", "content": message})

        # avoid running into a token limit, get the first two
        # prompts (context, and description) and last few prompts as specified in the arguments (latest pos history)
        summarized_history = self.memory
        if len(summarized_history) > 2 + memory_limit:
            summarized_history = self.memory[:2] + self.memory[-memory_limit:]
        print(summarized_history)
        completion = self.client.chat.completions.create(model=model, messages=summarized_history)

        self.memory.append({"role": "assistant", "content": completion.choices[0].message.content})
        self.latest = completion.choices[0].message.content

    def update(self):
        exact_position = json.loads(self.latest.split("\nPosition: ")[1])
        self.position = [  # round position to two decimal places
            round(exact_position[0], 2),
            round(exact_position[1], 2)
        ]
        self.position_history.append(self.position)

    def __str__(self):
        return "[{} Agent2D: (x: {}, y: {})]".format(self.identifier, self.position[0], self.position[1])
