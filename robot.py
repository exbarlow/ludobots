from sensor import SENSOR
from motor import MOTOR
import pybullet as p

class ROBOT:
    def __init__(self):
        self.sensors = {}
        self.motors = {}
        self.robotId = p.loadURDF("body.urdf")