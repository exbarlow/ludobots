import src.constants as c
import numpy as np

class LINK:
    def __init__(self,upstreamJoint,name):
        self.upstreamJoint = upstreamJoint
        self.name = name
        self.dims = np.random.uniform(c.minLinkSize,c.maxLinkSize,(3,))
        # if the link is a root link, its position is perfectly resting on the origin
        if self.upstreamJoint == None:
            self.absolutePosition = [0,0,self.dims[2]/2]
            self.relativePosition = self.absolutePosition
        else:
            self.relativePosition = np.add(self.upstreamJoint.position,np.multiply(c.faces[self.upstreamJoint.face],self.dims/2))
            # add the distribution from upstream joint to link
            self.absolutePosition = self.upstreamJoint.parent.absolutePosition + self.relativePosition
            # add the distance from upstream link to upstream joint
            self.absolutePosition += np.multiply(c.faces[self.upstreamJoint.face],self.upstreamJoint.parent.dims/2)

        self.space = [[center - dim/2, center + dim/2] for center, dim in zip(self.absolutePosition,self.dims)]

    def spacesOverlap(self,otherLink):
        def intervalsOverlap(interval1,interval2):
            return interval1[0] <= interval2[1] and interval2[0] <= interval1[1]
        #! temporary -> this will make it so the root never extends into -z, maybe worth changing later to shift all absolute positions above 0
        if self.space[2][0] < 0:
            return False
        return any(intervalsOverlap(selfSpace,otherSpace) for selfSpace, otherSpace in zip(self.space,otherLink.space))

        