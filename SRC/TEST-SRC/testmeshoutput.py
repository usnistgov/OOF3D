# -*- python -*-
# $RCSfile: testmeshoutput.py,v $
# $Revision: 1.2.142.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:42 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import sys, getopt, string
from oof import *  # imports oofcpp and problem.
#from ghostmesh import *


trace_disable()

hexmaterial = newMaterial("2d-elastic",
                          HexagonalElasticity("hex", 1.0, 0.5, 0.0, 0.0, 0.0),
                          Orientation("unrotated", EulerAngle(0,0,0)))
  
eltypes = getMasterElementList()

#
# Defaults.
meshsize = 1 
para=0  # Parametricity. 1 == super, 0 == iso, -1 == sub
quad=0  # Quadratitude
file = sys.stdout

#
# Arguments are: q for quadratic (default is triangular),
# b for subparametric, p for superparametric, and n <size>.
#

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'qbpn:f:')
except getopt.error, message:
    print "Usage: python testbdy.py [-q] [-b|-p] [-n <size>] [-f file]"
    sys.exit(1)

for opt in optlist:
    if opt[0] == '-q':
        quad=1
    elif opt[0] == '-b':
        para = para - 1
    elif opt[0] == '-p':
        para = para + 1
    elif opt[0] == '-n':
        meshsize = string.atoi(opt[1])
    elif opt[0] == '-f':
        file = open(opt[1], 'w')
    

if quad:
    gm = quad_ghost_mesh(hexmaterial, meshsize, meshsize, 1.0, 1.0)
    if para == -1:
        mesh = gm.mesh(quad=eltypes['Subparametric 8-node quadrilateral'])
    elif para == 0:
        mesh = gm.mesh(quad=eltypes['Isoparametric 4-node quadrilateral'])
    elif para == 1:
        mesh = gm.mesh(quad=eltypes['Superparametric 8-node quadrilateral'])
else:
    gm = tri_ghost_mesh(hexmaterial, ghost_mesh.liberal,
                        meshsize, meshsize, 1.0, 1.0)
    if para == -1:
        mesh = gm.mesh(triangle=eltypes['Subparametric 6-node triangle'])
    elif para == 0:
        mesh = gm.mesh(triangle=eltypes['Isoparametric 3-node triangle'])
    elif para == 1:
        mesh = gm.mesh(triangle=eltypes['Superparametric 6-node triangle'])


mesh.define_field(displacement)
mesh.define_field(temperature)
#trace_enable()

#mlib = material_output(file)
mesh.output(file)
