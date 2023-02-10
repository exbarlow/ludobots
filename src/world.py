import pybullet as p
import pybullet_data

class WORLD:
    def __init__(self):
        self.planeId = p.loadURDF("plane.urdf")
        p.loadSDF("src/robotfiles/world.sdf")