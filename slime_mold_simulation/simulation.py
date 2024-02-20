import math

import numpy as np
from scipy.ndimage import gaussian_filter

import config

WIDTH = config.WIDTH
HEIGHT = config.HEIGHT
DECAY = config.DECAY
DIFFUSION_COEFFICENT = config.DIFFUSION_COEFFICENT
AGENT_NUMBER = config.AGENT_NUMBER
SPEED = config.SPEED
SENSOR_DISTANCE = config.SENSOR_DISTANCE
ROTATION_SPEED = config.ROTATION_SPEED
SENSOR_ANGLE = config.SENSOR_ANGLE


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
        y = np.random.uniform(0, HEIGHT, AGENT_NUMBER)
        x = np.random.uniform(0, WIDTH, AGENT_NUMBER)
        heading = np.random.uniform(0, 2 * np.pi, AGENT_NUMBER)
        self.agenten = np.column_stack((y, x, heading))


# Applying a gaussian filter to the array, so that the pheromones within the array diffuse
def diffuse(p_array):
    return gaussian_filter(p_array, sigma=DIFFUSION_COEFFICENT)


# @jit
# Applying a fading to the array, so that the pheromones within the array decay
def decay(p_array):
    return p_array * DECAY


# @jit
# Update possible angles
def get_sensors(agents, SENSOR_ANGLE=SENSOR_ANGLE, AGENT_NUMBER=AGENT_NUMBER):
    # Prepare anlges for each of agents sensores, with a little randomness to create more natural behavior
    angle_left = agents[:, 2] - SENSOR_ANGLE + np.random.uniform(-0.3 * np.pi, 0.3 * np.pi, AGENT_NUMBER)
    angle_main = agents[:, 2]
    angle_right = agents[:, 2] + SENSOR_ANGLE + np.random.uniform(-0.3 * np.pi, 0.3 * np.pi, AGENT_NUMBER)

    # Prepare y and x coordinates for the position of each sensor for each agent
    sensor_left = [
        agents[:, 0] + SENSOR_DISTANCE * np.sin(angle_left),
        agents[:, 1] + SENSOR_DISTANCE * np.cos(angle_left),
    ]
    sensor_main = [
        agents[:, 0] + SENSOR_DISTANCE * np.sin(angle_main),
        agents[:, 1] + SENSOR_DISTANCE * np.cos(angle_main),
    ]
    sensor_right = [
        agents[:, 0] + SENSOR_DISTANCE * np.sin(angle_right),
        agents[:, 1] + SENSOR_DISTANCE * np.cos(angle_right),
    ]

    # create a list with all sensor coordinates and an array with all possible angles for agents
    sensors = [sensor_left, sensor_main, sensor_right]
    sensors_angles = np.column_stack((angle_left, angle_main, angle_right))
    return sensors, sensors_angles


"""
def get_pheromone_value_at(p_array, sensors,AGENT_NUMBER=AGENT_NUMBER):
    sensor_values = np.zeros((AGENT_NUMBER, len(sensors)))
    for idx, sensor in enumerate(sensors):
        try:
            # Clip x and y to ensure they are within the bounds of the pheromone array
            y = np.round(sensor[0]).astype(int), 0, HEIGHT - 1
            x = np.round(sensor[1]).astype(int), 0, WIDTH - 1
            sensor_values[:, idx] = p_array[y, x]
        except:
            sensor_values[:, idx] = 0
    return sensor_values
"""


def get_pheromone_value_at(p_array, sensors, AGENT_NUMBER=AGENT_NUMBER):
    sensor_values = np.zeros((AGENT_NUMBER, len(sensors)))
    for idx, sensor in enumerate(sensors):
        # Clip x and y to ensure they are within the bounds of the pheromone array
        y = np.round(sensor[0]).astype(int)
        x = np.round(sensor[1]).astype(int)
        mask_HEIGHT = np.logical_and(y >= 0, y <= HEIGHT - 1)
        mask_WIDTH = np.logical_and(x >= 0, x <= WIDTH - 1)
        mask_combined = np.logical_and(mask_HEIGHT, mask_WIDTH)
        y = y[mask_combined]
        x = x[mask_combined]
        sensor_values[:, idx][mask_combined] = p_array[y, x]
    return sensor_values


def angle_adjustment(agents):
    mask_to_low = agents[:, 2] < 0
    mask_to_big = agents[:, 2] > 2 * np.pi
    agents[mask_to_low, 2] = agents[mask_to_low, 2] + 2 * np.pi
    agents[mask_to_big, 2] = agents[mask_to_big, 2] - 2 * np.pi
    return agents


# @jit


def reflect_boundary(agents):
    mask_top = agents[:, 0] < 0
    mask_bottom = agents[:, 0] > HEIGHT - 1
    mask_left = agents[:, 1] < 0
    mask_right = agents[:, 1] > WIDTH - 1

    agents[mask_top, 0] = -agents[mask_top, 0] + 1 + 2 * np.random.rand(np.sum(mask_top))
    agents[mask_bottom, 0] = 2 * HEIGHT - agents[mask_bottom, 0] - 1 - 2 * np.random.rand(np.sum(mask_bottom))
    agents[mask_left, 1] = -agents[mask_left, 1] + 1 + 2 * np.random.rand(np.sum(mask_left))
    agents[mask_right, 1] = 2 * WIDTH - agents[mask_right, 1] - 1 - 2 * np.random.rand(np.sum(mask_right))

    # Reflect the heading if the agent hits a boundary
    agents[mask_top, 2] = np.pi - agents[mask_top, 2] + np.random.uniform(-math.pi / 4, math.pi / 4, np.sum(mask_top))
    agents[mask_bottom, 2] = (
        np.pi - agents[mask_bottom, 2] + np.random.uniform(-math.pi / 4, math.pi / 4, np.sum(mask_bottom))
    )
    agents[mask_left, 2] = (
        np.pi - agents[mask_left, 2] + np.random.uniform(-math.pi / 4, math.pi / 4, np.sum(mask_left))
    )
    agents[mask_right, 2] = (
        np.pi - agents[mask_right, 2] + np.random.uniform(-math.pi / 4, math.pi / 4, np.sum(mask_right))
    )
    return agents


# @jit
def move(agents, SPEED=SPEED):
    # agents = angle_adjustment(agents)
    # Update agent's position based on heading=agents[:, 2] and
    agents[:, 0] = agents[:, 0] + SPEED * np.sin(agents[:, 2])
    agents[:, 1] = agents[:, 1] + SPEED * np.cos(agents[:, 2])
    agents = reflect_boundary(agents)
    agents = angle_adjustment(agents)
    return agents


def deposit_pheromone(p_array, agents, HEIGHT=HEIGHT, WIDTH=WIDTH):
    # Round coordinates to the nearest integers and clip to array bounds
    y_idx = np.clip(np.round(agents[:, 0]).astype(int), 0, HEIGHT - 1)
    x_idx = np.clip(np.round(agents[:, 1]).astype(int), 0, WIDTH - 1)
    # Deposit pheromone at the rounded position
    p_array[y_idx, x_idx] = p_array[y_idx, x_idx] + 1
    return p_array


# @jit#@jit
def rotate_towards_sensor_simple(
    agents, sensor_values, sensors_angles, AGENT_NUMBER=AGENT_NUMBER, ROTATION_SPEED=ROTATION_SPEED
):
    if ROTATION_SPEED > 1 or ROTATION_SPEED < 1:
        np.clip(ROTATION_SPEED, 0, 1)
    highest_pheromons = np.argmax(sensor_values, axis=1)

    highest_value_left = sensor_values[:, 0] == highest_pheromons
    highest_value_mid = sensor_values[:, 1] == highest_pheromons
    highest_value_right = sensor_values[:, 2] == highest_pheromons

    # Create a combined condition
    combined_all = np.logical_and(highest_value_left, highest_value_mid, highest_value_right)
    combined_left_mid = np.logical_and(highest_value_left, highest_value_mid)
    combined_left_right = np.logical_and(highest_value_left, highest_value_right)
    combined_mid_right = np.logical_and(highest_value_mid, highest_value_right)

    idx_angles = np.zeros((AGENT_NUMBER, 1))
    numbers = [0, 2]
    random_l_r = np.random.choice(numbers, (idx_angles[combined_left_right].shape[0], 1))
    random_all = np.random.randint(0, 3, (idx_angles[combined_all].shape[0], 1))
    random_l_m = np.random.randint(0, 2, (idx_angles[combined_left_mid].shape[0], 1))
    random_m_r = np.random.randint(1, 3, (idx_angles[combined_mid_right].shape[0], 1))

    # masked_left = sensor_values[highest_value_left]
    idx_angles[highest_value_mid] = 1
    idx_angles[highest_value_right] = 2
    idx_angles[combined_left_mid] = random_l_m
    idx_angles[combined_mid_right] = random_m_r
    idx_angles[combined_left_right] = random_l_r
    idx_angles[combined_all] = random_all
    idx_angles = idx_angles.astype(int)
    # agents[:, 2] = sensors_angles[idx_angles] * ROTATION_SPEED

    # Accessing elements from sensors_angles using idx_angles
    selected_angles = sensors_angles[np.arange(len(idx_angles)), idx_angles[:, 0]]

    # Applying ROTATION_SPEED
    agents[:, 2] = selected_angles
    return agents


def main(parray, agnet):
    parray = diffuse(parray)
    parray = decay(parray)
    sensors, sensors_angles = get_sensors(agnet)
    sensor_values = get_pheromone_value_at(parray, sensors)
    agnet = rotate_towards_sensor_simple(agnet, sensor_values, sensors_angles)
    agnet = move(agnet)
    parray = deposit_pheromone(parray, agnet)
    return parray, agnet
