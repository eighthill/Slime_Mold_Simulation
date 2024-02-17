import math
from random import choice, randint
from numba import jit
from scipy.stats import rankdata
import numpy as np
from scipy.ndimage import gaussian_filter
import time

# Put the global parameters in a seperate file for visualization?
# Simulationparameters
WIDTH = 1000
HEIGHT = 1000
DECAY = 0.95
DIFFUSION_COEFFICENT = 0.5

# Agentparameters
AGENT_NUMBER = 100000
SENSOR_ANGLE = 0.33
SPEED = 2
THRESHOLD = 0.1  # Adjust based on your simulation
ROTATION_SPEED = 1
SENSOR_DISTANCE = 10  # this is the radius


class PheromoneArray:
    def __init__(self, width=WIDTH, height=HEIGHT):
        self.width = WIDTH
        self.height = HEIGHT
        self.p_array = np.zeros((WIDTH, HEIGHT))


# the agent class creates a list with one dictionary for each agent
class Agent:
    def __init__(self, AGENT_NUMBER=AGENT_NUMBER, WIDTH=WIDTH, HEIGHT=HEIGHT):
        self.sensor_distance = SENSOR_DISTANCE  # Distance from agent to sensor
        self.rotation_speed = ROTATION_SPEED
        # self.threshold = THRESHOLD
        x = np.random.uniform(WIDTH * 0.5, WIDTH * 0.6, AGENT_NUMBER)
        y = np.random.uniform(HEIGHT * 0.5, HEIGHT * 0.6, AGENT_NUMBER)
        heading = np.random.uniform(0, 2 * math.pi, AGENT_NUMBER)
        self.agents = np.column_stack((x, y, heading))


# @jit
def update_pheromones(p_array, diffuse=DIFFUSION_COEFFICENT, decay=DECAY):
    # def diffuse(p_array, diffuse=DIFFUSION_COEFFICENT):
    # def decay(self, decay=DECAY):
    # Apply Gaussian filter for diffusion
    p_array = gaussian_filter(p_array, sigma=DIFFUSION_COEFFICENT)
    p_array = p_array * decay
    return p_array


# @jit
def get_pheromone_value_at(p_array, sensors, AGENT_NUMBER, width=WIDTH, height=HEIGHT):
    pheromone_values = np.zeros((AGENT_NUMBER, len(sensors)))
    for idx, sensor in enumerate(sensors):
        # Clip x and y to ensure they are within the bounds of the pheromone array
        x = np.clip(np.round(sensor[0]).astype(int), 0, width - 1)
        y = np.clip(np.round(sensor[1]).astype(int), 0, height - 1)
        pheromone_values[:, idx] = p_array[y, x]  # Werte an pheromone_values anhängen
    return pheromone_values


# @jit
def rotate_towards_sensor(p_array, agents, SENSOR_DISTANCE, rotation_speed=ROTATION_SPEED):
    # Define sensor positions directly in the constructor
    sensor_left = [
        agents[:, 0] + SENSOR_DISTANCE * np.cos(agents[:, 2] - SENSOR_ANGLE),
        agents[:, 1] + SENSOR_DISTANCE * np.sin(agents[:, 2] - SENSOR_ANGLE),
    ]
    main_sensor = [
        agents[:, 0] + SENSOR_DISTANCE * np.cos(agents[:, 2]),
        agents[:, 1] + SENSOR_DISTANCE * np.sin(agents[:, 2]),
    ]
    sensor_right = [
        agents[:, 0] + SENSOR_DISTANCE * np.cos(agents[:, 2] + SENSOR_ANGLE),
        agents[:, 1] + SENSOR_DISTANCE * np.sin(agents[:, 2] + SENSOR_ANGLE),
    ]

    # Combine sensor positions into a numpy array
    sensors = [sensor_left, main_sensor, sensor_right]
    sensors_angles = [-SENSOR_ANGLE, 0, SENSOR_ANGLE]
    sensor_values = get_pheromone_value_at(p_array, sensors, len(agents))

    selected_angles = []
    for row in sensor_values:
        sensor_ranking = rankdata(row, method="min")

        if np.count_nonzero(sensor_ranking == 1) == 1:
            idx = np.where(sensor_ranking == 1)[0][0]
        else:
            # if we want the Agents to choose a point between two sensores that both have the highest value of pheromones
            # then we have to change code here so that not indecies are stored but the new angle is calculated here already
            indices_of_ones = np.where(sensor_ranking == 1)[0]
            idx = choice(indices_of_ones)

        selected_angles.append(sensors_angles[idx])

    # Adjust heading towards the sensors with matrix operations
    agents[:, 2] = agents[:, 2] + selected_angles * rotation_speed


# @jit
def move(agents, width=WIDTH, height=HEIGHT, speed=SPEED):
    # Update agent's position based on heading and speed
    new_x = agents[:, 0] + speed * np.cos(agents[:, 2])
    new_y = agents[:, 1] + speed * np.sin(agents[:, 2])


# @jit
def deposit_pheromone(p_array, agents, width=WIDTH, height=HEIGHT):
    # Round coordinates to the nearest integers and clip to array bounds
    x_idx = np.clip(np.round(agents[:, 0]).astype(int), 0, width - 1)
    y_idx = np.clip(np.round(agents[:, 1]).astype(int), 0, height - 1)

    # Deposit pheromone at the rounded position
    p_array[y_idx, x_idx] = p_array[y_idx, x_idx] + 1


# print("hallo")


p_array = PheromoneArray()
parray = p_array.p_array
agneten = Agent()
agnete = agneten.agents

for _ in range(10):
    start_time = time.time()
    parray = update_pheromones(parray)
    rotate_towards_sensor(parray, agnete, SENSOR_DISTANCE)
    move(agnete)
    deposit_pheromone(parray, agnete)
    end_time = time.time()
    execution_time = end_time - start_time
    print(_, ": Execution time:", execution_time, "seconds")
