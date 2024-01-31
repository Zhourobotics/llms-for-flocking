import asyncio
import random
import time
import os

from agents import FlockingAgent
from graph import Graph
from data import Data

from arguments import gen_parser
import prompts


async def main():
    parser = gen_parser()
    args = parser.parse_args()

    if args.mode == "run":
        if not os.path.isfile(f'./results/{args.name}/results'):
            # create our list of agents
            agents = []

            # ...and add them to the list
            for i in range(args.agents):
                agents.append(FlockingAgent(i, [
                    round(random.uniform(args.spawn_x_min, args.spawn_x_max), 2),
                    round(random.uniform(args.spawn_y_min, args.spawn_y_max), 2),
                ]))

            for r in range(args.rounds):
                print("======ROUND {}/{}======".format(r + 1, args.rounds))
                coroutines = []
                tick = time.time()

                for agent in agents:
                    other_agent_positions = "{}".format(", ".join(
                        map(lambda a: str(a.position), filter(lambda a: a.identifier != agent.identifier, agents))))

                    if r > 0:
                        message = prompts.Flocking.get_round_description(
                            agent.position,
                            other_agent_positions,
                            [args.goal_x, args.goal_y],
                        )
                    else:
                        message = prompts.Flocking.get_game_description(
                            agent.position,
                            other_agent_positions,
                            [args.goal_x, args.goal_y],
                            args.max_velocity,
                            args.shape,
                            args.safe_distance
                        )

                    # ask agent where to move (coroutine)
                    coroutines.append(
                        agent.prompt(message + " " + prompts.Flocking.output_format, args.model, args.memory_limit))

                    print("------------------------------------")
                    print("AGENT", agent.identifier + 1)
                    print(agent.latest)  # print out reasoning (this includes the position)
                    print("Peers: {}".format("[{}]".format(other_agent_positions)))
                    print("------------------------------------\n")

                try:
                    # wait for coroutines to finish
                    await asyncio.gather(*coroutines)
                    # update each agent's location!
                    list(map(lambda a: a.update(), agents))

                except Exception as e:
                    print(f"Error: {e}. Error in an agent's response format or failed to move agent!")

                time_lapse = time.time() - tick
                print(f"Time for this round is {time_lapse:.2f}")
                print("\n\n\n")

            print("Drone Positions:")
            for agent in agents:
                print("{}: {}".format(agent.identifier, agent.position_history))
            print("\n")

            # Save Data
            Data.save(agents, args, identifier=args.name)
        else:
            print(f'Error: Test {args.name} already exists!')

    # Animate Final Graph
    if os.path.isfile(f'./results/{args.name}/results'):
        Graph.plot_animated(Data.load(args))
    else:
        print(f'Error: Test {args.name} does not exist!')


if __name__ == "__main__":
    asyncio.run(main())
