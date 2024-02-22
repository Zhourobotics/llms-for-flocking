import time

import airsim
import math
import numpy as np
from drone import Drone
import random

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
    def __init__(self, drones):
        self.drone_client = airsim.MultirotorClient()

        self.drones = []
        for name, offset in drones.items():
            self.drones.append(Drone(self.drone_client, name, offset))

        self.close_limit = 10
        self.repel_factor = 10

        self.radius = 50  # Greater than close_limit
        self.interp_strength = 0.5  # between 0-1

        self.goalSpeed = 5

        self.avoidLimit = 10
        self.avoidFactor = 10

    def get_drone(self, index):
        return self.drones[index]

    # gets the position of the object in the environment, NOT drones or cars
    def get_position(self, object_name):
        query_string = objects_dict[object_name] + ".*"
        object_names_ue = []
        while len(object_names_ue) == 0:
            object_names_ue = self.drone_client.simListSceneObjects(query_string)
        pose = self.drone_client.simGetObjectPose(object_names_ue[0])
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]

    def initialize(self):
        # Start all takeoffs without waiting for each to complete
        takeoff_futures = [drone.takeoff() for drone in self.drones]

        # Now, wait for all takeoffs to complete
        for future in takeoff_futures:
            future.join()

    def separation(self):
        repelVectors = []
        for drone in self.drones:
            repelVec = drone.separation(self.drones, self.close_limit, self.repel_factor, self.interp_strength)
            repelVectors.append(repelVec)
        return repelVectors

    def alignment(self):
        alignVectors = []
        for drone in self.drones:
            alignVec = drone.alignment(self.drones, self.radius, self.interp_strength)
            alignVectors.append(alignVec)
        return alignVectors

    def cohesion(self):
        cohesionVectors = []
        for drone in self.drones:
            cohesVec = drone.cohesion(self.drones, self.radius, self.interp_strength)
            cohesionVectors.append(cohesVec)
        return cohesionVectors

    def goal(self, goalPos):
        goalVectors = []
        for drone in self.drones:
            goalVec = drone.goal(goalPos, self.goalSpeed, self.interp_strength)
            goalVectors.append(goalVec)
        return goalVectors

    def avoid(self):
        avoidVectors = []
        for drone in self.drones:
            avoidVec = drone.avoid(self.avoidLimit, self.avoidFactor, self.interp_strength)
            avoidVectors.append(avoidVec)
        return avoidVectors
