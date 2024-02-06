import airsim
import math
import numpy as np
import json

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
    # takes list of drone names to create dictionary of drone objects
    def __init__(self, drone_names):
        self.client = airsim.MultirotorClient()
        self.drones = {name: Drone(self.client, name, ) for name in drone_names}

    def get_drone(self, drone_name):
        return self.drones.get(drone_name, None)

    # gets the position of the object in the environment
    def get_position(self, object_name):
        query_string = objects_dict[object_name] + ".*"
        object_names_ue = []
        while len(object_names_ue) == 0:
            object_names_ue = self.client.simListSceneObjects(query_string)
        pose = self.client.simGetObjectPose(object_names_ue[0])
        return [pose.position.x_val, pose.position.y_val, pose.position.z_val]


# Drone class for each drone in the environment
class Drone:
    def __init__(self, client, drone_name):
        self.client = client
        self.drone_name = drone_name

        # Obtain the initial offset from settings.json
        with open('settings.json', 'r') as file:
            settings = json.load(file)

        # Ensure the drone name exists in the settings to avoid KeyError
        if drone_name in settings["Vehicles"]:
            drone_settings = settings["Vehicles"][drone_name]
            # Extract the initial X, Y, Z positions
            initial_offset = [
                drone_settings.get("X", 0),  # Default to 0 if not found
                drone_settings.get("Y", 0),  # Default to 0 if not found
                drone_settings.get("Z", 0)  # Default to 0 if not found
            ]
        else:
            initial_offset = [0, 0, 0]  # Default offset if drone_name is not found

        self.initial_offset = initial_offset

        # Confirm connection and enable API control for this drone
        self.client.confirmConnection()
        self.client.enableApiControl(True, drone_name)
        self.client.armDisarm(True, drone_name)

    # makes the drone take off
    def takeoff(self):
        self.client.takeoffAsync(vehicle_name=self.drone_name)

    # makes the drone land on the ground
    def land(self):
        self.client.landAsync(vehicle_name=self.drone_name)

    # returns the drone's current position, relative to the world
    def get_drone_position(self):
        pose = self.client.simGetVehiclePose(vehicle_name=self.drone_name)
        # Adjust the position by the initial offset to align with the global origin
        adjusted_position = [
            pose.position.x_val + self.initial_offset[0],
            pose.position.y_val + self.initial_offset[1],
            pose.position.z_val + self.initial_offset[2]
        ]
        return adjusted_position

    # makes the drone fly to a specific point in the environment, z axis is always negative
    def fly_to(self, point):
        if point[2] > 0:
            self.client.moveToPositionAsync(point[0], point[1], -point[2], 5, vehicle_name=self.drone_name)
        else:
            self.client.moveToPositionAsync(point[0], point[1], point[2], 5, vehicle_name=self.drone_name)

    # flies to various points in a path
    def fly_path(self, points):
        airsim_points = []
        for point in points:
            if point[2] > 0:
                airsim_points.append(airsim.Vector3r(point[0], point[1], -point[2]))
            else:
                airsim_points.append(airsim.Vector3r(point[0], point[1], point[2]))
        self.client.moveOnPathAsync(airsim_points, 5, 120, airsim.DrivetrainType.ForwardOnly,
                                    airsim.YawMode(False, 0),
                                    20, 1, vehicle_name=self.drone_name)

    # sets the drone's yaw rotation (turn left or right)
    def set_yaw(self, yaw):
        self.client.rotateToYawAsync(yaw, 5, vehicle_name=self.drone_name)

    # gets the drone's current yaw
    def get_yaw(self):
        orientation_quat = self.client.simGetVehiclePose(vehicle_name=self.drone_name).orientation
        yaw = airsim.to_eularian_angles(orientation_quat)[2]
        return yaw
