import sys
from pathlib import Path

import numpy as np
from PyQt5.QtWidgets import QApplication
from vispy import app, scene

from Ui_Slider_logic import SliderLogic  # noqa: E402

project_root = Path(__file__).resolve().parent.parent  # noqa: E402
sys.path.append(str(project_root))  # noqa: E402
from cfg_sim.world_cfg import SlimeConfig  # noqa: E402

import simulation  # noqa: E402


class SimulationGUI(app.Canvas):
    """Graphical User Interface for the Slime Simulation."""

    def __init__(self):
        """
        Initializes the GUI, sets up the canvas, a timer for periodic updates,
        Instantiates the pheromone array and agent and creates
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
        self.agenten = simulation.Agent()

        self.parray = p_array.p_array
        self.agent = self.agenten.agenten
        # self.simulation = simulation.move(self.agent)
        # Move = move(agents)
        self.view = scene.SceneCanvas(
            keys="interactive",
            size=(SlimeConfig.WIDTH, SlimeConfig.HEIGHT),
            show=True,
            vsync=True,
        )
        self.view.events.draw.connect(self.on_draw)
        # Create an image visual representing the pheromone array
        # Create a markers visual to represent agents as pixels
        self.agent_markers = scene.visuals.Markers(parent=self.view.scene)
        # Create an image visual representing the pheromone array
        self.image = scene.visuals.Image(self.parray, cmap="inferno", parent=self.view.scene)
        # self.view.scene._add_child(self.agents_scatter)

        # Initialize the slider logic
        self.slider_logic = SliderLogic(self)

        # Show the slider widget
        self.slider_logic.slider_widget.show()

        self.slider_logic.agent_count_spinbox.valueChanged.connect(self.update_agent_count)
        self.slider_logic.agent_speed_spinbox.valueChanged.connect(self.update_agent_speed)
        self.slider_logic.decay_spinbox.valueChanged.connect(self.update_decay)
        self.slider_logic.diff_spinbox.valueChanged.connect(self.update_diff)
        self.slider_logic.sen_dis_spinbox.valueChanged.connect(self.update_sen_dis)
        self.slider_logic.rota_speed_spinbox.valueChanged.connect(self.update_rota_speed)
        self.slider_logic.sen_angle_spinbox.valueChanged.connect(self.update_sen_angle)
        # self.slider_logic.time_step_spinbox.valueChanged.connect(self.update_time_step)

    # Update function for simulation parameters based on UI control changes
    def update_agent_speed(self):
        new_speed = self.slider_logic.agent_speed_spinbox.value()
        SlimeConfig.set_speed(new_speed)

    # Update function for simulation parameters based on UI control changes
    def update_agent_count(self):
        new_agent_count = self.slider_logic.agent_count_spinbox.value()
        SlimeConfig.set_agent_count(new_agent_count)

        self.agenten = simulation.Agent()
        self.agent = self.agenten.agenten

    # Update function for simulation parameters based on UI control changes
    def update_decay(self):
        new_decay = self.slider_logic.decay_spinbox.value()
        SlimeConfig.set_decay(new_decay)

    # Update function for simulation parameters based on UI control changes
    def update_diff(self):
        new_diff = self.slider_logic.diff_spinbox.value()
        SlimeConfig.set_diff(new_diff)

    # Update function for simulation parameters based on UI control changes
    def update_sen_dis(self):
        new_sen_dis = self.slider_logic.sen_dis_spinbox.value()
        SlimeConfig.set_sen_dis(new_sen_dis)

    # Update function for simulation parameters based on UI control changes
    def update_rota_speed(self):
        new_rota_speed = self.slider_logic.rota_speed_spinbox.value()
        SlimeConfig.set_rota_speed(new_rota_speed)

    # Update function for simulation parameters based on UI control changes
    def update_sen_angle(self):
        new_sen_angle = self.slider_logic.sen_angle_spinbox.value()
        SlimeConfig.set_sen_angle(new_sen_angle)

    # Update function for simulation parameters based on UI control changes
    def update_time_step(self):
        new_time_step = self.slider_logic.time_step_spinbox.value()
        SlimeConfig.set_time_step(new_time_step)

    def restart_simulation(self):
        """
        Resets the simulation to its initial state, including reinitializing the agent
        positions and clearing the pheromone array.
        """
        self.parray = np.zeros_like(self.parray)

        # Reinitialize the Agent instances
        self.agenten = simulation.Agent()  # Recreate agent instances
        self.agent = self.agenten.agenten  # Reset agent positions

        # Reset the visuals
        self.image.set_data(self.parray)  # Reset the display image to the cleared pheromone array
        self.agent_markers.set_data(pos=self.agent[:, :2], size=3, face_color=(1, 1, 1, 1))  # Reset agent visuals

    def on_draw(self, event):
        """
        Event handler for drawing on the canvas.
        Updates the visual representation of the pheromone array.
        """

        # Set the data of the image visual to the current pheromone array
        self.image.set_data(self.parray)

        self.agent[:, [0, 1]] = self.agent[:, [1, 0]]
        self.agent_markers.set_data(pos=self.agent[:, :2], size=1)
        self.agent[:, [1, 0]] = self.agent[:, [0, 1]]

    def on_timer(self, event):
        """
        Event handler for the timer.
        Updates the pheromone array and agent movements periodically.
        """
        self.parray, self.agent = simulation.main(self.parray, self.agent)
        self.image.set_data(self.parray)
        self.view.scene.update()

    def closeEvent(self, event):
        self.timer.stop()  # Stop the timer
        event.accept()  # Accept the window close event
        self.qt_app.quit()  # Quit the Qt application
        exit()


if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()

    gui.qt_app.exec_()
    app.run()
