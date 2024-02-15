from vispy import app, scene
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout
from simulation import Agent, PheromoneArray
import numpy as np

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
        self.view = scene.SceneCanvas(keys="interactive", size=(1000, 1000), show=True)
        self.view.events.draw.connect(self.on_draw)
        # Create an image visual representing the pheromone array
        self.image = scene.visuals.Image(self.pheromone.world, cmap="viridis", parent=self.view.scene)
        # Create a scatter plot visual for agents
        self.agents_scatter = scene.visuals.Markers()
        self.view.scene._add_child(self.agents_scatter)

        # Initialize PyQt5 application and create a widget for the slider
        self.qt_app = QApplication([])
        self.slider_widget = QWidget()
        self.slider_layout = QVBoxLayout(self.slider_widget)
        
        # Create a slider to control the agent size
        self.agent_size_slider = QSlider()
        self.agent_size_slider.setMinimum(5)
        self.agent_size_slider.setMaximum(30)
        self.agent_size_slider.setValue(15)
        self.agent_size_slider.setOrientation(1)  # Vertical orientation
        self.agent_size_slider.valueChanged.connect(self.update_agent_size)
        
        # Add the slider to the layout
        self.slider_layout.addWidget(QLabel("Agent Size"))
        self.slider_layout.addWidget(self.agent_size_slider)
        
        # Set up the layout of the slider widget
        self.slider_widget.setLayout(self.slider_layout)

        # Show the slider widget
        self.slider_widget.show()

    def update_agent_size(self):
        """
        Update agent size based on the slider value.
        """
        size = self.agent_size_slider.value()
        self.agents_scatter.set_data(size=size)

    def on_draw(self, event):
        """
        Event handler for drawing on the canvas.
        Updates the visual representation of the pheromone array and agents.
        """

        # Set the data of the image visual to the current pheromone array
        self.image.set_data(self.pheromone.world)

        # Set the positions of agents in the scatter plot visual
        positions = np.array([[agent["float_x_pos"], agent["float_y_pos"]] for agent in self.agents.Agents_list])
        self.agents_scatter.set_data(positions, edge_color='blue', size=self.agent_size_slider.value())

    def on_timer(self, event):
        """
        Event handler for the timer.
        Updates the pheromone array and agent movements periodically.
        """

        # Update the pheromone array based on agent positions
        self.pheromone.update_pheromone(self.agents.Agents_list)
        # Update the agent movements
        self.agents.make_move(self.pheromone)
        # Trigger a redraw of the scene
        self.view.scene.update()

if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    
    # Start the PyQt5 application loop
    gui.qt_app.exec_()
    app.run()