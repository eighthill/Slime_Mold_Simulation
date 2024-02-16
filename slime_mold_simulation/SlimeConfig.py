import math
from random import randint
import numpy as np

class SlimeConfig:
    num_agents=1000
    fading=0.97
    pheromone_value=10
    diffusion_coefficient=0.2
    sensor_angles=[0.33]
    radius=0.5
    move_speed = 5.0
    turn_speed = 5.0
    sensor_size = 20
    sensor_distances = [10.0]