from vispy import app, scene

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
        app.Canvas.__init__(
            self,
        )

        # Set up a timer for periodic updates
        self.timer = app.Timer(connect=self.on_timer, start=True)
        # Initialize the PheromoneArray and Agent instances
        self.pheromone = PheromoneArray()
        self.agents = Agent(self.pheromone)
        self.view = scene.SceneCanvas(keys="interactive", size=(100, 100), show=True)
        self.view.events.draw.connect(self.on_draw)
        # Create an image visual representing the pheromone array
        self.image = scene.visuals.Image(self.pheromone.world, cmap="viridis", parent=self.view.scene)

    def on_draw(self, event):
        """
        Event handler for drawing on the canvas.

        Updates the visual representation of the pheromone array.
        """

        # Set the data of the image visual to the current pheromone array
        self.image.set_data(self.pheromone.world)

    def on_timer(self, event):
        """
        Event handler for the timer.

        Updates the pheromone array and agent movements periodically.
        """

        # Update the pheromone array based on agent positions
        self.pheromone.update_pheromone(self.agents.Agents_list)
        # Update the agent movements
        self.agents.make_move(self.pheromone)
        # Update the Vispy scene to reflect the changes
        self.view.scene.update()


if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    app.run()
