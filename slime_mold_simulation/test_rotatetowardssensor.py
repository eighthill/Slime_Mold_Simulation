import numpy as np
from slime_mold_simulation.simulation import rotate_towards_sensor, get_sensors, get_pheromone_value_at
from slime_mold_simulation.config import AGENT_NUMBER, SENSOR_ANGLE, ROTATION_SPEED

# Mock setup for pheromone values and agent positions
def test_rotate_towards_sensor():
    # Configuration
    AGENT_NUMBER = 1
    SENSOR_ANGLE = np.pi
    ROTATION_SPEED = 0.1  # Adjusted for testing
    
    # Simulate a simple environment with predefined pheromone values
    p_array = np.zeros((100, 100))
    p_array[50, 50] = 10  # High pheromone concentration at the center
    
    # Initialize an agent facing north (0 radians), positioned at (49, 50)
    agents = np.array([[49, 50, 0]])
    
    # Get sensor values and angles
    sensors, sensors_angles = get_sensors(agents, SENSOR_ANGLE, AGENT_NUMBER)
    sensor_values = get_pheromone_value_at(p_array, sensors, AGENT_NUMBER)
    print(sensor_values)
    
    # Rotate agent towards the highest pheromone concentration
    agents_updated = rotate_towards_sensor(agents, sensor_values, sensors_angles, SENSOR_ANGLE, AGENT_NUMBER, ROTATION_SPEED)
    
    # Verify if the agent's heading is updated correctly
    # Since the highest concentration is directly ahead, the agent's heading should not change
    assert np.isclose(agents_updated[0, 2], 0), "Agent's heading did not update correctly."

if __name__ == "__main__":
    test_rotate_towards_sensor()
