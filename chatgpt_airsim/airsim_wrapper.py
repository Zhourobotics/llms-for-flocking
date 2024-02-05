import airsim
import math
import numpy as np
from drone import Drone
from car import Car

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
    # takes list of drone names and car names to create dictionary of drone and car objects
    def __init__(self, drone_names, car_names):
        self.drone_client = airsim.MultirotorClient()
        self.drones = {name: Drone(self.drone_client, name) for name in drone_names}
        self.car_client = airsim.CarClient()
        self.cars = {name: Car(self.car_client, name) for name in car_names}

    def get_drone(self, drone_name):
        return self.drones.get(drone_name, None)

    def get_car(self, car_name):
        return self.cars.get(car_name, None)

    # gets the position of the object in the environment, NOT drones or cars
    def get_position(self, object_name):
        query_string = objects_dict[object_name] + ".*"
        object_names_ue = []
        while len(object_names_ue) == 0:
            object_names_ue = self.client.simListSceneObjects(query_string)
        pose = self.client.simGetObjectPose(object_names_ue[0])
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]
