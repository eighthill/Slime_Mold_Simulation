from random import randint

import matplotlib.pyplot as plt
import math

"""
# This code is a first try out to identify what classes and methods are needed
# It is does not work userfriendly without any errors
# for example if the agents get a random startposition close to the edges it can happen, that the code will raise an error

# Here are two classes AgentArray and PheromoneArray, maybe it would be a good idea to give them the same Parent Class
# the entrie for the new positions of the Agents are the same for each of those arrays
# the diffrence is that the AgentArray always only contains a value at the positions of the agents
# the PheromoneArray on the other side gets multiplied by the factor 0.99 team it gets updated so that older values get smaller.
# the Value 1 for update_agent_position and 50 for update_pheromone are choosen randomly,
# here we should think about what values would make sense.


class AgentArray:
    def __init__(self, x_len, y_len):
        self.array = np.zeros((x_len, y_len), dtype=int)

    def update_agent_position(self, Agents_list):
        self.array = np.zeros_like(self.array, dtype=int)
        for agent in Agents_list:
            x, y, direction = agent[0], agent[1], agent[2]
            if direction == [1, 1]:
                self.array[x, y] += 1
            else:
                self.array[x, y] -= 1


class PheromoneArray:
    def __init__(self, x_len, y_len, fading=0.5, pheromone_value=10):
        self.world = np.zeros((x_len, y_len), dtype=int)
        self.fading = fading
        self.pheromone_value = pheromone_value

    def update_pheromone(self, Agents):
        self.world = (self.world * self.fading).astype(int)
        for agent in Agents:
            x, y = agent["int_x_pos"], agent["int_y_pos"]
            self.world[x, y] = self.pheromone_value

"""


# the agent class creates a list with one dictionary for each agent
class Agent:
    def __init__(self, array, num_agents=10, sensor_angle=50, radius=0.2):
        self.num_agents = num_agents
        self.sensor_angle = sensor_angle

        # since the radius is now used as distance, maybe the variables name should be changed to distance
        # if we still want the sensors to look within a given radius we should
        self.radius = radius
        self.Agents_list = []

        for idx in range(num_agents):
            int_x_pos = randint(0, array.world.shape[0] - 1)
            int_y_pos = randint(0, array.world.shape[1] - 1)
            float_x_pos, float_y_pos = self.mapping_int_to_float([int_x_pos, int_y_pos], array)
            movement_angle = randint(0, 360)  # degree as float?

            agent_dict = {
                "int_x_pos": int_x_pos,
                "int_y_pos": int_y_pos,
                "float_x_pos": float_x_pos,
                "float_y_pos": float_y_pos,
                "movement_angle": movement_angle,
            }

            self.Agents_list.append(agent_dict)

    # this method updates the next move for each agent
    def make_move(self, array):
        for agent in self.Agents_list:
            # the variable next_position contains: [x_coordinate,y_coordinate], angle
            next_position = self.get_best_move(array, agent)

            # the coordinates are given as float
            agent["float_x_pos"], agent["float_y_pos"] = next_position[0]

            # here we have the indicies for the array for each agent,
            # maybe there is a way to not safe it because we actually have the information already within the float coordinates
            # and we can always calculate those to integers with the function mapping_float_to_int
            [agent["int_x_pos"], agent["int_y_pos"]] = self.mapping_float_to_int(next_position[0], array)

            # this is the direction the agent is looking at after the move
            agent["movement_angle"] = next_position[1]

    # this method compares all possible next positions for an agent to find the best option
    def get_best_move(self, array, agent):
        possible_moves = self.get_next_moves(agent)
        amount_of_pheromones_list = []

        # get the amount of pheromones for each possible move and add it to the list amount_of_pheromones_list
        for move in possible_moves:
            int_coordinats = self.mapping_float_to_int(move[0], array)
            value = array.world[int_coordinats[0], int_coordinats[1]]
            amount_of_pheromones_list.append(value)

        # find which of the possitions has the most pheremones
        # here we could implement a method that makes sure that the agents change there way,
        # if there amount of pheromones has crossed a given value
        max_val = max(amount_of_pheromones_list)
        max_idx = amount_of_pheromones_list.index(max_val)
        next_position = possible_moves[max_idx]

        return next_position

    # calculate new x and y coordinate by given startposition, angle and distance
    def get_next_moves(self, agent):
        possible_moves = []

        # here we have 3 sensores, we could add a loop that creates a variable number of sensores
        angles = [-self.sensor_angle, 0, self.sensor_angle]
        for angle in angles:
            angle += agent["movement_angle"]
            x_new = agent["float_x_pos"] + self.radius * math.cos(angle)
            y_new = agent["float_y_pos"] + self.radius * math.sin(angle)

            if x_new > 1 or x_new < -1 or y_new > 1 or y_new < -1:
                # since agents can't leave the array, those lines calulate another angle and coordinates
                x_new, y_new, angle = self.reflect_at_boundary(x_new, y_new, agent["float_x_pos"], agent["float_y_pos"])

            # this list contains all possible next moves for one agent
            possible_moves.append([[x_new, y_new], angle])
        return possible_moves

    # this method is from ChatGPT as a help for now, but it has to be adjusted later in another issue
    def reflect_at_boundary(self, x, y, x_pos, y_pos):
        if x > 1:
            x = 2 - x
        elif x < -1:
            x = -2 - x
        if y > 1:
            y = 2 - y
        elif y < -1:
            y = -2 - y
        # calculating new angle
        angle = math.atan2(y - y_pos, x - x_pos)
        return x, y, angle

    # this method needs a list with 2 float coordinates and calculates them to integer indicies for an given array
    def mapping_float_to_int(self, coordinates, array):
        # 2 because of float has to be in [-1,1]
        float_world_size = 2
        new_coordinates = []

        for idx, val in enumerate(coordinates):
            coordinate = int(int((val + 1) / float_world_size * array.world.shape[idx])) - 1
            new_coordinates.append(coordinate)
        return new_coordinates

    # this method needs a list with 2 integer indicies for an given array and calculates them to float coordinates
    def mapping_int_to_float(self, coordinates, array):
        # 2 because of float has to be in [-1,1]
        float_world_size = 2
        new_coordinates = []

        for idx, val in enumerate(coordinates):
            coordinate = -1 + (float_world_size * val / array.world.shape[idx])
            new_coordinates.append(coordinate)
        return new_coordinates


# this method is only to visualize the current array
def plot_large_array_with_colors(array):
    plt.imshow(array.world, interpolation="none", cmap="viridis")
    plt.show()


"""

# this is the main programm where all the objects are created and methods are called
def main():
    # maybe we will here need a variables that are given from outside to the main method
    # so that it is easier to combine code and GUI
    x_len = 100
    y_len = 100

    pheromone_array = PheromoneArray(x_len, y_len)
    agent_array = AgentArray(x_len, y_len)

    agents = Agent(1, agent_array, 10)

    # this is actually initializing both arrays I'm sure there is a better way
    pheromone_array.update_pheromone(agents.Agents_list)
    agent_array.update_agent_position(agents.Agents_list)

    # here the agent array is plotted to see how the agents are distributed after initializing
    plot_large_array_with_colors(agent_array.array)

    # here we would definitly need sth else than a for loop through a range,
    # we have to work with time and update every second or ever 10 ms latest by creating the GUI
    # but for the try out this was really helpful

    for _ in range(50):
        agents.move_Agents(agents.Agents_list, pheromone_array.array)

        pheromone_array.update_pheromone(agents.Agents_list)
        agent_array.update_agent_position(agents.Agents_list)

    # Here the PheromoneArray is shown instead of the array with the agents,
    # because it gives a better overview on what has happend over the last iterations

    plot_large_array_with_colors(pheromone_array.array)


if __name__ == "__main__":
    main()
"""
