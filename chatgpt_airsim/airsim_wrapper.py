import time

import airsim
import math
import numpy as np
from drone import Drone
from pynput import keyboard

# dictionary of environment objects and their associated real names in AirSim
objects_dict = {
    "turbine1": "BP_Wind_Turbines_C_1",
    "turbine2": "StaticMeshActor_2",
    "solarpanels": "StaticMeshActor_146",
    "crowd": "StaticMeshActor_6",
    "car": "StaticMeshActor_10",
    "tower1": "SM_Electric_trellis_179",
    "tower2": "SM_Electric_trellis_7",
    "tower3": "SM_Electric_trellis_8",
}


# API that allows chatGPT to connect to AirSim to make the drone fly
class AirSimWrapper:
    # takes list of drone names to create dictionary of drones
    def __init__(self, drone_names):
        self.drone_client = airsim.MultirotorClient()
        self.drones = {name: Drone(self.drone_client, name) for name in drone_names}
        self.listener = None

    def start_keyboard_listener(self):
        # Method to start keyboard listener
        self.listener = keyboard.Listener(on_press=self.on_press)
        self.listener.start()

    def stop_keyboard_listener(self):
        # Method to stop the listener
        if self.listener:
            self.listener.stop()

    def on_press(self, key):
        # Delegate key presses to the leader drone
        for drone_name, drone in self.drones.items():
            if drone.get_leader():
                drone.on_press(key)
                break  # Assuming only one leader, break after processing

    def get_drone(self, drone_name):
        return self.drones.get(drone_name, None)

    # gets the position of the object in the environment, NOT drones or cars
    def get_position(self, object_name):
        query_string = objects_dict[object_name] + ".*"
        object_names_ue = []
        while len(object_names_ue) == 0:
            object_names_ue = self.drone_client.simListSceneObjects(query_string)
        pose = self.drone_client.simGetObjectPose(object_names_ue[0])
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]