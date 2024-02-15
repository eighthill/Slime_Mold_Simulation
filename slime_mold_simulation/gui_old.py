import numpy as np
from vispy import app, scene, gloo
from vispy.color import Color
from simulation_old import Agent, PheromoneArray
#import moderngl

class SlimeConfig:
    diffusion_speed = 10.0
    evaporation_speed = 5.0

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

        self.pheromone = PheromoneArray()
        self.agents = Agent(self.pheromone)

        # Set up a timer for periodic updates
        self.timer = app.Timer(connect=self.on_timer, start=True)

        # Create a black background
        self.view = scene.SceneCanvas(keys="interactive", size=(1500, 1500), show=True)
        self.view.bgcolor = Color("black")

        # Create yellow points visual
        self.points = scene.visuals.Markers()
        self.view.scene._add_child(self.points)

        # Vertex and fragment shaders
        # Vertex shader
        vertex_shader = """
        #version 120
        attribute vec2 a_position;
        varying vec4 v_color;

        uniform vec4 u_color;  // Declare u_color as a uniform variable

        void main() {
            gl_Position = vec4(a_position, 0.0, 1.0);
            v_color = u_color;  // Pass the uniform value to the varying variable
        }
        """

        # Fragment shader
        fragment_shader = """
        #version 120
        varying vec4 v_color;  // Declare v_color as a varying variable

        void main() {
            gl_FragColor = v_color;
        }
        """

        blur_shader = """
        #version 450

        // reduce fermones and blur fermones

        layout (local_size_x = 16, local_size_y = 16) in;

        layout(r8, location=0) restrict readonly uniform image2D fromTex;
        layout(r8, location=1) uniform image2D destTex;

        float fetchValue(ivec2 co) {
            return imageLoad(fromTex, co).r;
        }

        float blured(ivec2 co) {
            float sum = 
                fetchValue(co) +
                fetchValue(co + ivec2(-1, -1)) +
                fetchValue(co + ivec2( 0, -1)) +
                fetchValue(co + ivec2( 1, -1)) +
                fetchValue(co + ivec2( 1,  0)) +
                fetchValue(co + ivec2( 1,  1)) +
                fetchValue(co + ivec2( 0,  1)) +
                fetchValue(co + ivec2(-1,  1)) +
                fetchValue(co + ivec2(-1,  0));
            
            return sum / 9.;
        }

        // uniform float dt;
        uniform float diffuseSpeed;
        uniform float evaporateSpeed;

        #define dt 0.0166

        void main() {
            ivec2 texelPos = ivec2(gl_GlobalInvocationID.xy);
            float original_value = imageLoad(fromTex, texelPos).r;
            float v = blured(texelPos);
            
            float diffused = mix(original_value, v, diffuseSpeed * dt);
            float evaporated = max(0, diffused - evaporateSpeed * dt);

            imageStore(destTex, texelPos, vec4(evaporated));
        }

        
        """

        # Compile shaders
        self.program = gloo.Program(vert=vertex_shader, frag=fragment_shader)

        # Create a buffer for blurring
        self.blur_buffer = np.zeros(1000 * 1000, dtype=np.float32)
        self.blur_texture = gloo.Texture2D(shape=(1000, 1000), format='red')

        # Set uniform variable for color
        self.program["u_color"] = (1.0, 1.0, 0.0, 1.0)  # Yellow color

        # Compile shaders for the blur program
        ctx = moderngl.create_context()
        self.blur_program = ctx.compute_shader(blur_shader)

        # Set initial points
        self.update_points([])

    def update_points(self, points):
        """
        Update the positions of agents.
        """
        # Convert points to a numpy array
        points_array = np.array(points, dtype=np.float32)

        # Reshape points array if necessary
        if points_array.ndim == 1:
            points_array = points_array.reshape(-1, 2)

        self.points.set_data(points_array, face_color=(1.0, 1.0, 0.0, 1.0))  # Yellow color

    def on_timer(self, event):
        """
        Event handler for the timer.

        Updates the positions of agents periodically.
        """
        # Decay pheromones
        # self.pheromone.decay_pheromones()

        # Update the pheromone array based on agent positions
        self.pheromone.update_pheromone(self.agents.Agents_list)

        # Update the agent movements
        self.agents.make_move(self.pheromone)

        # Render with the main program
        new_points = [(agent["float_x_pos"], agent["float_y_pos"]) for agent in self.agents.Agents_list]
        self.update_points(new_points)
        self.view.update()

        # Use the main framebuffer and texture for blurring
        self.blur_program['fromTex'].write(self.pheromone.pheromone_value.flatten().astype(np.float32))
        self.blur_program['destTex'].write(self.blur_buffer)
        self.blur_program['diffuseSpeed'] = SlimeConfig.diffusion_speed
        self.blur_program['evaporateSpeed'] = SlimeConfig.evaporation_speed
        self.blur_program.run(1000 // 16, 1000 // 16, 1)

        # Update the Vispy scene to reflect the changes
        self.update_points(new_points)
        self.view.update()

if __name__ == "__main__":
    # Main Program
    gui = SimulationGUI()
    app.run()
    