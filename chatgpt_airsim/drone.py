import airsim
from vector_math import *


# Drone class for each drone in the environment
class Drone:

    def __init__(self, client, drone_name, initial_offset):
        self.client = client
        self.drone_name = drone_name
        self.initial_offset = initial_offset

        # Confirm connection and enable API control for this drone
        self.client.confirmConnection()
        self.client.enableApiControl(True, drone_name)
        self.client.armDisarm(True, drone_name)

    # makes the drone take off
    def takeoff(self):
        return self.client.takeoffAsync(vehicle_name=self.drone_name)

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

    def get_drone_velocity(self):
        # Get the state of the drone
        drone_state = self.client.getMultirotorState(vehicle_name=self.drone_name)

        # Extract the velocity
        vx = drone_state.kinematics_estimated.linear_velocity.x_val
        vy = drone_state.kinematics_estimated.linear_velocity.y_val
        vz = drone_state.kinematics_estimated.linear_velocity.z_val

        return [vx, vy, vz]

    def fly(self, velocity):
        # Extract the X, Y, and Z components of the velocity vector
        vx, vy, vz = velocity

        # Command the drone to move with the specified velocity
        self.client.moveByVelocityAsync(vx, vy, vz, duration=0.5, vehicle_name=self.drone_name)

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

    def separation(self, drones, close_limit, repel_factor, interpStrength):
        repelVecList = []
        dronePos = self.get_drone_position()
        for drone in drones:
            if drone != self:
                dist_vec = calcDistVec(dronePos, drone.get_drone_position())
                distance = mag(dist_vec)
                if distance < close_limit:
                    repelVec = calcRepelVec(dist_vec, repel_factor)
                    repelVecList.append(repelVec)
        averageRepelVec = averageVec(repelVecList)
        if len(repelVecList) == 0:
            return [0, 0, 0]
        return averageRepelVec

    def alignment(self, drones, radius, interpStrength):
        limitDronesVel = []
        for drone in drones:
            if drone != self and calcDist(self.get_drone_position(), drone.get_drone_position()) < radius:
                limitDronesVel.append(drone.get_drone_velocity())
        if len(limitDronesVel) == 0:
            return self.get_drone_velocity()
        averageVel = averageVec(limitDronesVel)
        interpVel = interpVec(self.get_drone_velocity(), averageVel, interpStrength)
        return interpVel

    def cohesion(self, drones, radius, interpStrength):
        limitDronesPos = []
        for drone in drones:
            if drone != self and calcDist(self.get_drone_position(), drone.get_drone_position()) < radius:
                limitDronesPos.append(drone.get_drone_position())
        if len(limitDronesPos) == 0:
            return self.get_drone_velocity()
        centroid = averageVec(limitDronesPos)
        vel = calcDistVec(self.get_drone_position(), centroid)
        return vel

    def goal(self, goal_position, speed, interpStrength):
        current_position = self.get_drone_position()
        direction_vector = calcDistVec(current_position, goal_position)
        distance = mag(direction_vector)

        if distance == 0:
            return [0, 0, 0]  # Already at the goal

        # Normalize the direction vector

        normalized_direction = normalize(direction_vector)

        # Scale the normalized direction by the desired speed
        velocity_vector = weightVec(normalized_direction, speed)

        return velocity_vector

    def avoid(self, avoidLimit, avoidFactor, interpStrength):
        dronePos = self.get_drone_position()
        if abs(dronePos[2]) < avoidLimit:
            dist_vec = [0, 0, abs(dronePos[2])]
            avoidVec = calcRepelVec(dist_vec, avoidFactor)
            return avoidVec
        else:
            return [0, 0, 0]
