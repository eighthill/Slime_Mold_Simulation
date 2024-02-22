"""Tests for the slime_mold_simulation.my_module module."""
import numpy as np
import pytest

from slime_mold_simulation.simulation import diffuse, decay, get_sensors, get_pheromone_value_at, reflect_boundary, move, deposit_pheromone, rotate_towards_sensor

