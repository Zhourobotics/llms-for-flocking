import asyncio
import random
import time

from agents import *
from graph import *
import prompts

from data import Data
from arguments import gen_parser


async def main():
    parser = gen_parser()
    args = parser.parse_args()

    if args.mode == "run":
        # todo: check if args.name doesnt exist
        # create our list of agents
        agents = []

        # ...and add them to the list
        for i in range(args.agents):
            agents.append(FlockingAgent(i, [
                round(random.uniform(args.spawn_x_min, args.spawn_x_max), 2),
                round(random.uniform(args.spawn_y_min, args.spawn_y_max), 2),
            ]))

        # todo: prettyprint!
        # todo: better err. handling

        for r in range(args.rounds):
            print("===ROUND {}/{} ===".format(r, args.rounds))
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
                coroutines.append(agent.prompt(message + " " + prompts.Flocking.output_format, args.model, args.memory_limit))

                print(agent.latest)  # debug line
                print("---------\n")  # debug line

            try:
                # wait for coroutines to finish
                await asyncio.gather(*coroutines)
                # update each agent's location!
                list(map(lambda agent: agent.update(), agents))

            except Exception as e:
                print(f"Error: {e}. Error in an agent's response format or failed to move agent!")

            time_lapse = time.time() - tick
            print(f"Time for this round is {time_lapse:.2f}")

        for agent in agents:
            print("{}: {}".format(agent.identifier, agent.position_history))

        # Save Data
        Data.save(agents, args, identifier=args.name)

    # Animate Final Graph
    # todo: err handling, make sure args.name exists!
    Graph.plot_animated(Data.load(args))

if __name__ == "__main__":
    asyncio.run(main())
