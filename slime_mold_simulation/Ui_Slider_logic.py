from PyQt5.QtWidgets import QLabel, QPushButton, QSlider, QSpinBox, QVBoxLayout, QWidget, QDoubleSpinBox

from config import SlimeConfig


class SliderLogic:
    def __init__(self, gui_instance):
        self.gui = gui_instance

        # Create sliders for agent-related parameters
        # self.agent_size_slider, self.agent_size_widget = self.create_slider(5, 30, 15, self.gui.update_agent_size, "Agent Size")
        self.agent_count_spinbox = self.create_spinbox_int(1, 1000000, SlimeConfig.AGENT_NUMBER, self.gui.update_agent_count)
        self.agent_speed_spinbox = self.create_spinbox_int(1, 10, SlimeConfig.SPEED, self.gui.update_agent_speed)
        self.sen_dis_spinbox = self.create_spinbox_int(1, 50, SlimeConfig.SENSOR_DISTANCE, self.gui.update_sen_dis)
        self.sen_angle_spinbox = self.create_spinbox_int(1, 75, SlimeConfig.SENSOR_ANGLE, self.gui.update_sen_angle)
        self.decay_spinbox = self.create_spinbox_float(0.1, 1.0, SlimeConfig.DECAY, self.gui.update_decay)
        self.diff_spinbox = self.create_spinbox_float(0.1, 1.0, SlimeConfig.DIFFUSION_COEFFICENT, self.gui.update_diff)
        self.rotta_speed_spinbox = self.create_spinbox_float(0.1, 1.0, SlimeConfig.ROTATION_SPEED, self.gui.update_rotta_speed)
        
        # Create sliders for simulation parameters
        # self.fading_slider, self.fading_widget = self.create_slider(1, 100, 1, self.gui.update_fading, "Fading")
        # self.diffusion_coefficient_slider, self.diffusion_coefficient_widget = self.create_slider(1, 100, 1, self.gui.update_diffusion_coefficient, "Diffusion Coefficient")
        # self.pheromone_value_slider, self.pheromone_value_widget = self.create_slider(1, 100, 1, self.gui.update_pheromone_value, "Pheromone Value")

        # Create a button to restart the simulation
        self.restart_button = QPushButton("Restart Simulation")
        self.restart_button.clicked.connect(self.gui.restart_simulation)

        # Create a widget for all the sliders and the restart button
        self.slider_widget = self.create_slider_widget()

    def create_slider(self, min_value, max_value, default_value, callback, label_text):
        slider = QSlider()
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(default_value)
        slider.setOrientation(1)  # Vertical orientation
        slider.valueChanged.connect(callback)

        label = QLabel(label_text)
        value_label = QLabel(str(default_value))  # Initially display default value

        # Add the label to the layout
        layout = QVBoxLayout()
        layout.addWidget(label)
        layout.addWidget(slider)
        layout.addWidget(value_label)

        # Set the layout for the widget
        widget = QWidget()
        widget.setLayout(layout)

        # Expose the value_label as an attribute for updating
        slider.value_label = value_label

        return slider, widget

    def create_spinbox_int(self, min_value, max_value, default_value, callback):
        spinbox = QSpinBox()
        spinbox.setMinimum(min_value)
        spinbox.setMaximum(max_value)
        spinbox.setValue(default_value)
        spinbox.setSingleStep(1)
        spinbox.valueChanged.connect(callback)
        return spinbox
    
    def create_spinbox_float(self, min_value, max_value, default_value, callback):
        spinbox = QDoubleSpinBox()
        spinbox.setMinimum(min_value)
        spinbox.setMaximum(max_value)
        spinbox.setValue(default_value)
        spinbox.setSingleStep(0.1)
        spinbox.valueChanged.connect(callback)
        return spinbox

    def create_slider_widget(self):
        widget = QWidget()
        layout = QVBoxLayout(widget)
        # layout.addWidget(QLabel("Agent Size"))
        # layout.addWidget(self.agent_size_slider)
        layout.addWidget(QLabel("Agent Speed"))
        layout.addWidget(self.agent_speed_spinbox)
        layout.addWidget(QLabel("Agent Count"))
        layout.addWidget(self.agent_count_spinbox)
        layout.addWidget(QLabel("Decay"))
        layout.addWidget(self.decay_spinbox)
        layout.addWidget(QLabel("Diffusion Coefficient"))
        layout.addWidget(self.diff_spinbox)
        layout.addWidget(QLabel("Sensor Distance"))
        layout.addWidget(self.sen_dis_spinbox)
        layout.addWidget(QLabel("Rotation Speed"))
        layout.addWidget(self.rotta_speed_spinbox)
        layout.addWidget(QLabel("Sensor Angle"))
        layout.addWidget(self.sen_angle_spinbox)
        layout.addWidget(self.restart_button)
        widget.setLayout(layout)
        widget.setMinimumSize(200,100)
        return widget
