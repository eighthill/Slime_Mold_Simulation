import sys
import numpy as np
from vispy import app, scene, visuals

class SliderOverlay(scene.SceneCanvas):
    def __init__(self, simulation_object):
        scene.SceneCanvas.__init__(self, keys='interactive', show=True)

        self.unfreeze()
        self.simulation_object = simulation_object

        self.view = self.central_widget.add_view()
        self.view.camera = 'panzoom'

        self.slider_line = visuals.Line(pos=np.array([[0, 0], [1, 0]]), color='white', method='gl')
        self.slider_handle = visuals.Markers(pos=np.array([[0, 0]]), size=20, symbol='o', face_color='red', edge_color='black')

        self.view.add(self.slider_line)
        self.view.add(self.slider_handle)

        self.freeze()

        self.events.key_press.connect(self.on_key_press)
        self.events.mouse_press.connect(self.on_mouse_press)
        self.events.mouse_release.connect(self.on_mouse_release)
        self.events.mouse_move.connect(self.on_mouse_move)

        self.slider_value = 0.5  # Initial slider value
        self.update_slider()

    def update_slider(self):
        handle_pos = np.array([[self.slider_value, 0]])
        self.slider_handle.set_data(pos=handle_pos)
        self.simulation_object.update_parameter(self.slider_value)

    def on_key_press(self, event):
        if event.key == 'Right':
            self.slider_value = min(1.0, self.slider_value + 0.1)
            self.update_slider()
        elif event.key == 'Left':
            self.slider_value = max(0.0, self.slider_value - 0.1)
            self.update_slider()

    def on_mouse_press(self, event):
        if event.button == 1:  # Left mouse button
            self.dragging = True

    def on_mouse_release(self, event):
        if event.button == 1:  # Left mouse button
            self.dragging = False

    def on_mouse_move(self, event):
        if self.dragging:
            pos = self.view.canvas.transforms.canvas_transform.map(event.pos)
            self.slider_value = max(0.0, min(1.0, pos[0] / self.view.size[0]))
            self.update_slider()


class SimulationObject:
    def __init__(self):
        # Your simulation initialization code here
        pass

    def update_parameter(self, slider_value):
        # Update simulation parameters based on the slider value
        print(f"Updating simulation with slider value: {slider_value}")


if __name__ == '__main__':
    simulation_object = SimulationObject()
    slider_overlay = SliderOverlay(simulation_object)
    app.run()
