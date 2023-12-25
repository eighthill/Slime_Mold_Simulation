# This code is a first try out to identify what classes and methods are needed
# It is does not work userfriendly without any errors
# for example if the agents get a random startposition close to the edges it can happen, that the code will raise an error


import matplotlib.pyplot as plt
import numpy as np
from random import randint
import random

"""
Here are two classes AgentArray and PheromoneArray, maybe it would be a good idea to give them the same Parent Class 
the entrie for the new positions of the Agents are the same for each of those arrays
the diffrence is that the AgentArray always only contains a value at the positions of the agents
the PheromoneArray on the other side gets multiplied by the factor 0.99 team it gets updated so that older values get smaller.
the Value 1 for update_agent_position and 50 for update_pheromone are choosen randomly, 
here we should think about what values would make sense.
"""


class AgentArray:
    def __init__(self, x_len, y_len):
        self.array = np.zeros((x_len, y_len), dtype=int)

    def update_agent_position(self, Agents_list):
        self.array = np.zeros_like(self.array, dtype=int)
        for agent in Agents_list:
            x, y, direction = agent[0], agent[1], agent[2]
            self.array[x, y] = 1


class PheromoneArray:
    def __init__(self, x_len, y_len):
        self.array = np.zeros((x_len, y_len), dtype=int)

    def update_pheromone(self, Agents_list):
        self.array = (self.array * 0.99).astype(int)
        for agent in Agents_list:
            x, y, direction = agent[0], agent[1], agent[2]
            self.array[x, y] = 50


"""
the Agents here have a radius, direction, position and num_agents
num_agents says how many agent shoud be initiated
the position is choosen randomly for each agent in the beginning and stored in the list Agents_list
the angle and the direction are not implemented yet, there is a value for the direction in the Agents_list, 
but it is not used in the code yet.
also the angle should be implemented, but this was too complicated for a quick tryout
I've realized that we have to find a way to store the direction of each agent 
so that we know at each time in what direction an agent is looking
"""


class Agent:
    def __init__(self, radius, agent_array, num_agents=10):
        self.radius = radius
        self.Agents_list = []
        self.direction = [1, 1]
        for idx in range(num_agents):
            x_pos = randint(0, agent_array.array.shape[0] - 1)
            y_pos = randint(0, agent_array.array.shape[1] - 1)
            self.Agents_list.append([x_pos, y_pos, self.direction])

    def move_Agents(self, Agents_list, array):
        for agent in Agents_list:
            x, y, direction = agent[0], agent[1], agent[2]
            moves = [(x, y), (x - 1, y - 1), (x + 1, y - 1)]

            # Find the move with the maximum value in the pheromone array or a random move
            max_move = random.choice(moves)

            # Update the agent's position based on the chosen move
            agent[0], agent[1] = max_move


"""
this method move_Agents was almost completly done by ChatGPT
here it is important to know that the method does not really find out what move would be the best next move, 
like where the most pheromones are
it just choose random a next move out of 3 options
there has to be a method implemented that compares all possible next moves depending on 
the direction the agent is facing, angle and radius, to decide the next move
"""


# This code is only to visualize an given array
def plot_large_array_with_colors(array):
    plt.imshow(array, interpolation="none", cmap="viridis")
    plt.show()


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
