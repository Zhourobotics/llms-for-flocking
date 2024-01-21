from openai import OpenAI

import asyncio
import random
import time
import json

from agents import *
import prompts
from plot_result import *


async def main():
    # loading configuration for test
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    test_id =       config["test_id"]
    goal_position = config["goal_position"]
    flock_shape =   config["flock_shape"]
    max_velocity =  config["max_velocity"]
    safe_distance = config["safe_distance"]
    rounds =        config["rounds"]
    
    agents = []


    # we create our list of agents and add them to the list
    for i in range(3):
        agents.append(FlockingAgent(i, [random.randint(0, 10), random.randint(0, 10)]))

    # todo: prettyprint!
    # todo: better err. handling
    # todo: saving result - Peihan
    for r in range(rounds):
        tick = time.time()
        if not all(agent.position == agents[0].position for agent in agents):
            print("===ROUND {} ===".format(r))
            coroutines = []
            for agent in agents:

                other_agent_positions = "{}".format(", ".join(
                    map(lambda a: str(a.position), filter(lambda a: a.identifier != agent.identifier, agents))))

                if r > 0:
                    message = prompts.Flocking.get_round_description(
                        agent.position,
                        other_agent_positions,
                        goal_position
                    )
                else:
                    message = prompts.Flocking.get_game_description(
                        agent.position,
                        other_agent_positions,
                        goal_position,
                        max_velocity,
                        flock_shape,
                        safe_distance
                    )

                print("---------")  # debug line
                print("AGENT", agent.identifier)  # debug line

                # you guessed it (debug)
                print(
                    "Position: {}\nPeers: {}".format(
                        agent.position,
                        "[{}]".format(other_agent_positions),
                    )
                )

                # ask agent where to move (coroutine)
                coroutines.append(agent.prompt(message + " " + prompts.Flocking.output_form))

                print(agent.latest)  # debug line
                print("---------\n")  # debug line

            try:
                # wait for coroutines to finish
                await asyncio.gather(*coroutines)
                # update each agent's location!
                list(map(lambda agent: agent.update(), agents))
            except:
                print("Error in an agent's response format or failed to move agent!")
        else:
            print(f"Consensus reached on round {r - 1}")
        time_lapse = time.time() - tick
        print(f"Time for this round is {time_lapse:.2f}")

    for agent in agents:
        print("{}: {}".format(agent.identifier, agent.position_history))

    plot_result(agents).plot_fig()


if __name__ == "__main__":
    asyncio.run(main())
