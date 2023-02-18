import src.pyrosim.pyrosim as pyrosim

def Create_World():
    """
    Creates a world for the simulation. Currently, this is just a blank world.

    @return: None
    """
    pyrosim.Start_SDF("src/robotfiles/world.sdf")
    pyrosim.End()