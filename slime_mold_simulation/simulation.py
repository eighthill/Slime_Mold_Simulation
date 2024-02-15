<<<<<<< HEAD
import math
from random import randint

import numpy as np
from scipy.ndimage import gaussian_filter

# Simulationparameters
WIDTH = 1000
HEIGHT = 1000
PHEROMONE_VALUE = 10
DECAY = 0.97
DIFFUSION_COEFFICENT = 0.2

# Agentparameters
AGENT_NUMBER = 1000
SENSOR_ANGLE = 0.33
RADIUS = 0.5
SPEED = 0.02


class PheromoneArray:
    def __init__(
        self,
        x_len=WIDTH,
        y_len=HEIGHT,
        fading=DECAY,
        pheromone_value=PHEROMONE_VALUE,
        diffusion_coefficient=DIFFUSION_COEFFICENT,
    ):
        self.world = np.zeros((x_len, y_len), dtype=float)
        self.fading = fading
        self.pheromone_value = pheromone_value
        self.diffusion_coefficient = diffusion_coefficient

    def update_pheromone(self, Agents):
        self.world = (self.world * self.fading).astype(float)
        for agent in Agents:
            x, y = agent["int_x_pos"], agent["int_y_pos"]
            self.world[x, y] = self.pheromone_value

        # Update pheromone concentration using Gaussian filter
        dt = 10  # Time step
        spread = np.sqrt(2 * self.diffusion_coefficient * dt)
        self.world = gaussian_filter(self.world, sigma=spread)


# the agent class creates a list with one dictionary for each agent
class Agent:
    def __init__(self, array, num_agents=AGENT_NUMBER, sensor_angle=SENSOR_ANGLE, radius=RADIUS, speed=SPEED):
        self.num_agents = num_agents
        self.sensor_angle = sensor_angle
        self.radius = radius
        self.speed = speed  # Neuer Parameter für die Geschwindigkeit
        self.Agents_list = []

        center_x = array.world.shape[0] // 2
        center_y = array.world.shape[1] // 2
        angles = np.random.random(num_agents) * 2 * math.pi
        dst = np.random.random(num_agents) * radius

        for angle, d in zip(angles, dst):
            # Convert polar coordinates to Cartesian coordinates
            x = center_x + int(d * array.world.shape[0] * np.cos(angle))
            y = center_y + int(d * array.world.shape[1] * np.sin(angle))

            float_x_pos, float_y_pos = self.mapping_int_to_float([x, y], array)
            movement_angle = np.random.uniform(0, 360)
            agent_dict = {
                "int_x_pos": x,
                "int_y_pos": y,
                "float_x_pos": float_x_pos,
                "float_y_pos": float_y_pos,
                "movement_angle": movement_angle,
                "speed": speed,  # Neues Attribut für die Geschwindigkeit
            }

            self.Agents_list.append(agent_dict)

    # this method updates the next move for each agent
    def make_move(self, array):
        for agent in self.Agents_list:
            # the variable next_position contains: [x_coordinate,y_coordinate], angle
            next_position = self.get_best_move(array, agent)

            # the coordinates are given as float
            agent["float_x_pos"], agent["float_y_pos"] = next_position[0]

            # here we have the indicies for the array for each agent,
            # maybe there is a way to not safe it because we actually have the information already within the float coordinates
            # and we can always calculate those to integers with the function mapping_float_to_int
            [agent["int_x_pos"], agent["int_y_pos"]] = self.mapping_float_to_int(next_position[0], array)

            # this is the direction the agent is looking at after the move
            agent["movement_angle"] = next_position[1] + randint(-5, 5)

    # this method compares all possible next positions for an agent to find the best option
    def get_best_move(self, array, agent):
        possible_moves = self.get_next_moves(agent)
        amount_of_pheromones_list = []

        # get the amount of pheromones for each possible move and add it to the list amount_of_pheromones_list
        for move in possible_moves:
            int_coordinats = self.mapping_float_to_int(move[0], array)
            value = array.world[int_coordinats[0], int_coordinats[1]]
            amount_of_pheromones_list.append(value)

        # find which of the possitions has the most pheremones
        # here we could implement a method that makes sure that the agents change there way,
        # if there amount of pheromones has crossed a given value
        max_val = max(amount_of_pheromones_list)
        max_idx = amount_of_pheromones_list.index(max_val)
        next_position = possible_moves[max_idx]

        return next_position

    # calculate new x and y coordinate by given startposition, angle and distance
    def get_next_moves(self, agent):
        possible_moves = []

        # here we have 3 sensores, we could add a loop that creates a variable number of sensores
        angles = [-self.sensor_angle + randint(0, 1), 0, self.sensor_angle + randint(0, 1)]
        for angle in angles:
            angle = agent["movement_angle"]

            x_new = agent["float_x_pos"] + self.speed * self.radius * math.cos(angle)
            y_new = agent["float_y_pos"] + self.speed * self.radius * math.sin(angle)

            if x_new > 1 or x_new < -1 or y_new > 1 or y_new < -1:
                # since agents can't leave the array, those lines calulate another angle and coordinates
                x_new, y_new, angle = self.reflect_at_boundary(x_new, y_new, agent["float_x_pos"], agent["float_y_pos"])

            # this list contains all possible next moves for one agent
            possible_moves.append([[x_new, y_new], angle])
        return possible_moves

    # method to reflect the object from the edge of the square
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

    # this method needs a list with 2 float coordinates and calculates them to integer indicies for an given array
    def mapping_float_to_int(self, coordinates, array):
        # 2 because of float has to be in [-1,1]
        float_world_size = 2
        new_coordinates = []

        for idx, val in enumerate(coordinates):
            coordinate = int((val + 1) / float_world_size * array.world.shape[idx])

            # ensure coordinate is within bounds
            coordinate = max(0, min(array.world.shape[idx] - 1, coordinate))
            new_coordinates.append(coordinate)
        return new_coordinates

    # this method needs a list with 2 integer indicies for an given array and calculates them to float coordinates
    def mapping_int_to_float(self, coordinates, array):
        # 2 because of float has to be in [-1,1]
        float_world_size = 2
        new_coordinates = []

        for idx, val in enumerate(coordinates):
            coordinate = -1 + (float_world_size * val / array.world.shape[idx])
            new_coordinates.append(coordinate)
        return new_coordinates
=======
import math
from random import randint
import numpy as np
from scipy.ndimage import gaussian_filter


class SlimeConfig:
    num_agents=1000
    fading=0.97
    pheromone_value=10
    diffusion_coefficient=0.2
    sensor_angle=0.33
    radius=0.5
    move_speed=0.02
    angles = np.random.random(num_agents) * 2 * math.pi
    sensor_size = 3
    
class PheromoneArray:
    def __init__(self, x_len=1000, y_len=1000, fading=0.97, pheromone_value=10, diffusion_coefficient=0.2):
        self.world = np.zeros((x_len, y_len), dtype=float)
        self.fading = fading
        self.pheromone_value = pheromone_value
        self.diffusion_coefficient = diffusion_coefficient

    def update_pheromone(self, Agents):
        self.world = (self.world * self.fading).astype(float)
        for agent in Agents:
            x, y = agent["int_x_pos"], agent["int_y_pos"]
            self.world[x, y] = self.pheromone_value

        # Update pheromone concentration using Gaussian filter
        dt = 10  # Time step
        spread = np.sqrt(4 * self.diffusion_coefficient * dt)
        self.world = gaussian_filter(self.world, sigma=spread)


# the agent class creates a list with one dictionary for each agent
class Agent:
    def __init__(self, array, num_agents=1000, sensor_angle=0.33, radius=0.5, speed=0.02):
        self.num_agents = num_agents
        self.sensor_angle = sensor_angle
        self.radius = radius
        self.speed = speed
        self.Agents_list = []

        center_x = array.world.shape[0] // 2
        center_y = array.world.shape[1] // 2

        # Generate uniformly distributed angles
        angles = np.linspace(0, 2 * np.pi, num_agents, endpoint=False)

        for angle in angles:
            # Calculate Cartesian coordinates based on the angle and radius
            x = center_x + int(center_x * radius * np.cos(angle))
            y = center_y + int(center_y * radius * np.sin(angle))

            # Ensure the initial position is within the canvas bounds
            x = max(0, min(x, array.world.shape[0] - 1))
            y = max(0, min(y, array.world.shape[1] - 1))
           # print(f"Initial Position - x: {x}, y: {y}")

            float_x_pos, float_y_pos = self.mapping_int_to_float([x, y], array)
            movement_angle = np.random.uniform(0, 2 * np.pi)

            agent_dict = {
                "int_x_pos": x,
                "int_y_pos": y,
                "float_x_pos": float_x_pos,
                "float_y_pos": float_y_pos,
                "movement_angle": movement_angle,
                "speed": speed,
            }

            self.Agents_list.append(agent_dict)

    # this method updates the next move for each agent
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
            print(f"Updated Position - x: {agent['float_x_pos']}, y: {agent['float_y_pos']}")

    def get_best_move(self, array, agent):
        possible_moves = self.get_next_moves(agent)

        # Get the pheromone values for each possible move
        pheromone_values = [array.world[tuple(self.mapping_float_to_int(move[0], array))] for move in possible_moves]

        # Find the move with the maximum pheromone concentration
        max_idx = np.argmax(pheromone_values)
        next_position = possible_moves[max_idx]

        return next_position

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

    def reflect_at_boundary(self, x, y, x_pos, y_pos):
        # Reflect at the boundary
        x = 2 * (x > 1) - x
        y = 2 * (y > 1) - y
        x = 2 * (x < 0) - x
        y = 2 * (y < 0) - y
        print(f"Reflected Position - x: {x}, y: {y}")
        # Calculate new angle
        dx = x - x_pos
        dy = y - y_pos
        angle = math.atan2(dy, dx)

        return x, y, angle

    # this method needs a list with 2 float coordinates and calculates them to integer indicies for an given array
    def mapping_float_to_int(self, coordinates, array):
        # 2 because of float has to be in [-1,1]
        float_world_size = 2
        new_coordinates = []

        for idx, val in enumerate(coordinates):
            coordinate = int((val + 1) / float_world_size * array.world.shape[idx])

            # ensure coordinate is within bounds
            coordinate = max(0, min(array.world.shape[idx] - 1, coordinate))
            new_coordinates.append(coordinate)
        return new_coordinates

    # this method needs a list with 2 integer indicies for an given array and calculates them to float coordinates
    def mapping_int_to_float(self, coordinates, array):
        # 2 because of float has to be in [-1,1]
        float_world_size = 2
        new_coordinates = []

        for idx, val in enumerate(coordinates):
            coordinate = -1 + (float_world_size * val / array.world.shape[idx])
            new_coordinates.append(coordinate)
        return new_coordinates
>>>>>>> b3387bdb388c298d0189c54489a1e568b4da1d1b
