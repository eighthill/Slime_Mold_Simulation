import numpy as np


# from numba import jit 
from scipy.ndimage import gaussian_filter
import sys
from pathlib import Path 

project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from cfg_sim.world_cfg import *


WIDTH = SlimeConfig.WIDTH
HEIGHT = SlimeConfig.HEIGHT
DECAY = SlimeConfig.DECAY
DIFFUSION_COEFFICENT = SlimeConfig.DIFFUSION_COEFFICENT
AGENT_NUMBER = SlimeConfig.AGENT_NUMBER
SPEED = SlimeConfig.SPEED
SENSOR_DISTANCE = SlimeConfig.SENSOR_DISTANCE
ROTATION_SPEED = SlimeConfig.ROTATION_SPEED
SENSOR_ANGLE = SlimeConfig.SENSOR_ANGLE
SPAWN_RADIUS = SlimeConfig.SPAWN_RADIUS


# Class creates an array "p_array" where the pheromones of the agents can be placed.
# It is the world in witch the agents are getting informations from to decide where to go.
class PheromoneArray:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.p_array = np.zeros((HEIGHT, WIDTH))


# Class creates an array "agenten" with informations about the agents. where each row represents an agent.
# colum 0 = y coordinate, colum 1 = x coordinate and colum 2 = the angle in which the agents is heading to.
class Agent:
    def __init__(self):
        current_agent_number = SlimeConfig.AGENT_NUMBER
        heading = np.random.uniform(0, 2 * np.pi, current_agent_number)
        center_y, center_x = SlimeConfig.HEIGHT / 2, SlimeConfig.WIDTH / 2

        # Random angles for circular distribution
        angle = np.random.uniform(0, 2 * np.pi, current_agent_number)

        # Varying radius for each agent to create an offset within a circular area
        radius = np.sqrt(np.random.uniform(0, 1, current_agent_number)) * SPAWN_RADIUS

        y = center_y + radius * np.sin(angle)
        x = center_x + radius * np.cos(angle)

        # Spawn the agents in a square area
        y = np.random.uniform(HEIGHT * 0.4, HEIGHT * 0.6, current_agent_number)
        x = np.random.uniform(WIDTH * 0.4, WIDTH * 0.6, current_agent_number)

        # Calculate heading towards the center with noise
        heading = np.arctan2(center_y - y, center_x - x) + np.random.uniform(-5, 5, current_agent_number)

        self.agenten = np.column_stack((y, x, heading))


# Applying a gaussian filter to the array, so that the pheromones within the array diffuse
def diffuse(p_array):
    current_diff = SlimeConfig.DIFFUSION_COEFFICENT

    # print(current_diff)
    return gaussian_filter(p_array, sigma=current_diff)


# @jit
# Applying a fading to the array, so that the pheromones within the array decay
def decay(p_array):
    current_decay = SlimeConfig.DECAY
    # print(current_decay)
    return p_array * current_decay


# @jit
# Update possible angles
def get_sensors(agents, SENSOR_ANGLE=SENSOR_ANGLE, AGENT_NUMBER=AGENT_NUMBER):
    # Prepare anlges for each of agents sensores / no randomenes on angles wtf
    current_sen_dis = SlimeConfig.SENSOR_DISTANCE
    current_sen_angle = SlimeConfig.SENSOR_ANGLE
    angle_left = agents[:, 2] - current_sen_angle
    angle_main = agents[:, 2]
    angle_right = agents[:, 2] + current_sen_angle

    # Prepare y and x coordinates for the position of each sensor for each agent
    sensor_left = [
        agents[:, 0] + current_sen_dis * np.sin(angle_left),
        agents[:, 1] + current_sen_dis * np.cos(angle_left),
    ]
    sensor_main = [
        agents[:, 0] + current_sen_dis * np.sin(angle_main),
        agents[:, 1] + current_sen_dis * np.cos(angle_main),
    ]
    sensor_right = [
        agents[:, 0] + current_sen_dis * np.sin(angle_right),
        agents[:, 1] + current_sen_dis * np.cos(angle_right),
    ]

    # create a list with all sensor coordinates and an array with all possible angles for agents
    sensors = [sensor_left, sensor_main, sensor_right]
    sensors_angles = np.column_stack((angle_left, angle_main, angle_right))
    return sensors, sensors_angles


def get_pheromone_value_at(p_array, sensors, AGENT_NUMBER=AGENT_NUMBER):
    current_agent_number = SlimeConfig.AGENT_NUMBER
    sensor_values = np.zeros((current_agent_number, len(sensors)))
    for idx, sensor in enumerate(sensors):
        try:
            # Round x and y coordinates to the nearest integers and clip them to array bounds
            y = np.clip(np.round(sensor[0]).astype(int), 0, HEIGHT - 1)
            x = np.clip(np.round(sensor[1]).astype(int), 0, WIDTH - 1)
            sensor_values[:, idx] = p_array[y, x]
        except sensor_values:
            sensor_values[:, idx] = 0
    return sensor_values


# @jit
def reflect_boundary(agents):
    mask_top = agents[:, 0] < 0
    mask_bottom = agents[:, 0] > HEIGHT - 1
    mask_left = agents[:, 1] < 0
    mask_right = agents[:, 1] > WIDTH - 1

    # vertical boundary
    agents[mask_top | mask_bottom, 0] = np.clip(agents[mask_top | mask_bottom, 0], 0, HEIGHT - 1)
    agents[mask_top | mask_bottom, 2] = 2 * np.pi - agents[mask_top | mask_bottom, 2]

    # horizontal boundary
    agents[mask_left | mask_right, 1] = np.clip(agents[mask_left | mask_right, 1], 0, WIDTH - 1)
    agents[mask_left | mask_right, 2] = np.pi - agents[mask_left | mask_right, 2]
    return agents


# @jit
def move(agents, parray, SPEED=SPEED):
    current_speed = SlimeConfig.SPEED
    agents[:, 0] = agents[:, 0] + current_speed * np.sin(agents[:, 2])
    agents[:, 1] = agents[:, 1] + current_speed * np.cos(agents[:, 2])
    agents = reflect_boundary(agents)
    return agents


def deposit_pheromone(p_array, agents, HEIGHT=HEIGHT, WIDTH=WIDTH):
    # Round coordinates to the nearest integers and clip to array bounds
    y_idx = np.clip(np.round(agents[:, 0]).astype(int), 0, HEIGHT - 1)
    x_idx = np.clip(np.round(agents[:, 1]).astype(int), 0, WIDTH - 1)
    # Deposit pheromone at the rounded position
    p_array[y_idx, x_idx] = p_array[y_idx, x_idx] + 1
    return p_array


# @jit
def rotate_towards_sensor(agents, sensor_values, sensors_angles, SENSOR_ANGLE):
    # Assuming SENSOR_ANGLE, AGENT_NUMBER, ROTATION_SPEED are globally defined or passed as parameters
    current_agent_number = SlimeConfig.AGENT_NUMBER
    current_rotta_speed = SlimeConfig.ROTATION_SPEED
    current_sen_angle = SlimeConfig.SENSOR_ANGLE
    current_time_step = SlimeConfig.TIMESTEP

    angle_left, angle_right = sensors_angles[:, 0], sensors_angles[:, 2]  # Transpose for easy unpacking


    # Calculate pheromone differences
    # print(sensor_values[:, 0])
    pheromone_diff_left = sensor_values[:, 0] >= sensor_values[:, 1]
    pheromone_diff_right = sensor_values[:, 2] >= sensor_values[:, 1]

    # Determine rotation direction
    rotate_left = pheromone_diff_left & (sensor_values[:, 0] > sensor_values[:, 2])
    rotate_right = pheromone_diff_right & (sensor_values[:, 2] > sensor_values[:, 0])
    rotate_random = np.logical_and(pheromone_diff_left, pheromone_diff_right)

    # Calculate target angle based on rotation direction

    target_angle = np.where(
        rotate_random,
        np.where(np.random.rand(current_agent_number) < 0.5, angle_left, angle_right),
        np.where(rotate_left, angle_left, np.where(rotate_right, angle_right, agents[:, 2])),
    )


    # Calculate random steering strength
    randomSteerStrength = np.random.rand(current_agent_number)

    # Adjust agents' angles
    angle_difference = target_angle - agents[:, 2]
    adjusted_angle = agents[:, 2] + (
        (current_rotta_speed * randomSteerStrength - 0.5) * angle_difference * current_sen_angle * current_time_step
    )

    # Normalize angles to range [0, 2π]
    normalized_angle = np.mod(adjusted_angle, 2 * np.pi)
    agents[:, 2] = normalized_angle

    return agents


def main(parray, agent):

    sensors, sensors_angles = get_sensors(agent)
    sensor_values = get_pheromone_value_at(parray, sensors)
    agent = rotate_towards_sensor(agent, sensor_values, sensors_angles, SENSOR_ANGLE)
    agent = move(agent, parray)
    parray = deposit_pheromone(parray, agent)

    parray = diffuse(parray)
    parray = decay(parray)
    return parray, agent
