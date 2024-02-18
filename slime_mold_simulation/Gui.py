from vispy import app, scene
from PyQt5.QtWidgets import QApplication
import numpy as np
from simulation import Agent, PheromoneArray
from SlimeConfig import SlimeConfig
import random

class SimulationGUI(app.Canvas):
    def __init__(self):
        super().__init__()
        self.qt_app = QApplication([])
        self.timer = app.Timer('auto', connect=self.on_timer)
        self.pheromone = PheromoneArray()
        self.view = scene.SceneCanvas(keys='interactive', size=(1100, 1100), show=True)
        self.image = scene.visuals.Image(self.pheromone.world.astype(np.float32), parent=self.view.scene)
        self.agents_scatter = scene.visuals.Markers()
        self.view.scene._add_child(self.agents_scatter)
        # Initialize agents
        self.initialize_agents()

    def initialize_agents(self):
        center_x, center_y = self.view.size[0] // 2, self.view.size[1] // 2
        # Adjust Agent.initialize_agents if necessary to match this call
        agent_params = Agent.initialize_agents(center_x=center_x, center_y=center_y, num_agents=SlimeConfig.num_agents, radius=250, move_speed=SlimeConfig.move_speed, world_x=self.view.size[0], world_y=self.view.size[1], pheromone_array=self.pheromone.world)
        self.agents_data = [Agent(x=param['x'], y=param['y'], movement_angle=param['movement_angle'], pheromone_array=self.pheromone.world, move_speed=param['move_speed'], turn_speed=SlimeConfig.turn_speed, sensor_distances=SlimeConfig.sensor_distances, sensor_angles=SlimeConfig.sensor_angles, random_move=random.choice([True, False])) for param in agent_params]

    def on_draw(self, event):
        self.image.set_data(self.pheromone.world.astype(np.float32))
        positions = np.array([[agent.x, agent.y] for agent in self.agents_data])
        self.agents_scatter.set_data(positions, size=5, edge_color='white', face_color='white')
        self.update()
    
    def on_timer(self, event):
        for agent in self.agents_data:
            agent.update()
        self.pheromone.update_pheromone(self.agents_data)
        self.update()

    

if __name__ == "__main__":
    gui = SimulationGUI()
    gui.show()
    app.run()
