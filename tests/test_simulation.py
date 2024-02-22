import pytest
import numpy as np
from slime_mold_simulation import config
from slime_mold_simulation import simulation
# from slime_mold_simulation.simulation import WIDTH, HEIGHT, AGENT_NUMBER, SENSOR_ANGLE

def test_PheromoneArray_init():
    p_array = simulation.PheromoneArray()
    assert p_array.width == config.WIDTH, f"Expected p_array.width to be {config.WIDTH}, but got {p_array.width}"
    assert p_array.height == config.HEIGHT, f"Expected p_array.height to be {config.HEIGHT}, but got {p_array.height}"
    assert np.all(p_array.p_array == 0), "Expected the pheromone array to be initialized with all zeros"


def test_agent_init():
    agent = simulation.Agent()
    assert isinstance(agent.agenten, np.ndarray), "Expected agent.agenten to be an instance of np.ndarray"
    assert agent.agenten.shape == (config.AGENT_NUMBER, 3), f"Expected agent.agenten.shape to be {(config.AGENT_NUMBER, 3)}, but got {agent.agenten.shape}"


def test_diffuse():
    p_array = np.zeros((config.HEIGHT, config.WIDTH))
    p_array[10, 10] = 1
    p_array_diffused = simulation.diffuse(p_array)
    assert 0 < p_array_diffused[10, 10] < 1, "Value at [10, 10] should be diffused"
    assert np.any(p_array_diffused[:10, :] > 0), "Pheromone should diffuse outward"

def test_decay():
    p_array = np.ones((config.HEIGHT, config.WIDTH))
    p_array_decayed = simulation.decay(p_array)
    assert np.all(p_array_decayed < p_array), "Expected values in the decayed pheromone array to be less than original values"

def test_get_sensors():
    agents = np.random.rand(config.AGENT_NUMBER, 3)
    sensors, sensors_angles = simulation.get_sensors(agents)
    assert isinstance(sensors, list), "Expected 'sensors' to be a list, but it is not."
    assert isinstance(sensors_angles, np.ndarray), "Expected 'sensors_angles' to be a numpy ndarray, but it is not."
    assert sensors_angles.shape == (config.AGENT_NUMBER, 3), f"Expected 'sensors_angles' to have shape {(config.AGENT_NUMBER, 3)}, but got {sensors_angles.shape}."


def test_get_pheromone_value_at():
    p_array = np.zeros((config.HEIGHT, config.WIDTH))
    p_array[10, 10] = 1
    sensors = np.array([[10, 10], [0, 0], [15, 15], [100,100]])
    sensor_values = simulation.get_pheromone_value_at(p_array, sensors, config.HEIGHT, config.WIDTH, config.AGENT_NUMBER)
    assert sensor_values.shape == (config.AGENT_NUMBER, len(sensors)), f"Expected shape ({config.AGENT_NUMBER}, {len(sensors)}), got {sensor_values.shape}"
    assert np.all(sensor_values[:, 0] == 1), "Sensor on pheromone should detect value 1 for all agents"
    assert np.all(sensor_values[:, 1] == 0), "Sensor not on pheromone should detect value 0 for all agents"
    assert np.all(sensor_values[:, 2] == 0), "Sensor not on pheromone should detect value 0 for all agents"
    assert np.all(sensor_values[:, 3] == 0), "Sensor not on pheromone should detect value 0 for all agents"
    
def test_reflect_boundary():
    agents = np.array([
        [1, 1, 0],
        [config.HEIGHT, config.WIDTH, 0],
        [0, config.WIDTH, 0],
        [config.HEIGHT, 0, 0]
    ])
    agents_reflected = simulation.reflect_boundary(agents)

    assert np.all(agents_reflected[:, 0] >= 0), "Expected all x positions to be >= 0 after reflection, but some are not."
    assert np.all(agents_reflected[:, 0] < config.HEIGHT), f"Expected all x positions to be < {config.HEIGHT} after reflection, but some are not."
    assert np.all(agents_reflected[:, 1] >= 0), "Expected all y positions to be >= 0 after reflection, but some are not."
    assert np.all(agents_reflected[:, 1] < config.WIDTH), f"Expected all y positions to be < {config.WIDTH} after reflection, but some are not."


def test_move():
    agents = np.array([[1, 1, 0],
                       [config.HEIGHT, config.WIDTH, 0]])
    agents_moved = simulation.move(agents, np.zeros((config.HEIGHT, config.WIDTH)))
    assert np.all(agents_moved[:, 0] >= 0), "After moving, expected all agents' x positions to be >= 0, but some are outside the boundary."
    assert np.all(agents_moved[:, 0] < config.HEIGHT), f"After moving, expected all agents' x positions to be < {config.HEIGHT}, but some exceed this boundary."
    assert np.all(agents_moved[:, 1] >= 0), "After moving, expected all agents' y positions to be >= 0, but some are outside the boundary."
    assert np.all(agents_moved[:, 1] < config.WIDTH), f"After moving, expected all agents' y positions to be < {config.WIDTH}, but some exceed this boundary."


def test_deposit_pheromone():
    p_array = np.zeros((config.HEIGHT, config.WIDTH))
    agents = np.array([
        [1, 1],
        [config.HEIGHT - 1, config.WIDTH - 1]
    ])
    p_array_deposited = simulation.deposit_pheromone(p_array, agents)
    assert p_array_deposited[1, 1] == 1, "Pheromone not deposited correctly at (1, 1)"
    assert p_array_deposited[config.HEIGHT - 1, config.WIDTH - 1] == 1, "Pheromone not deposited correctly at the edge"

def test_rotate_towards_sensor():
    agents = np.random.rand(config.AGENT_NUMBER, 3)
    sensor_values = np.random.rand(config.AGENT_NUMBER, len(agents))
    sensors_angles = np.random.rand(config.AGENT_NUMBER, 3)
    agents_rotated = simulation.rotate_towards_sensor(agents, sensor_values, sensors_angles, config.SENSOR_ANGLE)
    assert np.all(agents_rotated[:, 2] >= 0), "Expected all rotated agents' direction angles to be >= 0 radians."
    assert np.all(agents_rotated[:, 2] < 2 * np.pi), "Expected all rotated agents' direction angles to be < 2π radians."

def test_main():
    p_array = np.zeros((config.HEIGHT, config.WIDTH))
    agents = np.random.rand(config.AGENT_NUMBER, 3)
    p_array, agents = simulation.main(p_array, agents)
    assert np.all(agents[:, 0] >= 0), "Expected all agents' x positions to be >= 0, ensuring they're within the vertical boundaries."
    assert np.all(agents[:, 0] < config.HEIGHT), f"Expected all agents' x positions to be < {config.HEIGHT}, ensuring they're within the vertical boundaries."
    assert np.all(agents[:, 1] >= 0), "Expected all agents' y positions to be >= 0, ensuring they're within the horizontal boundaries."
    assert np.all(agents[:, 1] < config.WIDTH), f"Expected all agents' y positions to be < {config.WIDTH}, ensuring they're within the horizontal boundaries."
    assert np.all(p_array >= 0), "Expected all values in p_array to be >= 0, indicating non-negative pheromone levels."