from config import *
import math
import numpy as np
from random import choice, randint
from scipy.stats import rankdata
from scipy.ndimage import gaussian_filter


class PheromoneArray:
    def __init__(self):
        self.width = WIDTH
        self.height = HEIGHT
        self.p_array = np.zeros((WIDTH, HEIGHT))

class Agent:
    def __init__(self):
        y = np.random.uniform(0, HEIGHT, AGENT_NUMBER)
        x = np.random.uniform(0, WIDTH, AGENT_NUMBER)
        heading = np.random.uniform(0, 2 * math.pi, AGENT_NUMBER)
        self.agenten = np.column_stack((y, x, heading))

def diffuse(p_array):
    # Apply Gaussian filter for diffusion
    return gaussian_filter(p_array, sigma=DIFFUSION_COEFFICENT)

def decay(p_array):
    return p_array * DECAY

def get_sensors(agents):
    # Define sensor positions directly in the constructor
    angle_left = -agents[:,2] - SENSOR_ANGLE-np.random.uniform(0, 0.1* math.pi, AGENT_NUMBER)
    angle_main = agents[:,2]
    angle_right= agents[:,2] + SENSOR_ANGLE+np.random.uniform(0,  0.1*math.pi, AGENT_NUMBER)

    sensor_left = [agents[:,0] + SENSOR_DISTANCE * np.sin(angle_left),
                   agents[:,1] + SENSOR_DISTANCE * np.cos(angle_left)]
    sensor_main = [agents[:,0] + SENSOR_DISTANCE * np.sin(angle_main),
                   agents[:,1] + SENSOR_DISTANCE * np.cos(angle_main)]
    sensor_right = [agents[:,0] + SENSOR_DISTANCE * np.sin(angle_right),
                    agents[:,1] + SENSOR_DISTANCE * np.cos(angle_right)]
    
    sensors = [sensor_left, sensor_main, sensor_right]
    sensors_angles = np.column_stack((angle_left,angle_main,angle_right))

    """
    # Überprüfen und abprallen
    for idx,senor in enumerate(sensors):
        mask_top = senor[0] < 0
        mask_bottom = senor[0] > HEIGHT 
        mask_left = senor[1] < 0
        mask_right = senor[1] > WIDTH
        
        sensors_angles[idx] = np.where(mask_left, -sensors_angles[idx], sensors_angles[idx])
        sensors_angles[idx] = np.where(mask_right, 2 * math.pi - sensors_angles[idx], sensors_angles[idx])
        sensors_angles[idx] = np.where(mask_top, -sensors_angles[idx], sensors_angles[idx])
        sensors_angles[idx] = np.where(mask_bottom, 2 * math.pi - sensors_angles[idx], sensors_angles[idx])
        """
    return sensors,sensors_angles

def get_pheromone_value_at(p_array, sensors):
    sensor_values = np.zeros((AGENT_NUMBER, len(sensors)))
    for idx, sensor in enumerate(sensors):
        # Clip x and y to ensure they are within the bounds of the pheromone array
        y = np.clip(np.round(sensor[0]).astype(int), 0, WIDTH - 1)
        x = np.clip(np.round(sensor[1]).astype(int), 0, HEIGHT - 1)
        sensor_values[:, idx] = p_array[y, x]
    return sensor_values






def move(agents):
    # Update agent's position based on heading=agents[:, 2] and speed
    agents[:, 0] = agents[:, 0] + SPEED * np.sin(agents[:, 2])
    agents[:, 1] = agents[:, 1] + SPEED * np.cos(agents[:, 2])
    return agents


def deposit_pheromone(p_array, agents):
    # Round coordinates to the nearest integers and clip to array bounds
    x_idx = np.clip(np.round(agents[:, 0]).astype(int), 0, HEIGHT  - 1)
    y_idx = np.clip(np.round(agents[:, 1]).astype(int), 0, WIDTH - 1)
    # Deposit pheromone at the rounded position
    p_array[y_idx, x_idx] = p_array[y_idx, x_idx] + 1
    return p_array





def rotate_towards_sensor_simple(agents, sensor_values, sensors_angles):
    for idx in range(AGENT_NUMBER):
        selected_angle = np.argmax(sensor_values[idx])
        agents[idx,2] =  sensors_angles[idx][selected_angle] #* ROTATION_SPEED agents[idx,2] + 
        print(type(agents))
    return agents

def rank_pheromone_values(sensor_values):
    sensor_ranking = []
    for row in sensor_values:
        sensor_ranking.append(rankdata(row, method='min'))
    return sensor_ranking
    
def rotate_towards_sensor_upgrade(agents,sensor_ranking,sensors_angles):
    selected_angles = []
    for idx,row in enumerate(sensor_ranking):
        if np.count_nonzero(row == 1) == 1:
            idx_angle = np.where(row == 1)[0][0]
        else:
            # if we want the Agents to choose a point between two sensores that both have the highest value of pheromones
            # then we have to change code here so that not indecies are stored but the new angle is calculated here already
            indices_of_ones = np.where(row == 1)[0]
            idx_angle = choice(indices_of_ones)
        selected_angles.append(sensors_angles[idx][idx_angle])
    #selected_angles = np.array(selected_angles)
    # Adjust heading towards the sensors with matrix operations
    agents[:, 2]= selected_angles# * ROTATION_SPEEDagents[:, 2] + 
    #print(type(agents))
    return agents




def main_simple(parray,agnet):
    parray = diffuse(parray)
    parray = decay(parray)
    sensors,sensors_angles = get_sensors(agnet)
    sensor_values = get_pheromone_value_at(parray, sensors)
    agnet = rotate_towards_sensor_simple(agnet, sensor_values, sensors_angles)
    agnet = move(agnet)
    parray= deposit_pheromone(parray, agnet)
    return parray,agnet



def main_upgrade(parray,agnet):
    parray = diffuse(parray)
    parray = decay(parray)
    sensors,sensors_angles = get_sensors(agnet)
    sensor_values = get_pheromone_value_at(parray, sensors)
    sensor_ranking = rank_pheromone_values(sensor_values)
    agnet = rotate_towards_sensor_upgrade(agnet,sensor_ranking,sensors_angles)
    agnet = move(agnet)
    parray= deposit_pheromone(parray, agnet)
    return parray,agnet

