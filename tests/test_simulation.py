import sys
from pathlib import Path

import numpy as np

sys.path.append(str(Path(__file__).resolve().parent.parent))  # noqa: E402

from cfg_sim.world_cfg import SlimeConfig  # noqa: E402

from slime_mold_simulation import simulation  # noqa: E402

# Define simulation parameters from the configuration file
WIDTH = SlimeConfig.WIDTH
HEIGHT = SlimeConfig.HEIGHT
DECAY = SlimeConfig.DECAY
DIFFUSION_COEFFICENT = SlimeConfig.DIFFUSION_COEFFICENT
AGENT_NUMBER = SlimeConfig.AGENT_NUMBER
SPEED = SlimeConfig.SPEED
SENSOR_DISTANCE = SlimeConfig.SENSOR_DISTANCE
ROTATION_SPEED = SlimeConfig.ROTATION_SPEED
SENSOR_ANGLE = SlimeConfig.SENSOR_ANGLE
SPAWN_RADIUS = SlimeConfig.SPAWN_RADIUS


# Test the initialization of the PheromoneArray class
def test_PheromoneArray_init():
    p_array = simulation.PheromoneArray()
    assert p_array.width == WIDTH, f"Expected p_array.width to be {WIDTH}, but got {p_array.width}"
    assert p_array.height == HEIGHT, f"Expected p_array.height to be {HEIGHT}, but got {p_array.height}"
    assert np.all(p_array.p_array == 0), "Expected the pheromone array to be initialized with all zeros"


# Test the initialization of the Agent class
def test_agent_init():
    agent = simulation.Agent()
    assert isinstance(agent.agenten, np.ndarray), "Expected agent.agenten to be an instance of np.ndarray"
    assert agent.agenten.shape == (
        AGENT_NUMBER,
        3,
    ), f"Expected agent.agenten.shape to be {(AGENT_NUMBER, 3)}, but got {agent.agenten.shape}"


# Test the diffusion of pheromones
def test_diffuse():
    p_array = np.zeros((HEIGHT, WIDTH))
    p_array[10, 10] = 1  # Set a single point with pheromone
    p_array_diffused = simulation.diffuse(p_array)
    assert 0 < p_array_diffused[10, 10] < 1, "Value at [10, 10] should be diffused"
    assert np.any(p_array_diffused[:10, :] > 0), "Pheromone should diffuse outward"


# Test the decay of pheromones
def test_decay():
    p_array = np.ones((HEIGHT, WIDTH))
    p_array_decayed = simulation.decay(p_array)
    assert np.all(
        p_array_decayed < p_array
    ), "Expected values in the decayed pheromone array to be less than original values"


# Test the calculation of sensor positions
def test_get_sensors():
    agents = np.random.rand(AGENT_NUMBER, 3)  # Random initial agent positions and orientations
    sensors, sensors_angles = simulation.get_sensors(agents)
    assert isinstance(sensors, list), "Expected 'sensors' to be a list, but it is not."
    assert isinstance(sensors_angles, np.ndarray), "Expected 'sensors_angles' to be a numpy ndarray, but it is not."
    assert sensors_angles.shape == (
        AGENT_NUMBER,
        3,
    ), f"Expected 'sensors_angles' to have shape {(AGENT_NUMBER, 3)}, but got {sensors_angles.shape}."


# Test the retrieval of pheromone values at sensor positions
def test_get_pheromone_value_at():
    p_array = np.zeros((HEIGHT, WIDTH))
    p_array[10, 10] = 1  # Pheromone present at (10, 10)
    sensors = np.array([[10, 10], [0, 0], [15, 15], [100, 100]])  # Example sensor positions
    sensor_values = simulation.get_pheromone_value_at(p_array, sensors)
    assert sensor_values.shape == (
        AGENT_NUMBER,
        len(sensors),
    ), f"Expected shape ({AGENT_NUMBER}, {len(sensors)}), got {sensor_values.shape}"
    assert np.all(sensor_values[:, 0] == 1), "Sensor on pheromone should detect value 1 for all agents"
    assert np.all(sensor_values[:, 1] == 0), "Sensor not on pheromone should detect value 0 for all agents"
    assert np.all(sensor_values[:, 2] == 0), "Sensor not on pheromone should detect value 0 for all agents"
    assert np.all(sensor_values[:, 3] == 0), "Sensor not on pheromone should detect value 0 for all agents"


# Test boundary reflection logic for agents
def test_reflect_boundary():
    agents = np.array([[1, 1, 0], [HEIGHT, WIDTH, 0], [0, WIDTH, 0], [HEIGHT, 0, 0]])  # Agents near the edges
    agents_reflected = simulation.reflect_boundary(agents)

    # Ensure all agents are within bounds after reflection
    assert np.all(
        agents_reflected[:, 0] >= 0
    ), "Expected all x positions to be >= 0 after reflection, but some are not."
    assert np.all(
        agents_reflected[:, 0] < HEIGHT
    ), f"Expected all x positions to be < {HEIGHT} after reflection, but some are not."
    assert np.all(
        agents_reflected[:, 1] >= 0
    ), "Expected all y positions to be >= 0 after reflection, but some are not."
    assert np.all(
        agents_reflected[:, 1] < WIDTH
    ), f"Expected all y positions to be < {WIDTH} after reflection, but some are not."


# Test agent movement logic
def test_move():
    agents = np.array([[1, 1, 0], [HEIGHT, WIDTH, 0]])  # Initial agent positions
    agents_moved = simulation.move(agents, np.zeros((HEIGHT, WIDTH)))  # Move agents
    # Ensure all agents are within bounds after movement
    assert np.all(
        agents_moved[:, 0] >= 0
    ), "After moving, expected all agents' x positions to be >= 0, but some are outside the boundary."
    assert np.all(
        agents_moved[:, 0] < HEIGHT
    ), f"After moving, expected all agents' x positions to be < {HEIGHT}, but some exceed this boundary."
    assert np.all(
        agents_moved[:, 1] >= 0
    ), "After moving, expected all agents' y positions to be >= 0, but some are outside the boundary."
    assert np.all(
        agents_moved[:, 1] < WIDTH
    ), f"After moving, expected all agents' y positions to be < {WIDTH}, but some exceed this boundary."


# Test pheromone deposition logic
def test_deposit_pheromone():
    p_array = np.zeros((HEIGHT, WIDTH))
    agents = np.array([[1, 1], [HEIGHT - 1, WIDTH - 1]])  # Agent positions for pheromone deposit
    p_array_deposited = simulation.deposit_pheromone(p_array, agents)
    assert p_array_deposited[1, 1] == 1, "Pheromone not deposited correctly at (1, 1)"
    assert p_array_deposited[HEIGHT - 1, WIDTH - 1] == 1, "Pheromone not deposited correctly at the edge"


# Test agent rotation towards sensed pheromone concentration
def test_rotate_towards_sensor():
    agents = np.random.rand(AGENT_NUMBER, 3)  # Agents with initial orientations
    sensor_values = np.random.rand(AGENT_NUMBER, len(agents))
    sensors_angles = np.random.rand(AGENT_NUMBER, 3)
    agents_rotated = simulation.rotate_towards_sensor(agents, sensor_values, sensors_angles, SENSOR_ANGLE)
    # Ensure agent orientations are updated correctly based on sensor readings
    assert np.all(agents_rotated[:, 2] >= 0), "Expected all rotated agents' direction angles to be >= 0 radians."
    assert np.all(agents_rotated[:, 2] < 2 * np.pi), "Expected all rotated agents' direction angles to be < 2π radians."


# Test the main simulation logic
def test_main():
    p_array = np.zeros((HEIGHT, WIDTH))  # Initialize pheromone array
    agents = np.random.rand(AGENT_NUMBER, 3)  # Initialize agents
    p_array, agents = simulation.main(p_array, agents)  # Run a simulation step
    # Ensure agents remain within bounds and pheromone levels are non-negative
    assert np.all(
        agents[:, 0] >= 0
    ), "Expected all agents' x positions to be >= 0, ensuring they're within the vertical boundaries."
    assert np.all(
        agents[:, 0] < HEIGHT
    ), f"Expected all agents' x positions to be < {HEIGHT}, ensuring they're within the vertical boundaries."
    assert np.all(
        agents[:, 1] >= 0
    ), "Expected all agents' y positions to be >= 0, ensuring they're within the horizontal boundaries."
    assert np.all(
        agents[:, 1] < WIDTH
    ), f"Expected all agents' y positions to be < {WIDTH}, ensuring they're within the horizontal boundaries."
    assert np.all(p_array >= 0), "Expected all values in p_array to be >= 0, indicating non-negative pheromone levels."
