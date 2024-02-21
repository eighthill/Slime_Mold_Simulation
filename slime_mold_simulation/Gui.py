from vispy import app, scene
import numpy as np

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
        agent = Agent()
        self.parray = p_array.p_array
        self.agent = agent.agenten

        self.view = scene.SceneCanvas(keys="interactive", size=(HEIGHT, WIDTH), show=True)
        self.view.events.draw.connect(self.on_draw)
        
        # Create a markers visual to represent agents as pixels
        self.agent_markers = scene.visuals.Markers(parent=self.view.scene)
        # Create an image visual representing the pheromone array
        self.image = scene.visuals.Image(self.parray, cmap="inferno", parent=self.view.scene)

    def on_draw(self, event):
        """
        Event handler for drawing on the canvas.
        Updates the visual representation of the pheromone array.
        """
        # Set the data of the image visual to the current pheromone array
        self.image.set_data(self.parray)
        self.agent[:, [0, 1]] = self.agent[:, [1, 0]]
        self.agent_markers.set_data(pos=self.agent[:, :2], size=3, face_color=(1, 1, 1, 1)) #weiß(1, 1, 1, 1), grün(0, 0, 1, 1), blau(0, 1, 0, 1), rot(1, 0, 0, 1)
        self.agent[:, [1, 0]] = self.agent[:, [0, 1]]
        
        # Set the position of the agent visual to the current position of the agents
        
    def on_timer(self, event):
        """
        Event handler for the timer.
        Updates the pheromone array and agent movements periodically.
        """
        self.parray, self.agent = main(self.parray, self.agent)
        self.image.set_data(self.parray)
        self.view.scene.update()


if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    app.run()
