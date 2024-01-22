from openai import OpenAI

import json

import prompts
from keys import get_key

class Agent:
    identifier = ""
    latest = ""
    position = None
    memory = []
    position_history = []

    def __init__(self, identifier, position):
        self.identifier = identifier
        self.position = position
        self.position_history = [position]
        self.client = OpenAI(api_key=get_key())

        self.define_system()

    def define_system(self):
        pass

    async def prompt(self, message):
        pass

    def update(self):
        pass

    def __str__(self):
        return "[Abstract Agent]"


class FlockingAgent(Agent):
    def define_system(self):
        self.memory.append({"role": "system", "content": prompts.Flocking.agent_role})

    async def prompt(self, message):
        with open('config.json', 'r') as json_file:
            config = json.load(json_file)

        self.memory.append({"role": "user", "content": message})

        completion = self.client.chat.completions.create(model=config["model"], messages=self.memory)
        self.memory.append({"role": "assistant", "content": completion.choices[0].message.content})
        self.latest = completion.choices[0].message.content

    def update(self):
        self.position = json.loads(self.latest.split("\nPosition: ")[1])
        self.position_history.append(self.position)

    def __str__(self):
        return "[{} Agent2D: (x: {}, y: {})]".format(self.identifier, self.position[0], self.position[1])
