import time
import random
import json
from airsim_wrapper import AirSimWrapper

# obtain list of drones
with open('settings.json', 'r') as file:
    settings = json.load(file)

# Initialize an empty list for drone names
drone_names = []

# Iterate through each vehicle in the "Vehicles" section
for vehicle_name, attributes in settings.get("Vehicles", {}).items():
    # Add drone name
    drone_names.append(vehicle_name)

# Initializes the AirSim Wrapper with the drones in environment
print(f"Initializing AirSim...")
aw = AirSimWrapper(drone_names)
aw.drones['Drone1'].set_leader(True)  # Set Drone1 as leader

def random_fly():
    while True:
        if aw.drones['Drone1'].get_leader():  # Check if Drone1 is still the leader
            x, y, z = (random.uniform(-10, 10), random.uniform(-10, 10), -10)  # Example random positions
            print(f"Moving leader to: {x}, {y}, {z}")
            aw.drones['Drone1'].fly_to([x, y, z])
            time.sleep(5)  # Wait for some time before next move


if __name__ == "__main__":
    random_fly()
