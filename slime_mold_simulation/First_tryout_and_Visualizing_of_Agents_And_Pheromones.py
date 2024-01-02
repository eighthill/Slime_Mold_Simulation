import numpy as np

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
