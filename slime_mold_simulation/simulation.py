import numpy as np
import math
from random import randint
from scipy.ndimage import gaussian_filter


class PheromoneArray:
    def __init__(self, x_len=1000, y_len=1000, fading=0.98999, pheromone_value=20, diffusion_coefficient=0.2):
        self.world = np.zeros((x_len, y_len), dtype=float)
        self.fading = fading
        self.pheromone_value = pheromone_value
        self.diffusion_coefficient = diffusion_coefficient

    def update_pheromone(self, Agents):
        # Fading der vorhandenen Pheromonspuren
        self.world *= self.fading

        # Platzieren von neuen Pheromonspuren an den Positionen der Agenten
        for agent in Agents:
            x, y = agent["int_x_pos"], agent["int_y_pos"]
            self.world[y, x] += self.pheromone_value  # Korrektur der Indizierung

        # Update pheromone concentration using Gaussian filter
        dt = 10  # Time step
        spread = np.sqrt(2 * self.diffusion_coefficient * dt)
        self.world = gaussian_filter(self.world, sigma=spread)


class Agent:
    def __init__(self, array, num_agents=1, sensor_angle=0.33, radius=0.5, speed=0.02):
        self.num_agents = num_agents
        self.sensor_angle = sensor_angle
        self.radius = radius
        self.speed = speed  
        self.Agents_list = []
        self.array = array

        # Spawn Agents in the center of the array
        center_x = array.world.shape[1] // 2  # Vertikale Dimension zuerst
        center_y = array.world.shape[0] // 2

        # Generate random angles for initial movement
        angles = np.random.random(num_agents) * 2 * math.pi

        for angle in angles:
            x = center_x
            y = center_y

            float_x_pos, float_y_pos = self.mapping_int_to_float([x, y])
            movement_angle = angle  

            agent_dict = {
                "int_x_pos": x,
                "int_y_pos": y,
                "float_x_pos": float_x_pos,
                "float_y_pos": float_y_pos,
                "movement_angle": movement_angle,
                "speed": speed,  
            }

            self.Agents_list.append(agent_dict)

    def make_move(self):
        for agent in self.Agents_list:
            # Get the next move for the agent
            next_position = self.get_best_move(agent)

            # Update the agent's position directly in integer coordinates
            agent["int_x_pos"], agent["int_y_pos"] = self.mapping_float_to_int(next_position[0])

            # Update the agent's movement angle
            agent["movement_angle"] = next_position[1] + randint(-5, 5)

            # Update the agent's float coordinates
            agent["float_x_pos"], agent["float_y_pos"] = next_position[0]


    def get_best_move(self, agent):
        possible_moves = self.get_next_moves(agent)
        amount_of_pheromones_list = []

        for move in possible_moves:
            int_coordinates = self.mapping_float_to_int(move[0])
            value = self.array.world[int_coordinates[1], int_coordinates[0]]  # Korrektur der Indizierung
            amount_of_pheromones_list.append(value)

        max_val = max(amount_of_pheromones_list)
        max_idx = amount_of_pheromones_list.index(max_val)
        next_position = possible_moves[max_idx]

        return next_position

    def get_next_moves(self, agent):
        possible_moves = []
        angles = [-self.sensor_angle, 0, self.sensor_angle]

        for angle_offset in angles:  
            angle = agent["movement_angle"] + angle_offset  
            x_new = agent["float_x_pos"] + self.speed * self.radius * math.cos(angle)
            y_new = agent["float_y_pos"] + self.speed * self.radius * math.sin(angle)

            if x_new > 1 or x_new < -1 or y_new > 1 or y_new < -1:
                x_new, y_new, angle = self.reflect_at_boundary(x_new, y_new, agent["float_x_pos"], agent["float_y_pos"])

            possible_moves.append([[x_new, y_new], angle])

        return possible_moves


    def reflect_at_boundary(self, x, y, x_pos, y_pos):
        if abs(x) > 1:
            x = 2 * (x > 0) - x

        if abs(y) > 1:
            y = 2 * (y > 0) - y

        dx = x - x_pos
        dy = y - y_pos

        angle = math.atan2(dy, dx)

        return x, y, angle

    def mapping_float_to_int(self, coordinates):
        float_world_size = 2
        new_coordinates = []

        for val in coordinates:
            coordinate = int((val + 1) / float_world_size * self.array.world.shape[0])  # Vertikale Dimension zuerst
            coordinate = max(0, min(self.array.world.shape[0] - 1, coordinate))
            new_coordinates.append(coordinate)

        return new_coordinates

    def mapping_int_to_float(self, coordinates):
        float_world_size = 2
        new_coordinates = []

        for idx, val in enumerate(coordinates):
            coordinate = -1 + (float_world_size * val / self.array.world.shape[idx])
            new_coordinates.append(coordinate)
        return new_coordinates
    
    def follow_pheromones(self):
        for agent in self.Agents_list:
            if self.detect_pheromones(agent):
                next_position = self.get_best_pheromone_move(agent)
                agent["float_x_pos"], agent["float_y_pos"] = next_position[0]
                [agent["int_x_pos"], agent["int_y_pos"]] = self.mapping_float_to_int(next_position[0])
                agent["movement_angle"] = next_position[1] + randint(-5, 5)
            else:
                self.make_move(agent)

    def detect_pheromones(self, agent):
        x, y = agent["int_x_pos"], agent["int_y_pos"]
        neighborhood = self.array.world[max(y - 1, 0):min(y + 2, self.array.world.shape[0]), max(x - 1, 0):min(x + 2, self.array.world.shape[1])]
        return np.max(neighborhood) > 0

    def get_best_pheromone_move(self, agent):
        possible_moves = self.get_next_moves(agent)
        amount_of_pheromones_list = []

        for move in possible_moves:
            int_coordinates = self.mapping_float_to_int(move[0])
            value = self.array.world[int_coordinates[1], int_coordinates[0]]  # Korrektur der Indizierung
            amount_of_pheromones_list.append(value)

        max_val = max(amount_of_pheromones_list)
        max_idx = amount_of_pheromones_list.index(max_val)
        next_position = possible_moves[max_idx]

        return next_position
