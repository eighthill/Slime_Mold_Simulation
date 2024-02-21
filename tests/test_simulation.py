import numpy as np
import unittest
from slime_mold_simulation.simulation import move, deposit_pheromone, get_pheromone_value_at, rotate_towards_sensor, get_sensors
from slime_mold_simulation.config import WIDTH, HEIGHT, SPEED, AGENT_NUMBER, SENSOR_DISTANCE, SENSOR_ANGLE, ROTATION_SPEED

class TestSimulationMethods(unittest.TestCase):
    def setUp(self):
        # Setup for test environment
        self.p_array = np.zeros((HEIGHT, WIDTH))
        self.agents = np.array([[300, 300, np.pi / 4]] * AGENT_NUMBER)  # Simple setup: all agents at (300, 300) facing 45 degrees

    def test_deposit_pheromone(self):
        # Test deposit_pheromone functionality
        deposit_pheromone(self.p_array, self.agents)
        self.assertTrue(np.sum(self.p_array) > 0, "Pheromone should be deposited")

    def test_move(self):
        # Test move functionality
        initial_position = self.agents.copy()
        move(self.agents, self.p_array, SPEED)
        self.assertTrue(np.any(self.agents != initial_position), "Agents should have moved")

    """
    #CURRENTLY BROKEN, fix needed
    def test_get_pheromone_value_at(self):
        # Assuming each agent has one sensor for simplicity, and it's located at [303, 303]
        sensors = [[[303, 303]] for _ in range(AGENT_NUMBER)]  # This matches the expected structure

        sensor_values = get_pheromone_value_at(self.p_array, sensors, AGENT_NUMBER)

        # Check if all sensor values are greater than 0, indicating they detected the pheromone
        self.assertTrue(np.all(sensor_values > 0), "All sensor values should be greater than 0 where pheromones are present")
    """
    
    def test_rotate_towards_sensor(self):
        # Configuration
        AGENT_NUMBER = 10000
        
        # Initialize agents facing north (0 radians), positioned near the high concentration
        agents = np.array([[49 + i, 50, 0] for i in range(AGENT_NUMBER)])
        
        # Mock sensor values and angles for each agent
        sensors, sensors_angles = get_sensors(agents, SENSOR_ANGLE, AGENT_NUMBER)
        sensor_values = get_pheromone_value_at(self.p_array, sensors, AGENT_NUMBER)
        
        # Rotate agents towards the highest pheromone concentration
        agents_updated = rotate_towards_sensor(agents, sensor_values, sensors_angles, SENSOR_ANGLE, AGENT_NUMBER, ROTATION_SPEED)
        
        # Verify if the agents' headings are updated correctly
        for i in range(AGENT_NUMBER):
            print(f"Agent {i} updated heading: {agents_updated[i, 2]}")

    
if __name__ == '__main__':
    unittest.main()
