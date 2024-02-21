# This is the Configutaion file with all global parameters
import numpy as np

# Simulationparameters
WIDTH = 1000
HEIGHT = 1000
DECAY = 0.95
DIFFUSION_COEFFICENT = 0.5

# Agentparameters
AGENT_NUMBER = 100
SPEED = 1
SENSOR_DISTANCE = 3
ROTATION_SPEED = 10
# the angles are calculated with radian (0 = 0° and 2*pi = 360°) in the simulation Code so the given angle shoulr be between 0 and 2pi.
# here the formula X/180*pi is calculating a given degree X into a radian
SENSOR_ANGLE = 33
