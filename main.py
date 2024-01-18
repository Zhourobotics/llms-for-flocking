from openai import OpenAI

import asyncio
import random
import json

from agents import *
import prompts

async def main():
    agents = []
    rounds = 10

    # we create our list of agents and add them to the list
    for i in range(3):
        # 1d --> 2d
        agents.append(Agent2D(i, [random.randint(0, 100), random.randint(0, 100)]))

    # todo: prettyprint!
    # todo: better err. handling
    for r in range(rounds):
        if not all(agent.pos == agents[0].pos for agent in agents):
            print("===ROUND {} ===".format(r))
            coroutines = []
            for agent in agents:
                # give our agent game description on the first round
                # and the updated text after that
                
                # two_dimensional -> one_dimensional for 1d arrays 
                message = prompts.two_dimensional.round_description if r > 0 else prompts.two_dimensional.game_description
                props = message.format(
                    agent.pos, "[{}]".format(
                        ", ".join(map(lambda a : str(a.pos), filter(lambda a: a.identifier != agent.identifier, agents)))
                        )
                )
                print("---------") # debug line
                print("AGENT", agent.identifier) # debug line

                # you guessed it (debug)
                print("Position: {}\nPeers: {}".format(agent.pos, "[{}]".format(", ".join(map(lambda a : str(a.pos), filter(lambda a: a.identifier != agent.identifier, agents))))))


                # ask agent where to move (coroutine)
                coroutines.append(agent.prompt(props + " " + prompts.agent_output_form))


                print(agent.latest) # debug line
                print("---------\n") # debug line



            try:
                # wait for coroutines to finish
                await asyncio.gather(*coroutines)
                # update each agents location!
                list(map(lambda agent: agent.update(), agents))
            except:
                print("Error in an agent's response format or failed to move agent!")
        else:
            print("Consensus reached on round {}", r - 1)


    for agent in agents:
        print("{}: {}".format(agent.identifier, agent.position_history))


if __name__ == '__main__':
    asyncio.run(main())