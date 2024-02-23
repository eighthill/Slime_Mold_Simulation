class SlimeConfig:
    """Configuration class for global simulation parameters."""

    # Canvas Dimension
    WIDTH = 1600
    HEIGHT = 900

    # Pheromone behavior parameters
    DECAY = 0.9  # Rate at which pheromones decay over time
    DIFFUSION_COEFFICENT = 0.85  # Rate of pheromone spread

    # Agent behavior parameters
    AGENT_NUMBER = 50000  # Initial number of agents
    SPEED = 1  # Movement speed of agents
    SENSOR_DISTANCE = 8  # Distance of the agents sensors
    ROTATION_SPEED = 0.2  # Rotation speed of agents (max 1 to avoid errors)
    SPAWN_RADIUS = 350  # Radius for initial agent spawning
    SENSOR_ANGLE = 30  # Angle between the forward direction and sensors

    # Simulation update rate
    TIMESTEP = 0.0166  # Currently used for angle rotation, was planned as simulation update rate

    @classmethod
    def set_speed(cls, new_speed):
        """Updates agent movement speed"""
        cls.SPEED = new_speed

    @classmethod
    def set_agent_count(cls, new_agent_count):
        """Updates the number of agents"""
        cls.AGENT_NUMBER = new_agent_count

    @classmethod
    def set_decay(cls, new_decay):
        """Updates the decay rate of pheromones"""
        cls.DECAY = new_decay

    @classmethod
    def set_diff(cls, new_diff):
        """Updates the diffusion coefficient for pheromones"""
        cls.DIFFUSION_COEFFICENT = new_diff

    @classmethod
    def set_sen_dis(cls, new_sen_dis):
        """Updates the sensor distance for agents"""
        cls.SENSOR_DISTANCE = new_sen_dis

    @classmethod
    def set_rota_speed(cls, new_rota_speed):
        """Updates the rotation speed of agents"""
        cls.ROTATION_SPEED = new_rota_speed

    @classmethod
    def set_sen_angle(cls, new_sen_angle):
        """Updates the sensor angle for agents"""
        cls.SENSOR_ANGLE = new_sen_angle

    @classmethod
    def set_time_step(cls, new_time_step):
        """Updates the simulation timestep"""
        cls.TIMESTEP = new_time_step
