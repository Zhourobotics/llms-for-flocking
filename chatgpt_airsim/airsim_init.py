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

sepW = 0.5
aliW = 0.5

while True:
    sepVectors = aw.separation()
    alignVectors = aw.alignment()
    print(sepVectors)
    print(alignVectors)

    # Ensure that repelVectors list and drones list are of the same length
    if len(sepVectors) == len(aw.drones) and len(alignVectors) == len(aw.drones):
        for drone, sepVec, alignVec in zip(aw.drones, sepVectors, alignVectors):
            velVec = sumVec([weightVec(sepVec, sepW), weightVec(alignVec, aliW)])
            drone.fly(velVec)
    else:
        print("Error: The number of repel vectors and drones does not match.")

    time.sleep(0.5)
