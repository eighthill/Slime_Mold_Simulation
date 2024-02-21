# This is the Configutaion file with all global parameters


class SlimeConfig:
    # Simulationparameters
    WIDTH = 1000
    HEIGHT = 1000
    DECAY = 0.97
    DIFFUSION_COEFFICENT = 0.75

    # Agentparameters
    AGENT_NUMBER = 10000
    SPEED = 1
    SENSOR_DISTANCE = 8
    ROTATION_SPEED = 0.2  # max. 1 otherwise error!
    SPAWN_RADIUS = 350
    SENSOR_ANGLE = 25
    TIMESTEP = 0.0166

    @classmethod
    def set_speed(cls, new_speed):
        cls.SPEED = new_speed

    @classmethod
    def set_agent_count(cls, new_agent_count):
        cls.AGENT_NUMBER = new_agent_count

    @classmethod
    def set_decay(cls, new_decay):
        cls.DECAY = new_decay
        
    @classmethod
    def set_diff(cls, new_diff):
        cls.DIFFUSION_COEFFICENT = new_diff  