import matplotlib.pyplot as plt
import numpy as np

# reserved line style
SHAPE = ["-o", "-v", "-s", "-D", "-x"]


class plot_result:
    def __init__(self, agents) -> None:
        self._agents = agents

    def plot_fig(self):
        for agent in self._agents:
            pos_hist = np.array(agent.position_history)
            plt.plot(pos_hist[:, 0], pos_hist[:, 1], SHAPE[agent.identifier])

        plt.show()
