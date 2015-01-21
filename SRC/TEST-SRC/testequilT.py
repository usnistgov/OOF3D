# -*- python -*-
# $RCSfile: testequilT.py,v $
# $Revision: 1.2.142.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:41 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import sys, getopt, string
from oofcpp import *
from problem import *
from ghostmesh import *

trace_disable()

##hexmaterial = newMaterial("2d-elastic",
##                       HexagonalElasticity("hex", 1.0, 0.5, 0.0, 0.0, 0.0),
##                       Orientation("unrotated", EulerAngle(0,0,0)))

thermmaterial = newMaterial("thermal",
                            IsoHeatConductivity("heatcond", 1.0),
                            Orientation("unrotated", EulerAngle(0,0,0)))
  
eltypes = getMasterElementList()

#
# Defaults.
meshsize = 1 
para=0  # Parametricity. 1 == super, 0 == iso, -1 == sub
quad=0  # Quadratitude

tolerance = 1.e-5
krylov_dim = 10
# maxiters = 100

#
# Arguments are: q for quadratic (default is triangular),
# b for subparametric, p for superparametric, and n <size>.
#

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'qbpn:t:k:N:')
except getopt.error, message:
    print "Usage: python testbdy.py [-q] [-b|-p] [-n <size>]"
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
    elif opt[0] == '-t':
        tolerance = string.atof(opt[1])
    elif opt[0] == '-k':
        krylov_dim = string.atoi(opt[1])
    elif opt[0] == '-N':
        maxiters = string.atoi(opt[1])
    

if quad:
    gm = quad_ghost_mesh(thermmaterial, meshsize, meshsize, 1.0, 1.0)
    if para == -1:
        mesh = gm.mesh(quad=eltypes['Subparametric 8-node quadrilateral'])
    elif para == 0:
        mesh = gm.mesh(quad=eltypes['Isoparametric 4-node quadrilateral'])
    elif para == 1:
        mesh = gm.mesh(quad=eltypes['Superparametric 8-node quadrilateral'])
else:
    gm = tri_ghost_mesh(thermmaterial, ghost_mesh.liberal,
                        meshsize, meshsize, 1.0, 1.0)
    if para == -1:
        mesh = gm.mesh(triangle=eltypes['Subparametric 6-node triangle'])
    elif para == 0:
        mesh = gm.mesh(triangle=eltypes['Isoparametric 3-node triangle'])
    elif para == 1:
        mesh = gm.mesh(triangle=eltypes['Superparametric 6-node triangle'])


temperature.set_in_plane(mesh, 1)
mesh.define_field(temperature)
mesh.activate_field(temperature)
mesh.activate_equation(heat_eqn)
mesh.newFixedBC(temperature, 0, heat_eqn, 0,
                '0.0', mesh.getBoundary('bottom'))
mesh.newFixedBC(temperature, 0, heat_eqn, 0,
                '0.1', mesh.getBoundary('top'))

# mesh.newFluxBC( heat_flux, '0.1', mesh.getBoundary('top'))

print "Equilibrating."
mesh.equilibrate(tolerance=1.e-8)

for node in mesh.funcnode_iterator():
    print node.position(), temperature.value(mesh, node, 0), heat_eqn.nodaleqn(mesh, node, 0).value()

