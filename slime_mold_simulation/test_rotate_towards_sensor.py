import numpy as np
from slime_mold_simulation.simulation import rotate_towards_sensor, get_sensors, get_pheromone_value_at
from slime_mold_simulation.config import SENSOR_ANGLE, ROTATION_SPEED, HEIGHT, WIDTH

def test_rotate_towards_sensor():
    # Configuration
    AGENT_NUMBER = 10000
    
    # Simulate a simple environment with predefined pheromone values
    p_array = np.zeros((HEIGHT, WIDTH))
    p_array[50, 50] = 10  # High pheromone concentration at the center
    
    # Initialize agents facing north (0 radians), positioned near the high concentration
    agents = np.array([[49 + i, 50, 0] for i in range(AGENT_NUMBER)])
    
    # Mock sensor values and angles for each agent
    sensors, sensors_angles = get_sensors(agents, SENSOR_ANGLE, AGENT_NUMBER)
    sensor_values = get_pheromone_value_at(p_array, sensors, AGENT_NUMBER)
    
    # Rotate agents towards the highest pheromone concentration
    agents_updated = rotate_towards_sensor(agents, sensor_values, sensors_angles, SENSOR_ANGLE, AGENT_NUMBER, ROTATION_SPEED)
    
    # Verify if the agents' headings are updated correctly
    for i in range(AGENT_NUMBER):
        print(f"Agent {i} updated heading: {agents_updated[i, 2]}")

if __name__ == "__main__":
    test_rotate_towards_sensor()
