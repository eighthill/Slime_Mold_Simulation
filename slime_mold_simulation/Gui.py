from vispy import app, scene

import config
from simulation import Agent, PheromoneArray, main

WIDTH = config.WIDTH
HEIGHT = config.HEIGHT
DECAY = config.DECAY
DIFFUSION_COEFFICENT = config.DIFFUSION_COEFFICENT
AGENT_NUMBER = config.AGENT_NUMBER
SPEED = config.SPEED
SENSOR_DISTANCE = config.SENSOR_DISTANCE
ROTATION_SPEED = config.ROTATION_SPEED
SENSOR_ANGLE = config.SENSOR_ANGLE


class SimulationGUI(app.Canvas):
    def __init__(self):
        """
        Initialize the Simulation GUI.
        This class sets up the canvas, a timer for periodic updates,
        initializes the PheromoneArray, Agent instances, and creates
        a visual representation of the pheromone array using Vispy.
        """
        # Initialize the Vispy canvas
        app.Canvas.__init__(
            self,
        )
        # Set up a timer for periodic updates

        self.timer = app.Timer(connect=self.on_timer, start=True)
        # Initialize the PheromoneArray and Agent instances
        p_array = PheromoneArray()
        agneten = Agent()
        self.parray = p_array.p_array
        self.agnet = agneten.agenten

        self.view = scene.SceneCanvas(keys="interactive", size=(HEIGHT, WIDTH), show=True)
        self.view.events.draw.connect(self.on_draw)
        # Create a visual representing the agents
        self.agents = scene.visuals.Markers(pos=self.agnet[:, :2],parent=self.view.scene)

        # Create an image visual representing the pheromone array
        self.image = scene.visuals.Image(self.parray, cmap="inferno", parent=self.view.scene)
        
    def on_draw(self, event):
        """
        Event handler for drawing on the canvas.
        Updates the visual representation of the pheromone array.
        """
        # Set the data of the image visual to the current pheromone array
        self.image.set_data(self.parray)
        # Set the position of the agent visual to the current position of the agents
        self.agnet[:, [0, 1]] = self.agnet[:, [1, 0]]
        self.agents.set_data(pos=self.agnet[:, :2])
        self.agnet[:, [1, 0]] = self.agnet[:, [0, 1]]

    def on_timer(self, event):
        """
        Event handler for the timer.
        Updates the pheromone array and agent movements periodically.
        """
        self.parray, self.agnet = main(self.parray, self.agnet)
        self.agents.set_data(pos=self.agnet[:, :2])
        self.view.scene.update()

if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    app.run()
