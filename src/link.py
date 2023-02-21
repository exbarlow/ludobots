import src.constants as c
import numpy as np

class LINK:
    def __init__(self,upstreamJoint,name):
        self.upstreamJoint = upstreamJoint
        self.name = name
        self.dims = np.random.uniform(c.minLinkSize,c.maxLinkSize,(3,))
        self.connectedFaces = set()
        # if the link is a root link, its position is perfectly resting on the origin
        if self.upstreamJoint == None:
            self.absolutePosition = [0,0,self.dims[2]/2 + 0.001]
            self.relativePosition = self.absolutePosition
        else:
            self.addConnectedFace(c.inverseFaces[self.upstreamJoint.face])
            self.relativePosition = np.multiply(c.faces[self.upstreamJoint.face],self.dims/2)
            # add the distribution from upstream joint to link
            if self.upstreamJoint.upstreamJoint == None:
                self.absolutePosition = self.upstreamJoint.position + self.relativePosition
            else:
                self.absolutePosition = self.upstreamJoint.position + self.relativePosition + self.upstreamJoint.parent.absolutePosition
            


        self.space = [[center - dim/2, center + dim/2] for center, dim in zip(self.absolutePosition,self.dims)]
        #! DEBUG
        # print("link name",self.name,"space",self.space)

    def addConnectedFace(self,face):
        assert(face not in self.connectedFaces)
        self.connectedFaces.add(face)

    def spacesOverlap(self,otherLink,tolerance=0.001):
        if self.space[2][0] < tolerance:
            return True
        for i in range(3):
            overlap = min(self.space[i][1], otherLink.space[i][1]) - max(self.space[i][0], otherLink.space[i][0])
            if overlap < tolerance:
                return False

        return True
        


        