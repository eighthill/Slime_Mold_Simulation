from vispy import app, scene
import numpy as np
from vispy import app, scene
from vispy.color import Color
from vispy.scene import visuals

from simulation import Agent, PheromoneArray


class SimulationGUI(app.Canvas):
    def __init__(self):
        """
        Initialize the Simulation GUI.
        This class sets up the canvas, a timer for periodic updates,
        initializes the PheromoneArray, Agent instances, and creates
        a visual representation of the pheromone array using Vispy.
        """
        # Initialize the Vispy canvas
        app.Canvas.__init__(self)

        # Set up a timer for periodic updates
        self.timer = app.Timer(connect=self.on_timer, start=True)

        # Initialize the PheromoneArray and Agent instances
        self.pheromone = PheromoneArray()
        self.agents = Agent(self.pheromone)

        # Initialize the Vispy scene
        self.view = scene.SceneCanvas(keys="interactive", size=(1000, 1000), show=True)
        self.view.events.draw.connect(self.on_draw)

        # Create Points visual for agents
        self.agent_points = visuals.Markers()
        self.view.scene._add_child(self.agent_points)

        # Create an image visual representing the pheromone array
        self.image = scene.visuals.Image(self.pheromone.world, cmap="plasma", parent=self.view.scene)
        self.view.scene._add_child(self.image)

    def on_draw(self, event):
        """
        Event handler for drawing on the canvas.
        Updates the visual representation of the pheromone array and agents.
        """

        # Set the data of the image visual to the current pheromone array
        self.image.set_data(self.pheromone.world)

        # Update the positions of agent points
        agent_positions = np.array([[agent["float_x_pos"], agent["float_y_pos"]] for agent in self.agents.Agents_list])
        self.agent_points.set_data(pos=agent_positions, edge_color='blue', size=15)

    def on_timer(self, event):
        """
        Event handler for the timer.
        Updates the pheromone array and agent movements periodically.
        """

        # Update the pheromone array based on agent positions
        self.pheromone.update_pheromone(self.agents.Agents_list)

        # Update agent movements
        self.agents.follow_pheromones()

        # Trigger a redraw of the scene
        self.view.update()



if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    app.run()