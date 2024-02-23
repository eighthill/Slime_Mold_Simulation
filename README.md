# How to use Slime Mold Simulation

## Introduction

This document provides guidance on how to get the slime mold simulation program running on your computer. This simulation visualizes the complex behavior of slime mold agents as they navigate and interact in their environment.

## Installation

Before you begin, ensure you have Python installed on your computer. This program requires at least Python 3.8 and several dependencies, including Vispy, a library for interactive scientific visualization.

## Steps for Installation: 
1. Install Pyhton 3.8 or newer from the [offical Pyhton website](https://www.python.org/downloads/).
2. Download the Program: Ensure you have all Files in a Folder. [click here to download](https://github.com/eighthill/Slime_Mold_Simulation/archive/refs/heads/main.zip)
3. Install Dependencies: Open your terminal or command prompt and navigate to the program's directory. Install the required Python libraries.
- `pip install vispy`
- `pip install numpy`
- `pip intall scipy`
- `pip install PyQt5`
     
## Starting the Program
After you have made all the installations, you can start the simulation program.
1. Open Terminal/Command Prompt: Navigate to the folder via
   - `cd ~/.../Silme_Mold_Simulation`
2. Run the Program: Execute the following command.
   - `python Gui.py`
  This will launch the graphical user interface

## What you can do in the program
Our Program creates a virtual environment where our slime / mold agents interact with each other. These agents simulate the behavior of real mold by moving to areas with higher concentrations of a virtual substance (pheromones) in the environment. As the agents move, they leave a trail (pheromones) that can attract other agents. The simulation includes processes that show how these pheromones diffuse and fade over time, and how the agents decide where to go based on the pheromones they detect. This shows intelligent behavior that can be traced back to the real unicellulars from the real world. The agents creat intersting patterns/pathways. Depending on the parameters you can visualize very different behivours.

## Using manual
The simulation can get unstable really easy. Especially the Sensor Angle and Randome factor can brake the agents so they stop moving!
We have collected some parameters which can help out in the beginning. Set the values for each simulation and restart the simulation for simillar results.

Example parameters:
---
Agent speed: 2
Agent count: 50000
Decay: 0,9
Diffusion coefficent: 0,95
Sensor distance: 10
Rotation speed: 0,3
Sensor Angle: 26
Randome factor: 0,1

Visual:
https://cdn.discordapp.com/attachments/1030079280794837013/1210413959669088287/VisPy_canvas_2024-02-23_02-53-23.gif?ex=65ea78d8&is=65d803d8&hm=8a2c68f374aed096f460e02555950ff5c3d01fde0d2df46a2f3f670ae04a1611&
---
Agent speed: 4
Agent count: 50000
Decay: 0,97
Diffusion coefficent: 0,97
Sensor distance: 15
Rotation speed: 0,2
Sensor Angle: 5
Randome factor: 0,02

Visual:
https://cdn.discordapp.com/attachments/1030079280794837013/1210413258574659704/VisPy-canvas-2024-02-23-03-03-13.gif?ex=65ea7831&is=65d80331&hm=f0d814ccef7314b73289f43a201a948ab850005b378af82ca6c2d7676c2dd3e69&
---

# For Developer 
## Developer Documentation
The documentation is especially for developers who are interested in getting a better understanding of our program.  Here you will find a detailed overview of how the classes and methods are structured and how they interact. You are also welcome to give us feedback for the code, if something was programmed too complicated or anything else :).

First of all, we decided to structure everything as well as possible. This means that the simulation was not written in one file, but the logic of the simulation is in one file (simulation.py), the Gui (Gui.py), Config (config.py) and the sliders (Ui_Slider_logic.py) are each in separate files so that they can be better separated.

### Code structure as a diagram
![Picture of Code Structure](https://cdn.discordapp.com/attachments/1179079479230992425/1209953090120323102/image.png?ex=65e8cba0&is=65d656a0&hm=3acc8596537df45ce254a2d39ce9f6d1e8a483d1644d9f55a7083c556e95e730&)


### Simulation
So let's look specifically at our logic, that's the heart of the program where everything is done. This is where the magic happens, where the agents find their way.This file is designed to simulate the complex, emergent behavior of slime molds using a combination of agent-based modeling and pheromone interaction mechanics.
- **`PheromoneArray` Class:**  Manages the simulation's environment, specifically the pheromone levels across the grid.
- **`Agent` Class:** Represents individual slime mold agents, including their position and heading direction.
- **`diffuse` Function:** Applies a Gaussian filter to simulate pheromone diffusion throughout the environment.
- **`decay` Function:** Reduces pheromone strength over time to simulate natural decay.
- **`get_sensors` Function:** Calculates sensor positions for agents to detect pheromones.
- **`get_pheromone_value_at` Function:** Retrieves pheromone levels at specified sensor positions.
- **`reflect_boundary` Function:** Ensures agents stay within the environmental boundaries by reflecting their movement at edges.
- **`move` Function:** Updates agent positions based on their speed and heading direction.
- **`deposit_pheromone` Function:** Agents deposit pheromones into the environment at their current location.
- **`rotate_towards_sensor` Function:** Adjusts agent heading based on detected pheromone levels, encouraging movement towards stronger pheromone concentrations.
- **`main` Function:** Orchestrates the simulation steps, including sensor reading, rotation, movement, pheromone deposition, diffusion, and decay.

### Config
We have also separated the parameters into a config so that everything is more dynamic and easier to understand. 
- **`WIDTH, HEIGHT`** gives us the width and height of our field in which the agents will move
- **`DECAY`** is the value of how quickly the phermones disappear after a certain time
- **`DIFFUSION_COEFFICENT`** Is the value of diffusion how far the pheromones should spread
- **`AGENT_NUMBER`** How many Agents spawns 
- **`SPEED`** how fast the agents move
- **`SENSOR_DISTANCE`** how far the agents can see
- **`ROTATION_SPEED`** how quickly the agent turns after discovering the pheromone
- **`SENSOR_ANGLE`** how the sensors are arranged in relation to each other
- **`set_speed`** here we update the speed for the agents that is changed via the sliders
- **`set_agent_count`** changes the number of agents via the sliders 

### Gui
Next, let's take a look at the Gui.
The `Gui.py` file implements the graphical user interface (GUI) for the slime mold simulation using Vispy, a Python library for interactive scientific visualization and PyQT5 for the interface with sliders to adjust simulation parameters dynamically. These sliders control aspects such as agent speed and count, directly the simulation's behavior.
It defines a `SimulationGUI` class that initializes the simulation environment, including the **pheromone array** and **agent** instances, and sets up a Vispy canvas for visualization. This class handles drawing the agents and pheromone levels on the canvas and updates these visuals in response to simulation changes. Key functionalities include initiating the simulation GUI, drawing and updating visuals based on simulation data, and managing periodic updates through a timer event. This GUI component is crucial for visualizing the simulation's dynamics and interacting with the simulation parameters in real-time.
- **`SimulationGUI ` Class:** Sets up the simulation canvas, initializes pheromone and agent arrays, and creates visual representations for them.
- **`Constructor __init__` Method:** Initializes the canvas, sets a timer for updates, prepares the pheromone array and agents, and establishes visuals for both agents and pheromones.
- **`on_draw` Method:** Handles drawing events on the canvas, updating agent positions and the pheromone map's visual representation.
- **`on_timer` Method**: Tied to a timer event, this method updates the pheromone array and agent positions, triggering a redraw of the canvas to reflect changes in the simulation state.

### Slider
The `Ui_Slider_logic.py` script integrates interactive elements into the slime mold simulation GUI, specifically focusing on PyQt5 sliders and buttons for dynamic configuration. It features:
We have a class here `SliderLogic` Class:
- **`Constructor (__init__)`:** Initializes the GUI instance and creates sliders for agent speed, a spinbox for agent count, and a restart simulation button. These elements are tied to specific functions in the GUI instance to update the simulation in real time.
- **`create_slider`:** Creates a slider widget for a given parameter (e.g., agent speed), setting its range, default value, and connecting it to a callback function for real-time updates.
- **`create_spinbox`:** Generates a spinbox for numerical input, such as agent count, with specified minimum, maximum, and default values, also linked to a callback function for immediate application in the simulation.
- **`create_slider_widget`**: Assembles the slider and spinbox widgets into a single UI component, organizing them vertically along with the restart button for a cohesive user interface.

## Runtime analysis
The February 2024 Final Version boasts a constant runtime complexity, a stark departure from Version 0's linear increase. Regardless of agent numbers, the Final Version consistently outperforms its predecessor. Despite initial compilation overhead, the NUMBA-optimized Final Version showcases superior performance, underscoring its enhanced efficiency and scalability.
More about that can be read in Issue 68 by now.


## Feedback 
Thank you for your attention so far, now you have gained an understanding of how our program works. We wish you a lot of fun trying out parameters which result in beautiful patterns, you are welcome to send us pictures, short videos of how your settings.  We would be very happy to receive feedback. If you have any suggestions for improvement or criticism, please feel free to contact us. We are looking forward to improve the simulation :)
