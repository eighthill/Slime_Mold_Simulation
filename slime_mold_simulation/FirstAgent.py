# Import necessary modules

import sys
import random
from vispy import app, gloo

# Set the initial position and speed of the agents
agents = [{"x": 0.5, "y": 0.5, "vx": random.uniform(-1, 1), "vy": random.uniform(-1, 1)} for _ in range(1)]
SPEED = 0.009

# Create a simple vertex shader
vertex_shader = """
attribute vec2 position;
void main()
{
    gl_Position = vec4(position, 0.0, 1.0);
}
"""

# Create a simple fragment shader (thats white)
fragment_shader = """
void main()
{
    gl_FragColor = vec4(1.0, 1.0, 1.0, 1.0);
}
"""

# Create the canvas and program
canvas = app.Canvas(keys="interactive")

program = gloo.Program(vertex_shader, fragment_shader)

# Set the initial positions of the agents
program["position"] = [(agent["x"], agent["y"]) for agent in agents]


# Define the update function
def update(ev):
    # Update the position of the agent based on its velocity
    for agent in agents:
        agent["x"] += agent["vx"] * SPEED
        agent["y"] += agent["vy"] * SPEED

        # Reflect the agent if it hits the boundaries
        if agent["x"] > 1 or agent["x"] < 0:
            agent["vx"] *= -1
        if agent["y"] > 1 or agent["y"] < 0:
            agent["vy"] *= -1
    # Update the positions in the program and trigger canvas update
    program["position"] = [(agent["x"], agent["y"]) for agent in agents]
    canvas.update()


# Create a timer to update the simulation
timer = app.Timer(interval=0.01, connect=update)
timer.start()

# Define the paint function
@canvas.connect
def on_draw(event):
    # Clear the canvas and draw the points using the program
    gloo.clear()
    program.draw("points")


# Run the application
if __name__ == "__main__":
    canvas.show()
    # Start the application event loop
    if sys.flags.interactive == 0:
        app.run()
