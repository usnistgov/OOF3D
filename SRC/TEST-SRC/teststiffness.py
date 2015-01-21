# -*- python -*-
# $RCSfile: teststiffness.py,v $
# $Revision: 1.2.142.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import sys, getopt, string
from oof import *

trace_enable()

try:
    options, args = getopt.getopt(sys.argv[1:], '34o:n:t:')
except getopt.error, message:
    sys.stderr.write(message + '\n')
    sys.exit(1)

quad = 0                                # quadrilateral or triangle?
order = 1                               # linear (1) or quadratic (2)
meshsize = 1
symtol = 0                              # tolerance for symmetry check

for opt in options:
    if opt[0] == '-3':
        quad = 0
    elif opt[0] == '-4':
        quad = 1
    elif opt[0] == '-o':
        order = string.atoi(opt[1])
        if order != 1 and order != 2:
            sys.stderr.write("order must be 1 or 2!\n")
            sys.exit(1)
    elif opt[0] == '-n':
        meshsize = string.atoi(opt[1])
    elif opt[0] == '-t':
        symtol = string.atof(opt[1])


hexmaterial = newMaterial("2d-elastic",
                          HexagonalElasticity("hex", 1.0, 0.5, 0.0, 0.0, 0.0),
                          Orientation("unrotated", EulerAngle(0,0,0)))
  

mesh = Mesh()

mesh.activate_equation(forcebalance_eqn)
#mesh.activate_equation(plane_stress_eqn)

displacement.set_in_plane(mesh,1)
mesh.define_field(displacement)
mesh.activate_field(displacement)
#mesh.activate_field(displacement.out_of_plane())

# It would be easier to use the ghostmesh to create the mesh here, but
# this code predates the ghostmesh class.

# mock up the old Tri3Element constructor, etc
def Tri3Element(mat, nodes):
    eltypes = getMasterElementList()
    el = eltypes['Isoparametric 3-node triangle']
    return el.build(mat, nodes)

def Tri6Element(mat, nodes):
    eltypes = getMasterElementList()
    el = eltypes['Subparametric 6-node triangle']
    return el.build(mat, nodes);

def Quad4Element(mat, nodes):
    eltypes = getMasterElementList()
    el = eltypes['Isoparametric 4-node quadrilateral']
    return el.build(mat, nodes)

def Quad8Element(mat, nodes):
    eltypes = getMasterElementList()
    el = eltypes['Subparametric 8-node quadrilateral']
    return el.build(mat, nodes)
       

if order == 1:
    nodelist = []
    for i in range(0, meshsize+1):
        for j in range(0, meshsize+1):
            nodelist.append(
                mesh.newFuncNode(Coord(j*1.0/meshsize, i*1.0/meshsize)))

    if not quad:
        # Create linear triangular elements
        for i in range(0, meshsize):
            for j in range(0, meshsize):
                ll = nodelist[j   +     i*(meshsize+1)]
                lr = nodelist[j+1 +     i*(meshsize+1)]
                ul = nodelist[j   + (i+1)*(meshsize+1)]
                ur = nodelist[j+1 + (i+1)*(meshsize+1)]
                mesh.AddElement(Tri3Element(hexmaterial, [ll, lr, ul]))
                mesh.AddElement(Tri3Element(hexmaterial, [lr, ur, ul]))

    else:
        # Create linear quadrilateral elements
        for i in range(0, meshsize):
            for j in range(0, meshsize):
                ll = nodelist[j   +     i*(meshsize+1)]
                lr = nodelist[j+1 +     i*(meshsize+1)]
                ul = nodelist[j   + (i+1)*(meshsize+1)]
                ur = nodelist[j+1 + (i+1)*(meshsize+1)]
                mesh.AddElement(Quad4Element(hexmaterial, [ll, lr, ur, ul]))

elif order == 2:
    if not quad:
        # Create quadratic triangular elements
        nodelist = []
        npts = 2*meshsize + 1           # no. of nodes in a row
        # Create nodes
        for i in range(0, npts):
            for j in range(0, npts):
                nodelist.append(mesh.newFuncNode(Coord(j/(2.*meshsize),
                                                        i/(2.*meshsize))))
        try:
            # Create elements
            for i in range(0, meshsize):
                for j in range(0, meshsize):
                    # Nodes in a two-element square
                    #   ul um ur
                    #   *--*--*
                    #   |\    |
                    # ml*  *  * mr
                    #   |   \ |
                    #   *--*--*
                    #   ll lm lr
                    ll = nodelist[2*j   + 2*i*npts] # lower left
                    lm = nodelist[2*j+1 + 2*i*npts] # lower middle
                    lr = nodelist[2*j+2 + 2*i*npts] # lower right
                    ml = nodelist[2*j   + (2*i+1)*npts] # middle left
                    mm = nodelist[2*j+1 + (2*i+1)*npts]	# middle middle
                    mr = nodelist[2*j+2 + (2*i+1)*npts]	# middle right
                    ul = nodelist[2*j   + (2*i+2)*npts] # upper left
                    um = nodelist[2*j+1 + (2*i+2)*npts]	# upper middle
                    ur = nodelist[2*j+2 + (2*i+2)*npts]	# upper right
                    mesh.AddElement(Tri6Element(hexmaterial,
                                                [ll,lm,lr,mm,ul,ml]))
                    mesh.AddElement(Tri6Element(hexmaterial,
                                                [lr,mr,ur,um,ul,mm]))
        except ErrProgrammingError, err:
            print err
            sys.exit()
    else:                               # Quadratic quadrilateral elements
 	#   *--*--*
	#   |     |
	#   *     *
	#   |     |
	#   *--*--*
        nodelist = []
        npts = 2*meshsize + 1 # number of nodes in bottom and top rows
        nmid = meshsize + 1 # number of points in the middle row
        # For each row of elements, create the bottom and middle rows of nodes
        for i in range(0, meshsize):
            for j in range(0, npts):    # bottom row
                nodelist.append(mesh.newFuncNode(Coord(j/(2.*meshsize),
                                                        i*1.0/meshsize)))
            for j in range(0, nmid):    # middle row
                nodelist.append(
                    mesh.newFuncNode(Coord(j*1.0/meshsize, (i+0.5)/meshsize)))
        # Create the nodes on the very top
        for j in range(0, npts):
            nodelist.append(mesh.newFuncNode(Coord(j/(2.*meshsize), 1.0)))
        try:
            # Create elements
            for i in range(0, meshsize): # loop over rows
                ll0 = i*(npts + nmid)   # node no. at ll of first element in row
                ml0 = ll0 + npts        # node no. at ml of first element in row
                ul0 = ml0 + nmid        # node no. at ul of first element in row
                for j in range(0, meshsize):
                    ll = nodelist[ll0 + 2*j]
                    lm = nodelist[ll0 + 2*j + 1]
                    lr = nodelist[ll0 + 2*j + 2]
                    ml = nodelist[ml0 + j]
                    mr = nodelist[ml0 + j + 1]
                    ul = nodelist[ul0 + 2*j]
                    um = nodelist[ul0 + 2*j + 1]
                    ur = nodelist[ul0 + 2*j + 2]
                    mesh.AddElement(Quad8Element(hexmaterial,
                                                 [ll, lm, lr, mr,
                                                  ur, um, ul, ml]))
        except ErrProgrammingError, err:
            print err
            sys.exit()


trace_enable()
mesh.make_stiffness()
stiffness = mesh.stiffness_matrix()

trace_enable()
mesh.mapdofeqs()
Amat = mesh.Amatrix()
print "A is", Amat.nrows(), "x", Amat.ncols()
##print "A is",
##if Amat.symmetric(symtol):
##    print "symmetric"
##else:
##    print "asymmetric"
##Amat.output()
print Amat

