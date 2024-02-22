import numpy as np
from scipy.ndimage import gaussian_filter

import slime_mold_simulation.config as config
#from numba import jit

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
        y = np.random.uniform(400, 600, AGENT_NUMBER)
        x = np.random.uniform(400, 600, AGENT_NUMBER)
        heading = np.random.uniform(0, 2 * np.pi, AGENT_NUMBER)
        self.agenten = np.column_stack((y, x, heading))


# Applying a gaussian filter to the array, so that the pheromones within the array diffuse
def diffuse(p_array):
    return gaussian_filter(p_array, sigma=DIFFUSION_COEFFICENT)


#@jit
# Applying a fading to the array, so that the pheromones within the array decay
def decay(p_array):
    return p_array * DECAY


#@jit
# Update possible angles
def get_sensors(agents, SENSOR_ANGLE=SENSOR_ANGLE, AGENT_NUMBER=AGENT_NUMBER):
    # Prepare anlges for each of agents sensores / no randomenes on angles wtf
    angle_left = agents[:, 2] - SENSOR_ANGLE
    angle_main = agents[:, 2]
    angle_right = agents[:, 2] + SENSOR_ANGLE

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


def get_pheromone_value_at(p_array, sensors, HEIGHT=HEIGHT, WIDTH=WIDTH, AGENT_NUMBER=AGENT_NUMBER):
    # Initialize the sensor_values array
    sensor_values = np.zeros((AGENT_NUMBER, len(sensors)))
    # Iterate over each sensor to get pheromone values
    for idx, sensor in enumerate(sensors):
        # Calculate the indices, ensuring they are within bounds
        y = np.clip(np.round(sensor[0]).astype(int), 0, HEIGHT - 1)
        x = np.clip(np.round(sensor[1]).astype(int), 0, WIDTH - 1)
        # Fill the sensor_values array with the pheromone value at the sensor's location
        sensor_values[:, idx] = p_array[y, x]
    return sensor_values


#@jit
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


#@jit
def move(agents, parray, SPEED=SPEED):
    # agents = angle_adjustment(agents)
    # Update agent's position based on heading=agents[:, 2] and
    agents[:, 0] = agents[:, 0] + SPEED * np.sin(agents[:, 2])
    agents[:, 1] = agents[:, 1] + SPEED * np.cos(agents[:, 2])
    agents = reflect_boundary(agents)
    return agents


def deposit_pheromone(p_array, agents, HEIGHT=HEIGHT, WIDTH=WIDTH):
    # Round coordinates to the nearest integers and clip to array bounds
    y_idx = np.clip(np.round(agents[:, 0]).astype(int), 0, HEIGHT - 1)
    x_idx = np.clip(np.round(agents[:, 1]).astype(int), 0, WIDTH - 1)
    # Deposit pheromone at the rounded position
    p_array[y_idx, x_idx] = p_array[y_idx, x_idx] + 1
    return p_array


#@jit
def rotate_towards_sensor(
    agents, sensor_values, sensors_angles, SENSOR_ANGLE, AGENT_NUMBER=AGENT_NUMBER, ROTATION_SPEED=ROTATION_SPEED
):
    for i in range(AGENT_NUMBER):
        pheromone_left = sensor_values[i, 0]
        pheromone_main = sensor_values[i, 1]
        pheromone_right = sensor_values[i, 2]

        if pheromone_left >= pheromone_main > pheromone_right:
            # Calculate the target angle between angle_left and angle_main
            target_angle = sensors_angles[i, 0]
        elif pheromone_right >= pheromone_main > pheromone_left:
            # Calculate the target angle between angle_right and angle_main
            target_angle = sensors_angles[i, 2]
        else:
            # If the pheromone values at sensor_right and sensor_left are the same, no heading change
            target_angle = agents[i, 2]

        # Smoothly adjust the agent's angle towards the target angle
        angle_difference = target_angle - agents[i, 2]

        agents[i, 2] += (ROTATION_SPEED * angle_difference) * SPEED
        # print(agents[i, 2])

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
