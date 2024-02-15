import math
from random import randint

import numpy as np
from scipy.ndimage import gaussian_filter

#Put the global parameters in a seperate file for visualization?
# Simulationparameters
WIDTH = 1000
HEIGHT = 1000
DECAY = 0.97
DIFFUSION_COEFFICENT = 0.2

# Agentparameters
AGENT_NUMBER = 10000
SENSOR_ANGLE = 0.33
RADIUS = 0.5
SPEED = 2
THRESHOLD = 0.5  # Adjust based on your simulation
ROTATION_SPEED = 0.01

class PheromoneArray:
    def __init__(self, width=WIDTH, height=HEIGHT,):
        self.width = WIDTH
        self.height = HEIGHT
        self.p_array = np.zeros((WIDTH, HEIGHT))

    def diffuse(self, diffuse=DIFFUSION_COEFFICENT):
        # Implement pheromone diffusion logic
        pass

    def decay(self, decay=DECAY):
        # Implement pheromone decay logic
        pass

    def get_pheromone_value_at(self, x, y):
        # Ensure x and y are within the bounds of the pheromone array
        x = np.clip(int(round(x)), 0, self.width - 1)
        y = np.clip(int(round(y)), 0, self.height - 1)

        return self.p_array[y, x]  # Access the pheromone value at the specified position

# the agent class creates a list with one dictionary for each agent
class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heading = np.random.uniform(0, 2 * math.pi)  # Initial heading is straight
        self.sensors = np.zeros((3, 2))  # 3 sensors with x, y coordinates
        self.sensor_distance = 10  # Distance from agent to sensor
        self.threshold = THRESHOLD
        self.rotation_speed = ROTATION_SPEED

    def calculate_sensor_directions(self):
        angles = np.linspace(-SENSOR_ANGLE / 2, SENSOR_ANGLE / 2, 3)
        for i in range(3):
            self.sensors[i] = [self.x + self.sensor_distance * np.cos(self.heading + angles[i]),
                               self.y + self.sensor_distance * np.sin(self.heading + angles[i])]
            
    def rotate_towards_sensor(self, pheromone_array):
        for i in range(3):
            sensor_x, sensor_y = self.sensors[i]
            sensor_value = pheromone_array.get_pheromone_value_at(sensor_x, sensor_y)

            # You may need to adjust the threshold based on your simulation
            if sensor_value > self.threshold:
                angle_to_sensor = np.arctan2(sensor_y - self.y, sensor_x - self.x)
                angle_difference = angle_to_sensor - self.heading

                # Adjust heading towards the sensor
                self.heading += angle_difference * self.rotation_speed

    def move(self):
        # Update agent's position based on heading and speed
        self.speed = SPEED
        self.x += self.speed * np.cos(self.heading)
        self.y += self.speed * np.sin(self.heading)

        # Ensure the agent stays within the simulation bounds (adjust as needed)
        self.x = max(0, min(self.x, WIDTH - 1))
        self.y = max(0, min(self.y, HEIGHT - 1))

    def deposit_pheromones(self, pheromone_array):
            # Round the agent's coordinates to integers
            deposit_x = int(round(self.x))
            deposit_y = int(round(self.y))

            # Deposit pheromones at the agent's position
            pheromone_array.p_array[deposit_y, deposit_x] += 1