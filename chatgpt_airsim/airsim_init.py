from airsim_wrapper import *
import os
import json
import time
from vector_math import *
import threading
import queue
from chatgpt_handler import ask, extract_python_code, initialize_chatgpt


# class attributes for ANSI escape sequences for colors
# essentially just changes the color of the terminal for the user
class colors:  # You may need to change color settings
    RED = "\033[31m"
    ENDC = "\033[m"
    GREEN = "\033[32m"
    YELLOW = "\033[33m"
    BLUE = "\033[34m"


class SharedParameter:
    def __init__(self, value):
        self.lock = threading.Lock()
        self.param = value

    def set_param(self, new_param):
        with self.lock:
            self.param = new_param

    def get_param(self):
        with self.lock:
            return self.param


def read_new_commands(command_queue):
    while True:
        # User inputs a new command
        prompt = input(colors.YELLOW + "AirSim> " + colors.ENDC)

        if prompt == "!quit" or prompt == "!exit":
            command_queue.put(prompt)
            break

        if prompt == "!clear":
            os.system("cls")
            continue

        # sends prompt to chatgpt
        response = ask(prompt, chat_history)
        command_queue.put(response)


def flocking_logic(command_queue):
    while True:
        try:
            # Check if there are messages in the queue
            while not command_queue.empty():
                # Get the command without blocking
                command = command_queue.get_nowait()

                if command == "!quit" or command == "!exit":
                    return  # Exit the main loop

                # runs chatgpt generated python code
                print(f"Processing command: {command}")
                code = extract_python_code(command, code_block_regex)
                if code is not None:
                    print("Please wait while I run the code in AirSim...")
                    exec(extract_python_code(command, code_block_regex))
                    print("Done!\n")

        except queue.Empty:
            # Queue is empty, no commands to process
            pass

        # flocking logic
        sepVectors = aw.separation()
        alignVectors = aw.alignment()
        cohVectors = aw.cohesion()
        goalVectors = aw.goal(goalPos.get_param())
        # print(f'Goal Position: {goalPos.get_param()}')
        avoidVectors = aw.avoid()
        # print(f'Separation Vectors: {sepVectors}')
        # print(f'Alignment Vectors: {alignVectors}')
        # print(f'Cohesion Vectors: {cohVectors}')
        # print(f'Goal Vectors: {goalVectors}')
        # print(f'Avoid Vectors: {avoidVectors}')

        for drone, sepVec, alignVec, cohVec, goalVec, avoidVec in zip(aw.drones, sepVectors, alignVectors, cohVectors,
                                                                      goalVectors, avoidVectors):
            velVec = sumVec(
                [weightVec(sepVec, sepW.get_param()), weightVec(alignVec, aliW.get_param()), weightVec(cohVec, cohW.get_param()), weightVec(goalVec, goalW.get_param()),
                 weightVec(avoidVec, avoidW.get_param())])
            drone.fly(velVec)

        time.sleep(0.2)


if __name__ == "__main__":
    # Create a queue for inter-thread communication
    command_queue = queue.Queue()

    # obtain list of drones
    with open('settings.json', 'r') as file:
        settings = json.load(file)

    # Initialize an empty list for drone names
    drones = {}

    # Iterate through each vehicle in the "Vehicles" section
    for vehicle_name, attributes in settings.get("Vehicles", {}).items():
        # Check if the vehicle type is "SimpleFlight" or "PhysXCar"
        if attributes.get("VehicleType") == "SimpleFlight":
            # Add drone name
            drones[vehicle_name] = [attributes.get("X"), attributes.get("Y"), attributes.get("Z")]

    # Initializes the AirSim Wrapper with the drones in environment
    print(f"Initializing AirSim...")
    aw = AirSimWrapper(drones)
    print(f"Done.")

    chat_history, code_block_regex = initialize_chatgpt()

    # make the drones take off and wait for 3 seconds
    aw.initialize()
    time.sleep(3)

    print("Welcome to Airsim Flocking Simulator")

    # weight variables to be edited by command
    sepW = SharedParameter(1)
    aliW = SharedParameter(1)
    cohW = SharedParameter(1)
    goalW = SharedParameter(2)
    # Initialize shared goal position object
    goalPos = SharedParameter(aw.get_position('crowd'))
    avoidW = SharedParameter(3)

    # Start the command reading thread
    command_thread = threading.Thread(target=read_new_commands, args=(command_queue,), daemon=True)
    command_thread.start()

    # Run the main flocking logic, processing commands from the queue
    flocking_logic(command_queue)
