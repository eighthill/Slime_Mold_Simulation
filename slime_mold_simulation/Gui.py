from vispy import app, scene, gloo
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QSlider, QVBoxLayout, QPushButton, QSpinBox
from simulation import Agent, PheromoneArray
import numpy as np
from SlimeConfig import SlimeConfig
from Move import  sense, sense_and_move, mapping_float_to_int, mapping_int_to_float, reflect_at_boundary 
import random

class SimulationGUI(app.Canvas):
    def __init__(self):
        app.Canvas.__init__(self)
        self.qt_app = QApplication([])
        self.timer = app.Timer(connect=self.on_timer, start=True)
        self.pheromone = PheromoneArray()
        self.view = scene.SceneCanvas(keys="interactive", size=(1100, 1100), show=True)
        center_x = self.view.size[0] // 2
        center_y = self.view.size[1] // 2
        self.view.events.draw.connect(self.on_draw)
        self.image = scene.visuals.Image(self.pheromone.world, cmap="inferno", parent=self.view.scene)
        self.agents_scatter = scene.visuals.Markers()
        self.view.scene._add_child(self.agents_scatter)
        # Initialize agents using the static method from the Agent class
        world_x, world_y = self.pheromone.world.shape
        self.canvas_width, self.canvas_height = self.view.size
        self.agents_data = [Agent(**agent_params, random_move=random.choice([True, False])) for agent_params in Agent.initialize_agents(
            center_x=center_x, 
            center_y=center_y, 
            num_agents=10,  # Adjust as needed
            radius=250,  # Adjust as needed
            move_speed=SlimeConfig.move_speed,
            world_x=world_x,
            world_y=world_y,            
        )]
        
    def on_draw(self, event):
        
        #self.agents_scatter.set_data(pos=positions, size=15)
        self.image.set_data(self.pheromone.world)
        positions = np.array([[agent.x, agent.y] for agent in self.agents_data])

    def on_timer(self, event):
        self.pheromone.update_pheromone(self.agents_data)
        
        for agent in self.agents_data:
            # Pass the canvas width and height to the sense_and_move function
            agent.sense_and_move(self.pheromone.world, SlimeConfig.sensor_distances, SlimeConfig.sensor_angles,
                                 SlimeConfig.move_speed, SlimeConfig.turn_speed,
                                 self.canvas_width, self.canvas_height)
        
       # [agent.sense_and_move(self.pheromone.world, SlimeConfig.sensor_distances, SlimeConfig.sensor_angles, SlimeConfig.move_speed, SlimeConfig.turn_speed) for agent in self.agents_data]
            
        self.view.update()


if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    
    # Start the PyQt5 application loop
    gui.qt_app.exec_()
    app.run()