from config import *

import math
from random import randint
import numba
import numpy as np
from scipy.ndimage import gaussian_filter


class PheromoneArray:
    def __init__(self, width=WIDTH, height=HEIGHT,):
        self.width = WIDTH
        self.height = HEIGHT
        self.p_array = np.zeros((WIDTH, HEIGHT))

    def diffuse(self, diffuse=DIFFUSION_COEFFICENT):
        # Apply Gaussian filter for diffusion
        #self.p_array = gaussian_filter(self.p_array, sigma=DIFFUSION_COEFFICENT)
        pass

    def decay(self):
        self.p_array = self.p_array * DECAY

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
        pass

    def move(self):
        # Update agent's position based on heading and speed
        self.speed = SPEED
        new_x = self.x + self.speed * np.cos(self.heading)
        new_y = self.y + self.speed * np.sin(self.heading)

        # Bounce off the borders with an angle of reflection
        if new_x < 0 or new_x > WIDTH:
            self.heading = np.pi - self.heading  # Reflect across the y-axis
            new_x = np.clip(new_x, 0, WIDTH)
        if new_y < 0 or new_y > HEIGHT:
            self.heading = -self.heading  # Reflect across the x-axis
            new_y = np.clip(new_y, 0, HEIGHT)

        # Update the agent's position
        self.x = new_x
        self.y = new_y

    def deposit_pheromone(self, pheromone_array):
        pass

