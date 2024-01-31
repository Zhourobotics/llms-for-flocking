import argparse


def gen_parser():
    parser = argparse.ArgumentParser(description="Flocking LLM Simulation")
    parser.add_argument("--mode", "-m", choices=["run", "plot"], required=True,
                        help="Whether to 'run' the simulation, or to 'plot' a completed simulation")

    parser.add_argument("--name", "-n", type=str, required=True,
                        help="Unique name for this particular simulation")

    # For running
    parser.add_argument("--goal_x", "-gx", type=float, default=50.0,
                        help="Goal x position")
    parser.add_argument("--goal_y", "-gy", type=float, default=50.0,
                        help="Goal y position")
    # todo: add place agents can spawn in as args
    parser.add_argument("--shape", "-s", type=str, default="line",
                        help="Shape flock will attempt to form")
    parser.add_argument("--max_velocity", "-v", type=float, default=10.0,
                        help="Maximum velocity agents can travel per round")
    parser.add_argument("--safe_distance", "-d", type=float, default=2.0,
                        help="Minimum distance agents will try to keep from each other")
    parser.add_argument("--rounds", "-r", type=int, default=10,
                        help="Number of rounds for the simulation to run")
    parser.add_argument("--agents", "-a", type=int, default=5,
                        help="Number of agents in the simulation")
    parser.add_argument("--memory", type=int, default=6,
                        help="Message history each agent remembers")
    parser.add_argument("--model", type=str, default="gpt-3.5-turbo-0613",  # gpt-4-1106-preview
                        help="Message history each agent remembers")
    # For plotting
    parser.add_argument("--follow_agents", action="store_true",
                        help="If the plot should adjust the dataview based on agent positions")
    parser.add_argument("--x_min", type=int, default=-20,
                        help="Left-side bound of plot")
    parser.add_argument("--x_max", type=int, default=130,
                        help="Right-side bound of plot")
    parser.add_argument("--x_ticks", type=int, default=10,
                        help="How many ticks to count up by on the plots x-axis")
    parser.add_argument("--y_min", type=int, default=0,
                        help="Lower bound of plot")
    parser.add_argument("--y_max", type=int, default=100,
                        help="Upper bound of plot")
    return parser
