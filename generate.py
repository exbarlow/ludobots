import pyrosim.pyrosim as pyrosim
pyrosim.Start_SDF("boxes.sdf")

length = 1
width = 1
height = 1
x = 0
y = 0
z = 0.5

for k in range(10):
    for i in range(5):
        for j in range(5):
            pyrosim.Send_Cube(name=f"Box{25*k+5*i+j}",pos=[x+j,y+i,z+k],size=[length*pow(0.9,k),width*pow(0.9,k),height*pow(0.9,k)])
            print(f"Box{25*k+5*i+j}")

pyrosim.End()