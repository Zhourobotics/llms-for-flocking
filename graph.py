import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation
from matplotlib.patches import FancyArrowPatch

# pycharm animation support
matplotlib.use("TkAgg")


class Graph:
    colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'brown', 'black']

    @staticmethod
    def plot_agents(agents):
        # Create a figure and axis
        fig, ax = plt.subplots()

        for idx, agent in enumerate(agents):
            color = Graph.colors[idx % len(Graph.colors)]

            # Plot each segment with an arrow
            for i in range(len(agent.position_history) - 1):
                start, end = agent.position_history[i], agent.position_history[i + 1]
                # Create our arrow patch
                arrow = FancyArrowPatch(start, end, color=color, arrowstyle='->', mutation_scale=20)
                ax.add_patch(arrow)

                # Plot points
                ax.plot(*start, color=color, marker='o')
                ax.plot(*end, color=color, marker='o')

            # Add a legend entry for this agent
            ax.plot([], [], color=color, label=agent.identifier, marker='o')

        ax.legend()

        # Set equal aspect ratio
        ax.set_aspect('equal', adjustable='datalim')

        # Show the plot
        plt.show()

    @staticmethod
    def plot_animated(agents, frames_per_round=10):
        fig, ax = plt.subplots()

        def update(frame):
            ax.clear()
            for idx, agent in enumerate(agents):
                color = Graph.colors[idx % len(Graph.colors)]

                # todo: there has to be some way to interpolate x and y at the same time thru numpy
                agent_position_history = np.array(agent.position_history)
                frame_datapoints = np.arange(0, len(agent_position_history) * frames_per_round, frames_per_round)

                interpolated_x = np.interp(frame, frame_datapoints, agent_position_history[:, 0])
                interpolated_y = np.interp(frame, frame_datapoints, agent_position_history[:, 1])

                ax.plot(interpolated_x, interpolated_y, color=color, marker='o')
                ax.plot([], [], color=color, label=agent.identifier, marker='o')

            ax.legend()
            ax.set_aspect('equal', adjustable='datalim')

        frame_count = max(len(agent.position_history) for agent in agents) * frames_per_round
        anim = FuncAnimation(fig, update, frames=frame_count, interval=200)

        # Show the animated plot
        plt.show()