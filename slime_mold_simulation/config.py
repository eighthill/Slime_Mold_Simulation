# This is the Configutaion file with all global parameters
<<<<<<< HEAD
import numpy as np


class SlimeConfig:
    # Simulationparameters
    WIDTH = 1000
    HEIGHT = 1000
    DECAY = 0.97
    DIFFUSION_COEFFICENT = 0.5

    # Agentparameters
    AGENT_NUMBER = 10000
    SPEED = 1
    SENSOR_DISTANCE = 3
    ROTATION_SPEED = 0.2  # max. 1 otherwise error!
    # the angles are calculated with radian (0 = 0° and 2*pi = 360°) in the simulation Code so the given angle shoulr be between 0 and 2pi.
    # here the formula X/180*pi is calculating a given degree X into a radian
    SENSOR_ANGLE = 33
    TIMESTEP = 0.0166

    @classmethod
    def set_speed(cls, new_speed):
        cls.SPEED = new_speed

    @classmethod
    def set_agent_count(cls, new_agent_count):
        cls.AGENT_NUMBER = new_agent_count
=======

# Simulationparameters
WIDTH = 1000
HEIGHT = 1000
DECAY = 0.97
DIFFUSION_COEFFICENT = 0.5


AGENT_NUMBER = 100
SPEED = 1
SENSOR_DISTANCE = 3
ROTATION_SPEED = 0.2
# the angles are calculated with radian (0 = 0° and 2*pi = 360°) in the simulation Code so the given angle shoulr be between 0 and 2pi.
# here the formula X/180*pi is calculating a given degree X into a radian
SENSOR_ANGLE = 33
>>>>>>> 5f2f9ffff8518091fa2f1e6395485042b4a1b27e
