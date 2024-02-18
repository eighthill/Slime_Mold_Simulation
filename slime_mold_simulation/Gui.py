from vispy import app, scene

from simulation import Agent, PheromoneArray, main_easy


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
        self.view = scene.SceneCanvas(keys="interactive", size=(100, 100), show=True)
        self.view.events.draw.connect(self.on_draw)
        # Create an image visual representing the pheromone array
        self.image = scene.visuals.Image(self.parray, cmap="viridis", parent=self.view.scene)

    def on_draw(self, event):
        """
        Event handler for drawing on the canvas.
        Updates the visual representation of the pheromone array.
        """

        # Set the data of the image visual to the current pheromone array
        self.image.set_data(self.parray)

    def on_timer(self, event):
        """
        Event handler for the timer.
        Updates the pheromone array and agent movements periodically.
        """
        self.parray,self.agnet=main_easy(self.parray,self.agnet)
        # Update the Vispy scene to reflect the changes
        self.view.scene.update()


if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    app.run()