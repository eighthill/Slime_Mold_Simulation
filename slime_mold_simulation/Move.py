import math
from random import randint
import numpy as np
from scipy.ndimage import gaussian_filter
from numba import jit
from SlimeConfig import SlimeConfig

    

# this method updates the next move for each agent
@jit
def make_move(self, array):
    for agent in self.Agents_list:
        # the variable next_position contains: [x_coordinate, y_coordinate], angle
        next_position = self.get_best_move(array, agent)

        # Update the pheromone concentration at the agent's current position
        x, y = self.mapping_float_to_int([agent["float_x_pos"], agent["float_y_pos"]], array)
        array.world[x, y] += SlimeConfig.pheromone_value

        # Move the agent to the next position
        agent["float_x_pos"], agent["float_y_pos"] = next_position[0]
        agent["int_x_pos"], agent["int_y_pos"] = self.mapping_float_to_int(next_position[0], array)

        # Update the direction the agent is looking at after the move
        agent["movement_angle"] = next_position[1] + randint(-5, 5)
        # print(f"Updated Position - x: {agent['float_x_pos']}, y: {agent['float_y_pos']}")

@jit
def get_best_move(self, array, agent):
    possible_moves = self.get_next_moves(agent)

    # Get the pheromone values for each possible move
    pheromone_values = [array.world[tuple(self.mapping_float_to_int(move[0], array))] for move in possible_moves]

    # Find the move with the maximum pheromone concentration
    max_idx = np.argmax(pheromone_values)
    next_position = possible_moves[max_idx]

    return next_position

@jit
def get_next_moves(self, agent):
    possible_moves = []

    # Iterate over sensor angles
    for sensor_angle in [-self.sensor_angle, 0, self.sensor_angle]:
        angle = agent["movement_angle"] + sensor_angle

        x_new = agent["float_x_pos"] + self.speed * self.radius * math.cos(angle)
        y_new = agent["float_y_pos"] + self.speed * self.radius * math.sin(angle)

        # Reflect at the boundary if the new position is outside the array
        if not (0 <= x_new <= 1 and 0 <= y_new <= 1):
            x_new, y_new, _ = self.reflect_at_boundary(x_new, y_new, agent["float_x_pos"], agent["float_y_pos"])

        # Append the move to the list of possible moves
        possible_moves.append([[x_new, y_new], angle])

    return possible_moves

@jit
def reflect_at_boundary(self, x, y, x_pos, y_pos):
    # check if absolute value is greater than 1
    # if true, reflect point from subtracting *2 the result of a comparison (if statements)
    if abs(x) > 1:
        x = 2 * (x > 0) - x

    if abs(y) > 1:
        y = 2 * (y > 0) - y

    dx = x - x_pos
    dy = y - y_pos

    # Calculate new angle
    angle = math.atan2(dy, dx)

    return x, y, angle

@jit
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

@jit
# this method needs a list with 2 integer indices for a given array and calculates them to float coordinates
def mapping_int_to_float(self, coordinates, array):
    # 2 because of float has to be in [-1,1]
    float_world_size = 2
    new_coordinates = []

    for idx, val in enumerate(coordinates):
        coordinate = -1 + (2 * val / array.world.shape[idx])
        new_coordinates.append(coordinate)
    return new_coordinates