from oofcpp import *
from problem import *

mesh = Mesh()
# count = 0
# for i in range(4):
#     for j in range(4):
#         count = count+1
#         mesh.AddNode(Node(count,Coord(i,j)))

# print mesh.getNodes()

# def setting(c1,c2,i):
#     print c1," ",c2
#     return c1*c2


node0 = Node(0, Coord(0,0))
mesh.AddNode(node0)
mesh.define_field(temperature)
print temperature.value(mesh, node0, 0)
