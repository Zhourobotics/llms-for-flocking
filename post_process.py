import pickle

class PostProcess:
    """
    A class to do post processing for data generated during test.
    """

    def __init__(self) -> None:
        self._agents =      []
        self._config =      []
        self._pos_hist =    []
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

    def save_data(self, agents, config):
        """Storing the data and system configuration to a binary file using pickle."""
        # store data
        self.__store_data(agents, config)

        # collecting data into a dictionary
        data = {"pos_hist": self._pos_hist,
                "config": self._config, 
                "memory": self._memory_hist}
        
        # initiate the file based on the test id
        file_name = f'./results/LLM_test_{self._config["test_id"]:03d}'
        data_file = open(file_name, 'ab')

        # storing the data to the file
        pickle.dump(data, data_file)
        data_file.close()


    def load_data(self, id):
        """Loading the data and system configuration from a binary file using pickle."""
        data_file = open(f'./results/LLM_test_{id:03d}', 'rb')
        data = pickle.load(data_file)
        self._config =      data["config"]
        self._memory_hist = data["memory"]
        self._pos_hist =    data["pos_hist"]

    def get_pos(self):
        return self._pos_hist
    
    def get_memory(self):
        return self._memory_hist