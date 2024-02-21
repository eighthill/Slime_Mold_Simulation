from vispy import app, scene, gloo
from config import SlimeConfig
import simulation
from Ui_Slider_logic import SliderLogic
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QPushButton, QSpinBox
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
        app.Canvas.__init__(
            self,
        )
        self.qt_app = QApplication([])
        # Set up a timer for periodic updates
        self.timer = app.Timer(connect=self.on_timer, start=True)
        # Initialize the PheromoneArray and Agent instances
        p_array = simulation.PheromoneArray()
        self.agneten = simulation.Agent()
        
        
        self.parray = p_array.p_array
        self.agent = self.agneten.agenten  
        #self.simulation = simulation.move(self.agent)
        #Move = move(agents)
        self.view = scene.SceneCanvas(keys="interactive", size=(SlimeConfig.WIDTH, SlimeConfig.HEIGHT), show=True)
        self.view.events.draw.connect(self.on_draw)
        # Create an image visual representing the pheromone array
        # Create a markers visual to represent agents as pixels
        self.agent_markers = scene.visuals.Markers(parent=self.view.scene)
        # Create an image visual representing the pheromone array
        self.image = scene.visuals.Image(self.parray, cmap="inferno", parent=self.view.scene)
        #self.view.scene._add_child(self.agents_scatter)
        
        
        # Initialize the slider logic
        self.slider_logic = SliderLogic(self)

        # Show the slider widget
        self.slider_logic.slider_widget.show()
        
        self.slider_logic.agent_speed_slider.valueChanged.connect(self.update_agent_speed)
        self.slider_logic.agent_count_spinbox.valueChanged.connect(self.update_agent_count)
    
    def update_agent_speed(self):
        new_speed = self.slider_logic.agent_speed_slider.value()
        SlimeConfig.set_speed(new_speed)
        #print(f"Speed updated to: {new_speed}")
        
    def update_agent_count(self):
        new_agent_count = self.slider_logic.agent_count_spinbox.value()
        SlimeConfig.set_agent_count(new_agent_count)
        #print(new_agent_count)
        
        self.agneten = simulation.Agent()
        self.agent = self.agneten.agenten
        # Optionally, update visuals or any other dependent components here
        #self.restart_simulation()  # Restart simulation to apply the changes immediately
        
        # Update the label
        #self.slider_logic.agent_count_spinbox.value_label.setText(str(agent_count))
    
    def restart_simulation(self):
            # Reset the Pheromone Array
        self.parray = np.zeros_like(self.parray)  # Assuming a 2D array structure

        # Reinitialize the Agent instances
        # This step depends on how your agents are initially created. You might need to call the initial setup method.
        self.agneten = simulation.Agent()  # Recreate agent instances
        self.agent = self.agneten.agenten  # Reset agent positions

        # Optionally, reset any other simulation states or configurations here

        # Reset the visuals
        self.image.set_data(self.parray)  # Reset the display image to the cleared pheromone array
        self.agent_markers.set_data(pos=self.agent[:, :2], size=3, face_color=(1, 1, 1, 1))  # Reset agent visuals

        # Restart the simulation timer if needed
        #self.timer.start()

       #print("Simulation restarted")

    def on_draw(self, event):
        """
        Event handler for drawing on the canvas.
        Updates the visual representation of the pheromone array.
        """

        # Set the data of the image visual to the current pheromone array
        self.image.set_data(self.parray)
        
        self.agent[:, [0, 1]] = self.agent[:, [1, 0]]
        self.agent_markers.set_data(pos=self.agent[:, :2], size=4)
        self.agent[:, [1, 0]] = self.agent[:, [0, 1]]
       # positions = [(self.agnet[:, 1],self.agnet[:, 0]) for agenten in agenten]
        #positions = np.array([[agent["float_x_pos"], agent["float_y_pos"]] for agent in self.agents.Agents_list])
       # self.agneten_scatter.set_data(positions)

    def on_timer(self, event):
        """
        Event handler for the timer.
        Updates the pheromone array and agent movements periodically.
        """
        self.parray, self.agent = simulation.main(self.parray, self.agent)
        self.image.set_data(self.parray)
        self.view.scene.update()

    

if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    
    gui.qt_app.exec_()
    app.run()