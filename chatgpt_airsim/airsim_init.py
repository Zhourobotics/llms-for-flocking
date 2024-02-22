import openai
import re
import argparse
from airsim_wrapper import *
import math
import numpy as np
import os
import json
import time
from vector_math import *

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

print("Welcome to Airsim Flocking Simulator")

# infinite loop for user commands
aw.initialize()

time.sleep(3)

sepW = 2
aliW = 1
cohW = 1.5
goalW = 2
goalPos = aw.get_position('crowd')
avoidW = 2.5

while True:
    sepVectors = aw.separation()
    alignVectors = aw.alignment()
    cohVectors = aw.cohesion()
    goalVectors = aw.goal(goalPos)
    avoidVectors = aw.avoid()
    print(f'Separation Vectors: {sepVectors}')
    print(f'Alignment Vectors: {alignVectors}')
    print(f'Cohesion Vectors: {cohVectors}')
    print(f'Goal Vectors: {goalVectors}')
    print(f'Avoid Vectors: {avoidVectors}')

    for drone, sepVec, alignVec, cohVec, goalVec, avoidVec in zip(aw.drones, sepVectors, alignVectors, cohVectors, goalVectors, avoidVectors):
        velVec = sumVec(
            [weightVec(sepVec, sepW), weightVec(alignVec, aliW), weightVec(cohVec, cohW), weightVec(goalVec, goalW), weightVec(avoidVec, avoidW)])
        drone.fly(velVec)

    time.sleep(0.5)
