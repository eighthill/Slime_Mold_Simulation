import math
from random import randint
import numpy as np

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