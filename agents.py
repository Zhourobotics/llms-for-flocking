from openai import OpenAI

import asyncio
import json

import prompts
from keys import get_key


class Agent:
    identifier = ""
    latest = ""  # latest msg
    pos = None
    memory = []
    position_history = []

    def __init__(self, id, pos):
        self.identifier = id
        self.pos = pos
        self.position_history = [pos]
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
        self.memory.append(
            {
                "role": "system",
                "content": prompts.Flocking.agent_role
            }
        )

    async def prompt(self, message):
        self.memory.append({"role": "user", "content": message})
        completion = self.client.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=self.memory
        )
        self.memory.append(
            {"role": "assistant", "content": completion.choices[0].message.content}
        )
        self.latest = completion.choices[0].message.content

    def update(self):
        self.pos = json.loads(self.latest.split("\nPosition: ")[1])
        self.position_history.append(self.pos)

    def __str__(self):
        return "[{} Agent2D: (x: {}, y: {})]".format(
            self.identifier, self.pos[0], self.pos[1]
        )
