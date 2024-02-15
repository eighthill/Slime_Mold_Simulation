import unittest
import math
import numpy as np

# Import the classes from your code
from simulation import Agent, PheromoneArray

class TestAgentMethods(unittest.TestCase):

    def test_float_to_init(self):
        array = PheromoneArray(x_len=500, y_len=500)  # smaller array for simplicity
        agent = Agent(array)

        # Test if the float coordinates [0.0, 0.0] are correctly converted to integer coordinates
        float_coordinates = [0.0, 0.0]
        int_coordinates = agent.mapping_float_to_int(float_coordinates, array)
        print(f"Float to Int: {float_coordinates} -> {int_coordinates}")
        expected_result = [array.world.shape[0] // 2, array.world.shape[1] // 2]
        self.assertEqual(int_coordinates, expected_result)

    def test_init_to_float(self):
        array = PheromoneArray(x_len=500, y_len=500)  # smaller array for simplicity
        agent = Agent(array)

        # Test if the integer coordinates [49, 49] are correctly converted to float coordinates
        int_coordinates = [array.world.shape[0] // 2, array.world.shape[1] // 2]
        float_coordinates = agent.mapping_int_to_float(int_coordinates, array)
        print(f"Int to Float: {int_coordinates} -> {float_coordinates}")
        expected_result = [0.0, 0.0]
        self.assertEqual(float_coordinates, expected_result)

if __name__ == '__main__':
    unittest.main() 

        

        