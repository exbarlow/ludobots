import src.constants as c 
import numpy as np

class JOINT:
    def __init__(self,parent,face=None):
        self.parent = parent
        #! temp: always revolute for now -> can play with this to see how behavior changes
        self.type = "revolute"
        # the face of the parent to which the child connects, {0: +x, 1: -x, 2: +y, 3: -y, 4: +z, 5: -z}
        self.face = face
        self.upstreamJoint = self.parent.upstreamJoint
        
        if self.upstreamJoint == None:
            displacementVector = self.getDisplacementVector(relative=False)
            self.position = self.parent.absolutePosition + np.multiply(displacementVector,self.parent.dims/2)
        else:
            displacementVector = self.getDisplacementVector()
            self.position = np.multiply(displacementVector,self.parent.dims/2)

        
        self.axis = c.axesToString[np.random.choice(c.faceToPossibleAxes[self.face])]
        
    
    def getDisplacementVector(self,relative=True):
        faceUnitVector = c.faces[self.face]

        # if the joint is a root joint, return the unit vector of the face
        if not relative:
            return faceUnitVector

        upstreamUnitVector = c.faces[self.upstreamJoint.face]
        # find and return the displacement vector between the joint and its upstreamJoint
        return np.add(faceUnitVector,upstreamUnitVector)

    def addChild(self,child):
        self.child = child
        self.name = f"{self.parent.name}_{self.child.name}"

        