from openai import OpenAI

import asyncio
import random
import time

from agents import *
from graph import *
import prompts

from data import Data


async def main():
    with open('config.json', 'r') as json_file:
        config = json.load(json_file)

    agents = []

    # we create our list of agents and add them to the list
    for i in range(config["agents"]):
        agents.append(FlockingAgent(i, [
            round(random.uniform(1.0, 10.0), 2),
            round(random.uniform(1.0, 10.0), 2),
        ]))

    # todo: prettyprint!
    # todo: better err. handling

    for r in range(config["rounds"]):
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
                        [float(config["goal"][0]), float(config["goal"][1])],
                    )
                else:
                    message = prompts.Flocking.get_game_description(
                        agent.position,
                        other_agent_positions,
                        [float(config["goal"][0]), float(config["goal"][1])],
                        float(config["max_velocity"]),
                        config["flock_shape"],
                        float(config["safe_distance"])
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
                coroutines.append(agent.prompt(message + " " + prompts.Flocking.output_format))

                print(agent.latest)  # debug line
                print("---------\n")  # debug line

            try:
                # wait for coroutines to finish
                await asyncio.gather(*coroutines)
                # update each agent's location!
                list(map(lambda agent: agent.update(), agents))

            except Exception as e:
                print(f"Error: {e}. Error in an agent's response format or failed to move agent!")
        else:
            print(f"Consensus reached on round {r - 1}")
        time_lapse = time.time() - tick
        print(f"Time for this round is {time_lapse:.2f}")

    for agent in agents:
        print("{}: {}".format(agent.identifier, agent.position_history))

    # Save Data
    results = Data.save(agents, config)

    # Animate Final Graph
    Graph.plot_animated(Data.load(results))

if __name__ == "__main__":
    asyncio.run(main())
