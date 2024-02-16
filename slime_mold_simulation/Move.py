import math
from random import randint
import numpy as np
from scipy.ndimage import gaussian_filter
from numba import jit
from SlimeConfig import SlimeConfig

    
def sense_and_move(self, pheromone, sensor_distances, sensor_angles, move_speed, turn_speed, canvas_width, canvas_height):
    # Calculate sensor readings for forward, left, and right directions
    #print(f"Initial values - x: {self.x}, y: {self.y}, angle: {self.movement_angle}")
    weightForward = self.sense(pheromone, sensor_distances[0], 0)  # Assuming forward distance is the first in the list
    weightLeft = self.sense(pheromone, sensor_distances[0], np.radians(-33))
    weightRight = self.sense(pheromone, sensor_distances[0], np.radians(33))
    #print(f"Weights - Forward: {weightForward}, Left: {weightLeft}, Right: {weightRight}")

    # Calculate randomSteerStrength
    random_seed = ((self.x + self.y) * 0.0166 + self.movement_angle) * (2**32-1)
    #print(f"Random seed: {random_seed}")

   # np.random.seed(int(random_seed * 1000))
    randomSteerStrength = np.random.rand()

    # Adjust angle based on weights and random steer strength
    if weightForward < weightLeft and weightForward < weightRight:
        self.movement_angle += (randomSteerStrength - 0.5) * 2 * turn_speed * 0.0166
    elif weightRight > weightLeft:
        self.movement_angle -= randomSteerStrength * turn_speed * 0.0166
    elif weightLeft > weightRight:
        self.movement_angle += randomSteerStrength * turn_speed * 0.0166

    #print(f"Updated values - x: {self.x}, y: {self.y}, angle: {self.movement_angle}")

    
    # Update position based on movement_angle
    self.x += np.cos(self.movement_angle) * move_speed
    self.y += np.sin(self.movement_angle) * move_speed
    # Deposit pheromone at the new position
    pheromone_array.update_pheromone_at_position(int(self.x), int(self.y))
    self.reflect_at_boundary( canvas_width, canvas_height)
    # Ensure x and y are within canvas bounds
    self.x = np.clip(self.x + np.cos(self.movement_angle) * move_speed, 0, canvas_width - 1)
    self.y = np.clip(self.y + np.sin(self.movement_angle) * move_speed, 0, canvas_height - 1)
    
    #print(f"Final position - x: {self.x}, y: {self.y}")

def sense(self, pheromone, distance, angle):
    # Convert polar to cartesian
    dx = distance * np.cos(self.movement_angle + angle)
    dy = distance * np.sin(self.movement_angle + angle)
    sensed_x = int(self.x + dx)
    sensed_y = int(self.y + dy)
    # Ensure sensed coordinates are within bounds
    sensed_x = np.clip(sensed_x, 0, pheromone.shape[1] - 1)
    sensed_y = np.clip(sensed_y, 0, pheromone.shape[0] - 1)
    return pheromone[sensed_y, sensed_x]

def reflect_at_boundary(agent, width, height):
    # Reflect off vertical boundaries (left/right edges)
    if agent.x <= 0 or agent.x >= width:
        agent.movement_angle = np.pi - agent.movement_angle

    # Reflect off horizontal boundaries (top/bottom edges)
    if agent.y <= 0 or agent.y >= height:
        agent.movement_angle = -agent.movement_angle

    # Normalize the angle to ensure it's between 0 and 2*np.pi
    agent.movement_angle = agent.movement_angle % (2 * np.pi)
    
    # Update the agent's position based on the new angle, if necessary
    # This part may require adjustment based on how you apply movement based on the angle

# this method needs a list with 2 float coordinates and calculates them to integer indices for a given array
def mapping_float_to_int(self, coordinates, array):
    # 2 because of float has to be in [-1,1]
    float_world_size = 2
    new_coordinates = []

    for idx, val in enumerate(coordinates):
        coordinate = int((val + 1) * 0.5 * array.world.shape[idx])

        # ensure coordinate is within bounds
        coordinate = max(0, min(array.world.shape[idx] - 1, coordinate))
        new_coordinates.append(coordinate)
    return new_coordinates

# this method needs a list with 2 integer indices for a given array and calculates them to float coordinates
def mapping_int_to_float(self, coordinates, array):
    # 2 because of float has to be in [-1,1]
    float_world_size = 2
    new_coordinates = []

    for idx, val in enumerate(coordinates):
        coordinate = -1 + (2 * val / array.world.shape[idx])
        new_coordinates.append(coordinate)
    return new_coordinates