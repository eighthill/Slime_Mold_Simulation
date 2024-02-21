import numpy as np
import unittest
from slime_mold_simulation.simulation import move, deposit_pheromone, get_pheromone_value_at
from slime_mold_simulation.config import WIDTH, HEIGHT, SPEED, AGENT_NUMBER, SENSOR_DISTANCE, SENSOR_ANGLE

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
    
if __name__ == '__main__':
    unittest.main()
