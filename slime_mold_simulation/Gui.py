from simulation import Agent, PheromoneArray,main_simple,main_upgrade
import numpy as np
from vispy import app, gloo, scene
from simulation import Agent, PheromoneArray, AGENT_NUMBER, WIDTH, HEIGHT


p_array = PheromoneArray()
agneten = Agent()
parray = p_array.p_array
agnets = agneten.agenten

# Create a canvas
canvas = scene.SceneCanvas(keys="interactive", size=(HEIGHT,WIDTH), show=True)

# Create a view
view = canvas.central_widget.add_view()

# Create a shader program for agents
vertex_shader = """
attribute vec2 position;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

fragment_shader = """
void main()
{
    gl_FragColor = vec4(1.0, 0.0, 0.0, 1.0);
}
"""

program = gloo.Program(vertex_shader, fragment_shader)


# [Agent(x=np.random.uniform(300, 600), y=np.random.uniform(300, 600)) for _ in range(AGENT_NUMBER)]

# Create agent visuals
markers = scene.visuals.Markers(parent=view.scene, symbol="disc", size=0.1, face_color="red")
markers.set_data(np.array([[agent[0], agent[1]] for agent in agnets], dtype=np.float32))

# Set camera view
view.camera = 'panzoom'


# Timer callback to update agent positions and redraw
def update_timer(parray,agnets):

    (parray,agnets) = main_upgrade(parray,agnets)
    agent_positions = np.array([[agent[0], agent[1]] for agent in agnets], dtype=np.float32)
    markers.set_data(agent_positions)

    # Clear the canvas before redrawing
    canvas.render()

    # Draw all marker visuals
    markers.draw()

    # Swap the buffer (show the rendered image)
    canvas.update()


# Create a timer to update positions
timer = app.Timer("auto", connect=lambda ev: update_timer(parray, agnets), start=True)

# Run the application
if __name__ == "__main__":
    app.run()