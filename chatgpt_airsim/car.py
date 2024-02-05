import airsim
import json


# Car class for each car in environment
class Car:
    def __init__(self, client, car_name):
        self.client = client
        self.car_name = car_name

        # Obtain the initial offset from settings.json
        with open('settings.json', 'r') as file:
            settings = json.load(file)

        # Ensure the car name exists in the settings to avoid KeyError
        if car_name in settings["Vehicles"]:
            car_settings = settings["Vehicles"][car_name]
            # Extract the initial X, Y, Z positions
            initial_offset = [
                car_settings.get("X", 0),  # Default to 0 if not found
                car_settings.get("Y", 0),  # Default to 0 if not found
                car_settings.get("Z", 0)  # Default to 0 if not found
            ]
        else:
            initial_offset = [0, 0, 0]  # Default offset if car_name is not found

        self.initial_offset = initial_offset

        # Confirm connection
        self.client.confirmConnection()

    # Returns the car's current position, relative to the world
    def get_car_position(self):
        pose = self.client.simGetVehiclePose(vehicle_name=self.car_name)
        # Adjust the position by the initial offset to align with the global origin
        adjusted_position = [
            pose.position.x_val + self.initial_offset[0],
            pose.position.y_val + self.initial_offset[1],
            pose.position.z_val + self.initial_offset[2]
        ]
        return adjusted_position

    # Gets the car's current speed
    def get_speed(self):
        car_state = self.client.getCarState(vehicle_name=self.car_name)
        return car_state.speed
