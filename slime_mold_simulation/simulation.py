import math
from random import randint
import numpy as np
from scipy.ndimage import gaussian_filter
from Move import sense, sense_and_move, mapping_float_to_int, mapping_int_to_float, reflect_at_boundary 
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

        # Update pheromone concentration using Gaussian filter
        dt = 0.0166  # Time step
        spread = np.sqrt(2 * self.diffusion_coefficient * dt)
        self.world = gaussian_filter(self.world, sigma=spread)

    def update_pheromone_at_position(self, x, y):
        # Assuming x and y are integers, if not, they should be converted before calling this method.
        # Add the pheromone value at the current position.
        self.world[x, y] += self.pheromone_value
        

# the agent class creates a list with one dictionary for each agent
class Agent:
    def __init__(self, x, y, movement_angle, sensor_distances=10.0, sensor_angles= 0.33, move_speed= 10.0, turn_speed = 10.0, random_move= 5):
        self.x = x
        self.y = y
        self.movement_angle = movement_angle
        self.sensor_distances = sensor_distances
        self.sensor_angles = sensor_angles
        self.move_speed = move_speed
        self.turn_speed = turn_speed
        self.random_move = random_move
        # Optionally, set the sense and sense_and_move methods as attributes if needed
        
    def update(self, pheromone_array):
        # Use the sense_and_move method to update the agent's position and orientation
        self.sense_and_move(pheromone_array.world, self.sensor_distances, self.sensor_angles, self.move_speed, self.turn_speed, self.x, self.y, self.movement_angle, pheromone_array)
        
        # Deposit a pheromone at the new position.
        pheromone_array.update_pheromone_at_position(int(self.x), int(self.y))
        
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
        } for x, y, angle in zip(x_positions, y_positions, movement_angles)]

        return agents
                
Agent.sense_and_move = sense_and_move
Agent.sense = sense

Agent.reflect_at_boundary = reflect_at_boundary
Agent.mapping_float_to_int = mapping_float_to_int
Agent.mapping_int_to_float = mapping_int_to_float