"""Tests for the slime_mold_simulation.my_module module."""
import numpy as np
import pytest

from slime_mold_simulation.my_module import hello
from slime_mold_simulation.simulation import get_sensors



def test_hello():
    assert hello("Alice") == "Hello Alice!"


def test_hello_with_error():
    with pytest.raises(ValueError) as excinfo:
        hello("nobody")
    assert "Can not say hello to nobody" in str(excinfo.value)


@pytest.fixture
def some_name():
    return "Jane Smith"


def test_hello_with_fixture(some_name):
    assert hello(some_name) == "Hello Jane Smith!"

import unittest

def test_get_sensors():
    # Test with valid inputs
    agents = np.array([[1, 2, 3], [4, 5, 6]])
    SENSOR_ANGLE = 45
    AGENT_NUMBER = 2
    expected_sensors = np.array([[1, 2, 3], [4, 5, 6]])
    expected_sensors_angles = np.array([[45, 45, 45], [45, 45, 45]])
    sensors, sensors_angles = get_sensors(agents, SENSOR_ANGLE, AGENT_NUMBER)
    assert np.array_equal(sensors, expected_sensors)
    assert np.array_equal(sensors_angles, expected_sensors_angles)

    # Test with invalid inputs
    agents = np.array([[1, 2, 3], [4, 5, 6]])
    SENSOR_ANGLE = 45
    AGENT_NUMBER = 3
    expected_sensors = np.array([[1, 2, 3], [4, 5, 6]])
    expected_sensors_angles = np.array([[45, 45, 45], [45, 45, 45]])
    with(ValueError):
        sensors, sensors_angles = get_sensors(agents, SENSOR_ANGLE, AGENT_NUMBER)

    # Test with invalid inputs
    agents = np.array([[1, 2, 3], [4, 5, 6]])
    SENSOR_ANGLE = 45
    AGENT_NUMBER = 2
    expected_sensors = np.array([[1, 2, 3], [4, 5, 6]])
    expected_sensors_angles = np.array([[45, 45, 45], [45, 45, 45]])
    with (ValueError):
        sensors, sensors_angles = get_sensors(agents, SENSOR_ANGLE, AGENT_NUMBER)

if __name__ == '__main__':
    unittest.main()