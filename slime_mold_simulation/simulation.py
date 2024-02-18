import math
import numpy as np
from random import choice, randint
from scipy.stats import rankdata
from scipy.ndimage import gaussian_filter
import time

# Put the global parameters in a seperate file for visualization?
# Simulationparameters
WIDTH = 10
HEIGHT = 10
DECAY = 0.95
DIFFUSION_COEFFICENT = 0.5

# Agentparameters
AGENT_NUMBER = 5
SENSOR_ANGLE = 0.33
SPEED = 2
THRESHOLD = 0.1  # Adjust based on your simulation
ROTATION_SPEED = 1
SENSOR_DISTANCE = 10 


class PheromoneArray:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.p_array = np.zeros((WIDTH, HEIGHT))

class Agent:
    def __init__(self):
        x = np.random.uniform(WIDTH * 0.5, WIDTH * 0.6, AGENT_NUMBER)
        y = np.random.uniform(HEIGHT * 0.5, HEIGHT * 0.6, AGENT_NUMBER)
        heading = np.random.uniform(0, 2 * math.pi, AGENT_NUMBER)
        self.agents = np.column_stack((x, y, heading))

def diffuse(p_array):
    # Apply Gaussian filter for diffusion
    return gaussian_filter(p_array, sigma=DIFFUSION_COEFFICENT)

def decay(p_array):
    return p_array * DECAY

def get_sensors(agents):
    # Define sensor positions directly in the constructor
    sensor_left = [agents[:,0] + SENSOR_DISTANCE * np.cos(agents[:,2]-SENSOR_ANGLE),
                   agents[:,1] + SENSOR_DISTANCE * np.sin(agents[:,2]-SENSOR_ANGLE)]
    main_sensor = [agents[:,0] + SENSOR_DISTANCE * np.cos(agents[:,2]),
                   agents[:,1] + SENSOR_DISTANCE * np.sin(agents[:,2])]
    sensor_right = [agents[:,0] + SENSOR_DISTANCE * np.cos(agents[:,2]+SENSOR_ANGLE),
                    agents[:,1] + SENSOR_DISTANCE * np.sin(agents[:,2]+SENSOR_ANGLE)]
    # Combine sensor positions 
    sensors = [sensor_left, main_sensor, sensor_right]
    sensors_angles = [-SENSOR_ANGLE,0,SENSOR_ANGLE]
    return sensors,sensors_angles

def get_pheromone_value_at(p_array, sensors):
    sensor_values = np.zeros((AGENT_NUMBER, len(sensors)))
    for idx, sensor in enumerate(sensors):
        # Clip x and y to ensure they are within the bounds of the pheromone array
        x = np.clip(np.round(sensor[0]).astype(int), 0, WIDTH - 1)
        y = np.clip(np.round(sensor[1]).astype(int), 0, HEIGHT - 1)
        sensor_values[:, idx] = p_array[y, x]
    return sensor_values






def move(agents):
    # Update agent's position based on heading=agents[:, 2] and speed
    agents[:, 0] = agents[:, 0] + SPEED * np.cos(agents[:, 2])
    agents[:, 1] = agents[:, 1] + SPEED * np.sin(agents[:, 2])

def deposit_pheromone(p_array, agents):
    # Round coordinates to the nearest integers and clip to array bounds
    x_idx = np.clip(np.round(agents[:, 0]).astype(int), 0, WIDTH - 1)
    y_idx = np.clip(np.round(agents[:, 1]).astype(int), 0, HEIGHT - 1)
    # Deposit pheromone at the rounded position
    p_array[y_idx, x_idx] = p_array[y_idx, x_idx] + 1





def rotate_towards_sensor_simple(agents, pheromone_values, sensors_angles):
    for idx,row in enumerate(pheromone_values):
        selected_angle = np.argmax(row)
        agents[idx,2] = agents[idx,2] + sensors_angles[selected_angle] * ROTATION_SPEED


def rank_pheromone_values(sensor_values):
    sensor_ranking = []
    for row in sensor_values:
        sensor_ranking.append(rankdata(row, method='min'))
        return sensor_ranking





def rotate_towards_sensor_upgrade(agents,sensor_ranking,sensors_angles):
    selected_angles = []
    for row in sensor_ranking:
        if np.count_nonzero(row == 1) == 1:
            idx = np.where(row == 1)[0][0]
        else:
            # if we want the Agents to choose a point between two sensores that both have the highest value of pheromones
            # then we have to change code here so that not indecies are stored but the new angle is calculated here already
            indices_of_ones = np.where(row == 1)[0]
            idx = choice(indices_of_ones)
        selected_angles.append(sensors_angles[idx])
    # Adjust heading towards the sensors with matrix operations
    agents[:, 2] = agents[:, 2] + selected_angles * ROTATION_SPEED




def main_easy(parray,agnet,_):
    parray = diffuse(parray)
    parray = decay(parray)
    sensors,sensors_angles = get_sensors(agnet)
    sensor_values = get_pheromone_value_at(parray, sensors)
    rotate_towards_sensor_simple(agnet, sensor_values, sensors_angles)
    move(agnet)
    deposit_pheromone(parray, agnet)



def main_better(parray,agnet,_):
    parray = diffuse(parray)
    parray = decay(parray)
    sensors,sensors_angles = get_sensors(agnet)
    sensor_values = get_pheromone_value_at(parray, sensors)
    sensor_ranking = rank_pheromone_values(sensor_values)
    rotate_towards_sensor_upgrade(agnet,sensor_ranking,sensors_angles)
    move(agnet)
    deposit_pheromone(parray, agnet)




p_array = PheromoneArray()
agneten = Agent()
parray = p_array.p_array
agnet = agneten.agents



for _ in range(5):
    main_easy(parray,agnet,_)
    main_better(parray,agnet,_)