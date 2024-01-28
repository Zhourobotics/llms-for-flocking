import pickle
import os
from agents import FlockingAgent


class PostProcess:
    """
    A class to post-process data generated during tests
    """

    def __init__(self) -> None:
        # Create results directory if none exists
        if not os.path.exists("./results"):
            os.makedirs("./results")

        self._agents = []
        self._config = []
        self._pos_hist = []
        self._memory_hist = []

    def __store_data(self, agents, config):
        self._agents = agents
        self._config = config
        self._pos_hist = [agent.position_history for agent in agents]
        self._memory_hist = [agent.memory for agent in agents]

    def get_agents(self):
        return self._agents

    def get_config(self):
        return self._config
    
    def get_pos(self):
        return self._pos_hist
    
    def get_memory(self):
        return self._memory_hist

    def save_data(self, agents, config):
        """Storing the data and system configuration to a binary file using pickle."""
        # store data
        self.__store_data(agents, config)

        # collecting data into a dictionary
        data = {
            "pos_hist": self._pos_hist,
            "config": self._config,
            "memory": self._memory_hist,
        }

        # create a file based on the test id
        file_name = f'./results/LLM_test_{self._config["test_id"]:03d}'
        data_file = open(file_name, "ab")

        # storing the data to the file
        pickle.dump(data, data_file)
        data_file.close()

    def load_data(self, id_):
        """Loading the data and system configuration from a binary file using pickle."""
        data_file = open(f"./results/LLM_test_{id_:03d}", "rb")
        data = pickle.load(data_file)
        self._config = data["config"]
        self._memory_hist = data["memory"]
        self._pos_hist = data["pos_hist"]

    def get_sys(self):
        return self.get_config, self.get_pos, self.get_memory

    def load_agents(self, id):
        """This function load the data and assign the corresponding data to the agents."""
        # load data from the saved file
        if self._config == []:
            self.load_data(id)
        config, pos_hist, memory = self.get_sys()
        # flush the "coolest_key" to 0 to assign from the beginning
        coolest_key = 0

        # load data to the agents
        agent_count = config["agent_count"]
        agents = [FlockingAgent(i, pos_hist[i][0]) for i in range(agent_count)]
        ...
