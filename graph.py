import matplotlib.pyplot
import matplotlib.pyplot as plt
import numpy as np

from matplotlib.animation import FuncAnimation

# pycharm animation support
matplotlib.use("TkAgg")


class Graph:
    colors = np.array([
        [0xe8, 0x3b, 0x3b],  # red
        [0x7a, 0x30, 0x45],  # maroon
        [0xf9, 0xc2, 0x2b],  # yellow
        [0x16, 0x5a, 0x4c],  # forest green
        [0x4d, 0x9b, 0xe6],  # blue
        [0x30, 0xe1, 0xb9],  # cyan
        [0xc3, 0x24, 0x54]  # dark pink
    ]) / 255

    @staticmethod
    def plot_animated(data):
        fig, ax = plt.subplots(figsize=(8, 4))

        lines = []
        scatters = []

        for i in range(data.settings.agents):
            current_color = Graph.colors[i % len(Graph.colors)]

            flight_path_line, = ax.plot([], [], lw=2, color=current_color, linestyle='--')
            lines.append(flight_path_line)

            scatter = ax.scatter([], [], marker='o', c=current_color.reshape(1, -1), s=50, alpha=0.8,
                                 label=f'Drone {i + 1}')
            scatters.append(scatter)

        def init():
            ax.set_xlabel('x')
            ax.set_ylabel('y')

            ax.set_ylim(data.settings.y_min, data.settings.y_max)
            ax.set_xticks(range(data.settings.x_min, data.settings.x_max, data.settings.x_ticks))

            for dashed_line, scatter in zip(lines, scatters):
                dashed_line.set_data([], [])
                scatter.set_offsets(np.empty((0, 2)))

            handles, labels = ax.get_legend_handles_labels()
            ax.legend(handles=handles, labels=labels, loc="upper left", labelspacing=0.6, fontsize=10)
            return lines + scatters

        def update(frame):
            for i, (dashed_line, scatter) in enumerate(zip(lines, scatters)):
                all_positions = data.agents[i]["position_history"]

                dashed_line.set_data([x for x, y in all_positions[max(0, frame - 3):frame + 1]],
                                     [y for x, y in all_positions[max(0, frame - 3):frame + 1]])
                latest_x, latest_y = all_positions[frame]
                scatter.set_offsets([latest_x, latest_y])

            if frame == data.settings.rounds - 1:
                plt.savefig(f'{data.directory}/last.svg', bbox_inches='tight')
            return lines + scatters

        ani = FuncAnimation(fig, update, frames=data.settings.rounds, init_func=init, blit=False)
        ani.save(f'{data.directory}/animation.gif', fps=3)
        plt.show()
