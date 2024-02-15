from vispy import app, scene
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QPushButton, QSpinBox
from simulation import Agent, PheromoneArray, SlimeConfig
import numpy as np
from Ui_Slider import SliderLogic

class SimulationGUI(app.Canvas):
    def __init__(self):
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

        # Initialize PyQt5 application
        self.qt_app = QApplication([])

        # Initialize the slider logic
        self.slider_logic = SliderLogic(self)

        # Show the slider widget
        self.slider_logic.slider_widget.show()
        
        # Connect the resize event to the on_resize method
     #   self.view.events.resize.connect(self.on_resize)

    def update_agent_size(self):
        size = self.slider_logic.agent_size_slider.value()
        self.agents_scatter.set_data(size=size)

        # Update the label
        self.slider_logic.agent_size_slider.value_label.setText(str(size))

    def update_agent_speed(self):
        slider_value = self.slider_logic.agent_speed_slider.value() / 10
        min_speed = 0.01
        max_speed = 0.1
        speed = slider_value * (max_speed - min_speed)
        self.agents.speed = speed

        # Update the label
        #self.slider_logic.agent_speed_slider.value_label.setText(f"{speed:.2f}")

    def update_agent_count(self):
        agent_count = self.slider_logic.agent_count_spinbox.value()
        self.agents = Agent(self.pheromone, num_agents=agent_count)

        # Update the label
        #self.slider_logic.agent_count_spinbox.value_label.setText(str(agent_count))

    def update_fading(self):
        slider_value = self.slider_logic.fading_slider.value() / 100
        SlimeConfig.fading = slider_value

        # Update the label
        #self.slider_logic.fading_slider.value_label.setText(f"{slider_value:.2f}")

    def update_diffusion_coefficient(self):
        slider_value = self.slider_logic.diffusion_coefficient_slider.value() / 100
        SlimeConfig.diffusion_coefficient = slider_value

        # Update the label
        #self.slider_logic.diffusion_coefficient_slider.value_label.setText(f"{slider_value:.2f}")

    def update_pheromone_value(self):
        slider_value = self.slider_logic.pheromone_value_slider.value() / 100
        SlimeConfig.pheromone_value = slider_value

        # Update the label
        #self.slider_logic.pheromone_value_slider.value_label.setText(f"{slider_value:.2f}")
        
    def restart_simulation(self):
        self.pheromone = PheromoneArray()
        self.agents = Agent(self.pheromone)

    def on_draw(self, event):
        """
        Event handler for drawing on the canvas.
        Updates the visual representation of the pheromone array and agents.
        """

        # Set the data of the image visual to the current pheromone array
        self.image.set_data(self.pheromone.world)

        # Set the positions of agents in the scatter plot visual
        # positions = np.array([[agent["float_x_pos"], agent["float_y_pos"]] for agent in self.agents.Agents_list])
        # self.agents_scatter.set_data(positions, edge_color='blue', size=15)

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
        
   # def on_resize(self, event):
    #    """
     #   Event handler for resizing the window.
      #  Update the size of the Vispy SceneCanvas and the PheromoneArray.
       # """
        #new_size = event.size[0], event.size[1]
        #self.view.size = new_size
        #self.image.set_data(self.pheromone.world)

        # Update the size of the PheromoneArray
        #self.pheromone = PheromoneArray(x_len=new_size[0], y_len=new_size[1])

if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    # Start the PyQt5 application loop
    gui.qt_app.exec_()
    app.run()