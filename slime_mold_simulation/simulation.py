import math
from random import randint
from numba import jit

import numpy as np
from scipy.ndimage import gaussian_filter

#Put the global parameters in a seperate file for visualization?
# Simulationparameters
WIDTH = 1000
HEIGHT = 1000
DECAY = 0.95
DIFFUSION_COEFFICENT = 0.5

# Agentparameters
AGENT_NUMBER = 100
SENSOR_ANGLE = 0.33
SPEED = 2
THRESHOLD = 0.1  # Adjust based on your simulation
ROTATION_SPEED = 1
SENSOR_DISTANCE = 10 #this is the radius

class PheromoneArray:
    def __init__(self, width=WIDTH, height=HEIGHT,):
        self.width = WIDTH
        self.height = HEIGHT
        self.p_array = np.zeros((WIDTH, HEIGHT))

    def diffuse(self, diffuse=DIFFUSION_COEFFICENT):
        # Apply Gaussian filter for diffusion
        self.p_array = gaussian_filter(self.p_array, sigma=DIFFUSION_COEFFICENT)

    def decay(self, decay=DECAY):
        self.p_array = self.p_array * decay

    def get_pheromone_value_at(self, x, y):
        # Clip x and y to ensure they are within the bounds of the pheromone array
        x = np.clip(np.round(x).astype(int), 0, self.width - 1)
        y = np.clip(np.round(y).astype(int), 0, self.height - 1)

        return self.p_array[y, x]  # Access the pheromone value at the specified position

# the agent class creates a list with one dictionary for each agent
class Agent:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.heading = np.random.uniform(0, 2 * math.pi)  # Initial heading is straight
        self.sensor_distance = SENSOR_DISTANCE  # Distance from agent to sensor
        self.threshold = THRESHOLD
        self.rotation_speed = ROTATION_SPEED

        # Define sensor positions directly in the constructor
        self.main_sensor = [self.x + self.sensor_distance * np.cos(self.heading),
                            self.y + self.sensor_distance * np.sin(self.heading)]

        # Calculate positions of the other two sensors

        self.sensor1 = [self.x + self.sensor_distance * np.cos(self.heading + SENSOR_ANGLE),
                        self.y + self.sensor_distance * np.sin(self.heading + SENSOR_ANGLE)]

        self.sensor2 = [self.x + self.sensor_distance * np.cos(self.heading - SENSOR_ANGLE),
                        self.y + self.sensor_distance * np.sin(self.heading - SENSOR_ANGLE)]

    def rotate_towards_sensor(self, pheromone_array):
        # Combine sensor positions into a numpy array
        sensors = np.array([self.main_sensor, self.sensor1, self.sensor2])

        sensor_values = pheromone_array.get_pheromone_value_at(sensors[:, 0], sensors[:, 1])

        # Find indices where sensor values exceed the threshold
        active_sensors = sensor_values > self.threshold

        # Calculate angles to sensors with matrix operations
        angles_to_sensors = np.arctan2(sensors[active_sensors, 1] - self.y,
                                       sensors[active_sensors, 0] - self.x)

        # Adjust heading towards the sensors with matrix operations
        self.heading += np.sum(angles_to_sensors) * self.rotation_speed


    def move(self):
        # Update agent's position based on heading and speed
        self.speed = SPEED
        new_x = self.x + self.speed * np.cos(self.heading)
        new_y = self.y + self.speed * np.sin(self.heading)
        
        # Update agent's position after bouncing
        self.x = new_x
        self.y = new_y
        
        self.reflect_at_boundary(WIDTH, HEIGHT)
        # Ensure the agent stays within the simulation bounds
       # self.x = max(1, min(self.x, WIDTH - 1))
       # self.y = max(1, min(self.y, HEIGHT - 1))
        
    def reflect_at_boundary(agent, width, height):
        # Reflect off vertical boundaries (left/right edges)
        if agent.x <= 0 or agent.x >= width:
            agent.heading = np.pi - agent.heading

        # Reflect off horizontal boundaries (top/bottom edges)
        if agent.y <= 0 or agent.y >= height:
            agent.heading = -agent.heading

        # Normalize the angle to ensure it's between 0 and 2*np.pi
        agent.heading = agent.heading % (2 * np.pi)

    def deposit_pheromone(self, pheromone_array):
        # Round coordinates to the nearest integers and clip to array bounds
        x_idx = np.clip(int(round(self.x)), 0, pheromone_array.width - 1)
        y_idx = np.clip(int(round(self.y)), 0, pheromone_array.height - 1)

        # Deposit pheromone at the rounded position
        pheromone_array.p_array[y_idx, x_idx] += 1