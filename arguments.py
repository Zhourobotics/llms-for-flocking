import argparse


def parse_cli_arguments():
    parser = argparse.ArgumentParser(description="Flocking Agents Simulation")
    parser.add_argument("--mode", "-m", choices=["run", "plot"], required=True,
                        help="Whether to 'run' the simulation, or to 'plot' a completed simulation")

    parser.add_argument("--name", "-n", type=str, required=True,
                        help="Unique name for this particular simulation")

    parser.add_argument("--prompt", "-p", type=str,
                        help="LLM prompt. Formats first {} to agent position and second {} to peer positions.")

    parser.add_argument("--round_description", "-r", type=str,
                        help="LLM round description. Formats first {} to agent position and second {} to peer positions.")

    # For running
    parser.add_argument("--seed", "-s", type=int, default=42,
                        help="Random seed")

    parser.add_argument("--spawn_x_min", "-sxmi", type=float, default=1.0,
                        help="Lower bound of the agent's random spawn range's x coordinate")
    parser.add_argument("--spawn_x_max", "-sxma", type=float, default=20.0,
                        help="Upper bound of the agent's random spawn range's x coordinate")

    parser.add_argument("--spawn_y_min", "-symi", type=float, default=1.0,
                        help="Lower bound of the agent's random spawn range's y coordinate")
    parser.add_argument("--spawn_y_max", "-syma", type=float, default=20.0,
                        help="Upper bound of the agent's random spawn range's y coordinate")

    parser.add_argument("--rounds", "-t", type=int, default=10,
                        help="Number of rounds for the simulation to run")
    parser.add_argument("--zombies", "-z", type=int, default=0,
                        help="The number of inactive agents in the simulation")
    parser.add_argument("--agents", "-a", type=int, default=5,
                        help="Number of agents in the simulation")
    parser.add_argument("--memory_limit", "-mlim", type=int, default=6,
                        help="Message history each agent remembers")
    parser.add_argument("--model", "-gpt", type=str, default="gpt-3.5-turbo-0613",  # gpt-4-1106-preview
                        help="Message history each agent remembers")
    # For plotting
    parser.add_argument("--x_min", "-pxmi", type=int, default=-20,
                        help="Left-side bound of plot")
    parser.add_argument("--x_max", "-pxma", type=int, default=130,
                        help="Right-side bound of plot")
    parser.add_argument("--x_ticks", "-pxmt", type=int, default=10,
                        help="How many ticks to count up by on the plots x-axis")
    parser.add_argument("--y_min", "-pymi", type=int, default=0,
                        help="Lower bound of plot")
    parser.add_argument("--y_max", "-pyma", type=int, default=100,
                        help="Upper bound of plot")

    args = parser.parse_args()

    if (args.mode == "run") and (args.prompt is None or args.round_description is None):
        parser.error("'Run' mode requires --prompt and --round_description arguments.")

    return args
