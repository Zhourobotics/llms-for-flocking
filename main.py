from openai import OpenAI

import asyncio
import random
import json
import time

from agents import *
import prompts
from plot_result import *

GOAL = [95, 95]
PATTERN = "line"
MAX_V = 5
EPS = 1


async def main():
    agents = []
    rounds = 6

    # we create our list of agents and add them to the list
    for i in range(3):
        # 1d --> 2d
        agents.append(Agent2D_flock(i, [random.randint(0, 10), random.randint(0, 10)]))

    # todo: prettyprint!
    # todo: better err. handling
    for r in range(rounds):
        tic = time.time()
        if not all(agent.pos == agents[0].pos for agent in agents):
            print("===ROUND {} ===".format(r))
            coroutines = []
            for agent in agents:
                # give our agent game description on the first round
                # and the updated text after that

                # two_dimensional -> one_dimensional for 1d arrays
                # message = (
                #     prompts.two_dimensional.round_description
                #     if r > 0
                #     else prompts.two_dimensional.game_description
                # )
                # props = message.format(
                #     agent.pos,
                #     "[{}]".format(
                #         ", ".join(
                #             map(
                #                 lambda a: str(a.pos),
                #                 filter(
                #                     lambda a: a.identifier != agent.identifier, agents
                #                 ),
                #             )
                #         )
                #     ),
                # )

                message = (
                    prompts.flocking_2D.round_description
                    if r > 0
                    else prompts.flocking_2D.game_description
                )
                props = message.format(
                    agent.pos,
                    "[{}]".format(
                        ", ".join(
                            map(
                                lambda a: str(a.pos),
                                filter(
                                    lambda a: a.identifier != agent.identifier, agents
                                ),
                            )
                        )
                    ),
                    GOAL,
                    MAX_V,
                    PATTERN,
                    EPS,
                )

                print("---------")  # debug line
                print("AGENT", agent.identifier)  # debug line

                # you guessed it (debug)
                print(
                    "Position: {}\nPeers: {}".format(
                        agent.pos,
                        "[{}]".format(
                            ", ".join(
                                map(
                                    lambda a: str(a.pos),
                                    filter(
                                        lambda a: a.identifier != agent.identifier,
                                        agents,
                                    ),
                                )
                            )
                        ),
                    )
                )

                # ask agent where to move (coroutine)
                coroutines.append(agent.prompt(props + " " + prompts.agent_output_form))

                print(agent.latest)  # debug line
                print("---------\n")  # debug line

            try:
                # wait for coroutines to finish
                await asyncio.gather(*coroutines)
                # update each agents location!
                list(map(lambda agent: agent.update(), agents))
            except:
                print("Error in an agent's response format or failed to move agent!")
        else:
            print(f"Consensus reached on round {r - 1}")
        time_lapse = time.time() - tic
        print(f"Time for this round is {time_lapse:.2f}")

    for agent in agents:
        print("{}: {}".format(agent.identifier, agent.position_history))

    plot_result(agents).plot_fig()


if __name__ == "__main__":
    asyncio.run(main())
