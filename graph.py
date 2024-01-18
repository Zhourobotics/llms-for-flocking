import matplotlib.pyplot as plt
from matplotlib.patches import FancyArrowPatch


class Graph:

    @staticmethod
    def plot_agents(agents):
        # Define a list of colors for different agents
        colors = ['red', 'green', 'blue', 'yellow', 'purple', 'orange', 'cyan', 'magenta', 'brown', 'black']

        # Create a figure and axis
        fig, ax = plt.subplots()

        # Iterate over the dictionary
        for idx, (agent) in enumerate(agents):
            # Get the color for this agent
            color = colors[idx % len(colors)]

            # Plot each segment with an arrow
            for i in range(len(agent.position_history) - 1):
                start, end = agent.position_history[i], agent.position_history[i + 1]
                # Create an arrow patch
                arrow = FancyArrowPatch(start, end, color=color, arrowstyle='->', mutation_scale=20)
                ax.add_patch(arrow)

                # Also plot points
                ax.plot(*start, color=color, marker='o')
                ax.plot(*end, color=color, marker='o')

            # Add a legend entry for this agent
            ax.plot([], [], color=color, label=agent.identifier, marker='o')

        # Add a legend
        ax.legend()

        # Set equal aspect ratio
        ax.set_aspect('equal', adjustable='datalim')

        # Show the plot
        plt.show()
