import pickle
import os

from datetime import datetime


class Data:
    """
    A class to facilitate storage and retrieval of test data
    """
    def __init__(self, identifier, agents, settings, results):
        self.identifier = identifier
        self.directory = f'./{results}/{identifier}'
        self.agents = agents
        self.settings = settings
        self.results = results

    @staticmethod
    def save(
            agents,
            settings,
            identifier=datetime.now().strftime("%y%b%d%H%M%S").lower(),
            results="results"
    ) -> str:
        Data.check_for_results_directory(results)  # make sure we have a results directory

        if not os.path.isdir(f'./{results}/{identifier}'):
            os.makedirs(f'./{results}/{identifier}')  # create an empty test results directory

            file = open(f'./{results}/{identifier}/results', 'ab')

            agents_object = [
                {
                    "identifier": agent.identifier,
                    "position_history": agent.position_history,
                    "memory": agent.memory
                } for agent in agents
            ]

            pickle.dump(Data(identifier, agents_object, settings, results), file)

            file.close()
            print(f'Success: Save test {identifier}!')
            return identifier
        else:
            print(f'Error: Test {identifier} already exists!')

    @staticmethod
    def load(args, results="results"):
        file = open(f'./{results}/{args.name}/results', 'rb')
        data = pickle.load(file)

        # Load plot settings in :)
        data.settings.x_min = args.x_min
        data.settings.x_max = args.x_max
        data.settings.x_ticks = args.x_ticks
        data.settings.y_min = args.y_min
        data.settings.y_max = args.y_max

        print(f'Success: Load test {args.name}!')
        return data

    @staticmethod
    def check_for_results_directory(dirname):
        # Create our results directory
        if not os.path.exists(f'./{dirname}'):
            os.makedirs(f'./{dirname}')
