import math
from random import randint
import numpy as np
from scipy.ndimage import gaussian_filter
from Move import make_move, mapping_float_to_int, mapping_int_to_float, get_best_move, get_next_moves, reflect_at_boundary 
from SlimeConfig import SlimeConfig
import numpy as np
from numba.experimental import jitclass
from numba import types, jit, deferred_type

node_type = deferred_type()

pheromone_spec = [
    ('x_len', types.int32),
    ('y_len', types.int32),
    ('fading', types.float32),
    ('pheromone_value', types.float32),
    ('diffusion_coefficient', types.float32),
    ('world', types.float32[:, :])
]

@jitclass(pheromone_spec)
class PheromoneArray:
    def __init__(self, x_len=1000, y_len=1000, fading=0.97, pheromone_value=10, diffusion_coefficient=0.2):
        self.x_len = x_len
        self.y_len = y_len
        self.fading = fading
        self.pheromone_value = pheromone_value
        self.diffusion_coefficient = diffusion_coefficient
        self.world = np.zeros((x_len, y_len), dtype=np.float32)

    def update_pheromone(self, Agents):
        self.world = (self.world * self.fading).astype(float)
        for agent in Agents:
            x, y = agent["int_x_pos"], agent["int_y_pos"]
            self.world[x, y] = self.pheromone_value

        # Update pheromone concentration using Gaussian filter
        dt = 10  # Time step
        spread = np.sqrt(2 * self.diffusion_coefficient * dt)
        self.world = gaussian_filter(self.world, sigma=spread)


agent_spec = [
    ('Agents_list', types.List(types.float32)),
    ('num_agents', types.int32),
    ('sensor_angle', types.float32),
    ('size', types.int32),
    ('radius', types.float32),
    ('speed', types.float32)
]

@jitclass(agent_spec)
# the agent class creates a list with one dictionary for each agent
class Agent:
    def __init__(self, array, num_agents=1000, sensor_angle=0.33, size=15 , radius=0.4, speed=0.02):
        self.num_agents = num_agents
        self.sensor_angle = sensor_angle
        self.radius = radius
        self.speed = speed
        self.Agents_list = []
        
        

        center_x = array.world.shape[0] // 2
        center_y = array.world.shape[1] // 2
        angles = np.random.random(num_agents) * 2 * math.pi
        dst = np.random.random(num_agents) * radius

        for angle, d in zip(angles, dst):
            # Convert polar coordinates to Cartesian coordinates
            x = center_x + int(d * array.world.shape[0] * np.cos(angle))
            y = center_y + int(d * array.world.shape[1] * np.sin(angle))

            # Ensure the initial position is within the canvas bounds
            x = max(0, min(x, array.world.shape[0] - 1))
            y = max(0, min(y, array.world.shape[1] - 1))
            #print(f"Initial Position - x: {x}, y: {y}")
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
            
Agent.make_move = make_move
Agent.get_best_move = get_best_move
Agent.get_next_moves = get_next_moves
Agent.reflect_at_boundary = reflect_at_boundary
Agent.mapping_float_to_int = mapping_float_to_int
#Agent.mapping_int_to_float = mapping_int_to_float