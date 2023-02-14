from pyrosim.commonFunctions import Save_Whitespace

class MATERIAL: 

    def __init__(self,color):

        if color == "Cyan":
            rgba = "0 1.0 1.0 1.0"
        elif color == "Green":
            rgba = "0 1.0 0 1.0"
        else:
            print("ERROR: Unknown color: " + color)
            exit()

        self.depth  = 3

        self.string1 = f'<material name="{color}">'

        self.string2 = f'    <color rgba="{rgba}"/>'

        self.string3 = '</material>'

    def Save(self,f):

        Save_Whitespace(self.depth,f)

        f.write( self.string1 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string2 + '\n' )

        Save_Whitespace(self.depth,f)

        f.write( self.string3 + '\n' )
