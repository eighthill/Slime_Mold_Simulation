import math
from random import randint
import numpy as np
from scipy.ndimage import gaussian_filter
#from Move import sense, sense_and_move, mapping_float_to_int, mapping_int_to_float, reflect_at_boundary 
from SlimeConfig import SlimeConfig

    
class PheromoneArray:
    def __init__(self, x_len=1100, y_len=1100, fading=0.97, pheromone_value=2, diffusion_coefficient=0.1):
        self.world = np.zeros((x_len, y_len), dtype=float)
        self.fading = fading
        self.pheromone_value = pheromone_value
        self.diffusion_coefficient = diffusion_coefficient

    def update_pheromone(self, Agents):
        self.world = (self.world * self.fading).astype(float)
        for agent in Agents:
            x, y = int(agent.x), int(agent.y)
            self.world[x, y] = self.pheromone_value

        dt = 0.0166  # Time step for diffusion
        spread = np.sqrt(2 * self.diffusion_coefficient * dt)
        self.world = gaussian_filter(self.world, sigma=spread)

    def update_pheromone_at_position(self, x, y):
        self.world[x, y] += self.pheromone_value

class Agent:
    def __init__(self, x, y, movement_angle, sensor_distances=10.0, sensor_angles=0.33, move_speed=10.0, turn_speed=10.0, random_move=5, pheromone_array=None):
        self.x = x
        self.y = y
        self.movement_angle = movement_angle
        self.sensor_distances = sensor_distances
        self.sensor_angles = sensor_angles
        self.move_speed = move_speed
        self.turn_speed = turn_speed
        self.random_move = random_move
        self.pheromone_array = pheromone_array

    def update(self):
        self.sense_and_move()
        self.pheromone_array.update_pheromone_at_position(int(self.x), int(self.y))
        
    
    def sense_and_move(self):
        front_concentration = self.sense(self.sensor_distances, 0, self.sensor_size)
        left_concentration = self.sense(self.sensor_distances, -self.sensor_angles, self.sensor_size)
        right_concentration = self.sense(self.sensor_distances, self.sensor_angles, self.sensor_size)

        # Calculate random steer strength
        random_seed = ((self.x + self.y) * 0.0166 + self.movement_angle) * (2**32-1)
        np.random.seed(int(random_seed * 1000))
        randomSteerStrength = np.random.rand()

        # Decision logic incorporating random steer strength
        if left_concentration > front_concentration and left_concentration > right_concentration:
            self.movement_angle -= self.turn_speed * randomSteerStrength
        elif right_concentration > front_concentration and right_concentration > left_concentration:
            self.movement_angle += self.turn_speed * randomSteerStrength
        else:
            # When moving forward, add a slight random variation to the movement angle
            self.movement_angle += (randomSteerStrength - 0.5) * self.turn_speed * 0.0166

        self.x += np.cos(self.movement_angle) * self.move_speed
        self.y += np.sin(self.movement_angle) * self.move_speed
        self.reflect_at_boundary()
        self.x = np.clip(self.x, 0, self.pheromone_array.world.shape[1] - 1)
        self.y = np.clip(self.y, 0, self.pheromone_array.world.shape[0] - 1)
        
    def sense(self, distance, angle, size):
        max_concentration = 0
        # Iterate over a range to simulate the sensor's coverage area
        for offset in np.linspace(-size / 2, size / 2, num=int(size)):
            dx = (distance * np.cos(self.movement_angle + angle)) + (offset * np.sin(self.movement_angle + angle))
            dy = (distance * np.sin(self.movement_angle + angle)) + (offset * np.cos(self.movement_angle + angle))
            sensed_x = int(self.x + dx)
            sensed_y = int(self.y + dy)
            sensed_x = np.clip(sensed_x, 0, self.pheromone_array.world.shape[1] - 1)
            sensed_y = np.clip(sensed_y, 0, self.pheromone_array.world.shape[0] - 1)
            concentration = self.pheromone_array.world[sensed_y, sensed_x]
            if concentration > max_concentration:
                max_concentration = concentration
        return max_concentration

    def reflect_at_boundary(self):
        if self.x <= 0 or self.x >= self.pheromone_array.world.shape[1]:
            self.movement_angle = np.pi - self.movement_angle
        if self.y <= 0 or self.y >= self.pheromone_array.world.shape[0]:
            self.movement_angle = -self.movement_angle
        self.movement_angle = self.movement_angle % (2 * np.pi)

    def mapping_float_to_int(self, coordinates, array):
        new_coordinates = []
        for idx, val in enumerate(coordinates):
            coordinate = int((val + 1) * 0.5 * array.world.shape[idx])
            coordinate = max(0, min(array.world.shape[idx] - 1, coordinate))
            new_coordinates.append(coordinate)
        return new_coordinates

    def mapping_int_to_float(self, coordinates, array):
        new_coordinates = []
        for idx, val in enumerate(coordinates):
            coordinate = -1 + (2 * val / array.world.shape[idx])
            new_coordinates.append(coordinate)
        return new_coordinates

    @staticmethod
    def initialize_agents(center_x, center_y, num_agents, radius, move_speed, world_x, world_y):
        angles = np.random.uniform(0, 2 * np.pi, num_agents)
        distances = np.sqrt(np.random.uniform(0, radius**2, num_agents))
        x_positions = center_x + (distances * np.cos(angles))
        y_positions = center_y + (distances * np.sin(angles))
        movement_angles = np.random.uniform(0, 2 * np.pi, num_agents)
        agents = [{
            "x": np.clip(x, 0, world_x - 1),
            "y": np.clip(y, 0, world_y - 1),
            "movement_angle": angle,
            "move_speed": move_speed,
            pheromone_array: pheromone_array_instance
        } for x, y, angle in zip(x_positions, y_positions, movement_angles)]
        return agents
                
#Agent.sense_and_move = sense_and_move
#Agent.sense = sense

#Agent.reflect_at_boundary = reflect_at_boundary
#Agent.mapping_float_to_int = mapping_float_to_int
#Agent.mapping_int_to_float = mapping_int_to_float