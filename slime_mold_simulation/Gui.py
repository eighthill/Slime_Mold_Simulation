from vispy import app, scene
from simulation import PheromoneArray, Agent


class SimulationGUI(app.Canvas):
    def __init__(self):
        """
        Initialize the Simulation GUI.

        This class sets up the canvas, a timer for periodic updates,
        initializes the PheromoneArray, Agent instances, and creates
        a visual representation of the pheromone array using Vispy.
        """
        app.Canvas.__init__(
            self,
        )
        self.timer = app.Timer(connect=self.on_timer, start=True)
        self.pheromone = PheromoneArray()
        self.agents = Agent(self.pheromone)
        self.view = scene.SceneCanvas(keys="interactive", size=(1900, 1080), show=True)
        self.view.events.draw.connect(self.on_draw)
        self.image = scene.visuals.Image(self.pheromone.world, cmap="viridis", parent=self.view.scene)

    def on_draw(self, event):
        """
        Event handler for drawing on the canvas.

        Updates the visual representation of the pheromone array.
        """
        self.image.set_data(self.pheromone.world)

    def on_timer(self, event):
        """
        Event handler for the timer.

        Updates the pheromone array and agent movements periodically.
        """
        self.pheromone.update_pheromone(self.agents.Agents_list)
        self.agents.make_move(self.pheromone)
        self.view.scene.update()


if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    app.run()