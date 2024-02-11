from vispy import app, scene
from simulation import Agent, PheromoneArray
import numpy as np
from vispy.color import Color
from vispy.scene import visuals


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

        self.pheromone = PheromoneArray()
        self.agents = Agent(self.pheromone)

        # Set up a timer for periodic updates
        self.timer = app.Timer(connect=self.on_timer, start=True)

        # Create a black background
        self.view = scene.SceneCanvas(keys="interactive", size=(100, 100), show=True)
        self.view.bgcolor = Color("black")

        # Create yellow points visual
        self.points = visuals.Markers()
        self.view.scene._add_child(self.points)

        # Set initial points (just as an example)
        self.update_points([])

    def update_points(self, points):
        """
        Update the positions of yellow points.
        """
        # Convert points to numpy array
        points_array = np.array(points, dtype=np.float32)

        # Reshape points array if necessary
        if points_array.ndim == 1:
            points_array = points_array.reshape(-1, 2)

        # Set data for points
        self.points.set_data(pos=points_array, face_color="yellow", size=2)

    def on_timer(self, event):
        """
        Event handler for the timer.

        Updates the positions of yellow points periodically.
        """
        # Update the pheromone array based on agent positions
        self.pheromone.update_pheromone(self.agents.Agents_list)
        # Update the agent movements
        self.agents.make_move(self.pheromone)
        # Update the Vispy scene to reflect the changes
        self.view.scene.update()

        # Example: Update points every timer event
        new_points = []
        for agent in self.agents.Agents_list:
            new_points.append((agent["float_x_pos"], agent["float_y_pos"]))
        self.update_points(new_points)


if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    app.run()
