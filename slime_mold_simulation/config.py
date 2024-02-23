# This is the Configutaion file with all global parameters


class SlimeConfig:
    # Simulationparameters
    WIDTH = 1280
    HEIGHT = 1080
    DECAY = 0.95
    DIFFUSION_COEFFICENT = 0.95

    # Agentparameters
    AGENT_NUMBER = 45000
    SPEED = 5
    SENSOR_DISTANCE = 15
    ROTATION_SPEED = 0.20  # max. 1 otherwise error!
    SPAWN_RADIUS = 450
    SENSOR_ANGLE = 50
    TIMESTEP = 3.15

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

    @classmethod
    def set_sen_dis(cls, new_sen_dis):
        cls.SENSOR_DISTANCE = new_sen_dis

    @classmethod
    def set_rotta_speed(cls, new_rotta_speed):
        cls.ROTATION_SPEED = new_rotta_speed

    @classmethod
    def set_sen_angle(cls, new_sen_angle):
        cls.SENSOR_ANGLE = new_sen_angle

    @classmethod
    def set_time_step(cls, new_time_setp):
        cls.TIMESTEP = new_time_setp
