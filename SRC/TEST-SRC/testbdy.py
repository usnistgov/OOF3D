# -*- python -*-
# $RCSfile: testbdy.py,v $
# $Revision: 1.2.142.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:40 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Boundary-condition tester file.  Does quick, nontrivial equilibrations
# with combinations of boundary conditions to get hopefully-reproducible
# results.

import sys, string, getopt
from oof import * # imports oofcpp and problem.
#from ghostmesh import *

trace_disable()

hexmaterial = newMaterial("2d-elastic",
                       HexagonalElasticity("hex", 1.0, 0.5, 0.0, 0.0, 0.0),
                       Orientation("unrotated", EulerAngle(0,0,0)))

eltypes = getMasterElementList()

# Defaults.
meshsize = 1 
para=0  # Parametricity. 1 == super, 0 == iso, -1 == sub
quad=0  # Quadratitude
upper='fixed'
lower='fixed'

tolerance = 1.e-5
krylov_dim = 10
maxiters = 100

#
# Arguments are: q for quadratic (default is triangular),
# b for subparametric, p for superparametric, and n <size>.
#
# Boundary-condition case uses top edge BC and 
# lower-left-and-lower-right point BC's.
#

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'qbpn:u:l:')
except getopt.error, message:
    print "Usage: python testbdy.py [-q] [-b|-p] [-n <size>] [-u <code>] [-l <code>]"
    print "Recognized codes are: 'fixed', 'float', 'flux' for upper, and"
    print "'fixed', 'float', 'force' for lower."
    print "The upper boundary is an edge, the lower one is points."
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
    elif opt[0] == '-u':
        if opt[1] == 'fixed' or opt[1] == 'float' or opt[1] == 'flux':
            upper = opt[1]
    elif opt[0] == '-l':
        if opt[1] == 'fixed' or opt[1] == 'float' or opt[1] == 'force':
            lower = opt[1]
#
# Options set.
#


if quad:
    print "Quadrilaterals."
    gm = quad_ghost_mesh(hexmaterial, meshsize, meshsize, 1.0, 1.0)
    if para == -1:
        mesh = gm.mesh(quad=eltypes['Subparametric 8-node quadrilateral'])
    elif para == 0:
        mesh = gm.mesh(quad=eltypes['Isoparametric 4-node quadrilateral'])
    elif para == 1:
        mesh = gm.mesh(quad=eltypes['Superparametric 8-node quadrilateral'])
else:
    print "Triangles."
    gm = tri_ghost_mesh(hexmaterial, ghost_mesh.liberal,
                        meshsize, meshsize, 1.0, 1.0)
    if para == -1:
        mesh = gm.mesh(triangle=eltypes['Subparametric 6-node triangle'])
    elif para == 0:
        mesh = gm.mesh(triangle=eltypes['Isoparametric 3-node triangle'])
    elif para == 1:
        mesh = gm.mesh(triangle=eltypes['Superparametric 6-node triangle'])





displacement.set_in_plane(mesh, 1)
mesh.define_field(displacement)
mesh.activate_field(displacement)
mesh.activate_equation(forcebalance_eqn)

try:
    pprofilex = DiscreteProfile({0:-0.1, meshsize:0.1})
    pprofiley = DiscreteProfile({0:0.0, meshsize:0.0})

    fluxprofile = ContinuumProfile('(0.0, -0.1)')

    cprofilex = ContinuumProfile('0.0')
    cprofiley = ContinuumProfile('-0.1')

    fixedx = mesh.newFixedBC(displacement, 0, forcebalance_eqn, 0)
    fixedy = mesh.newFixedBC(displacement, 1, forcebalance_eqn, 1)

    floatx = mesh.newFloatBC(displacement, 0, forcebalance_eqn, 0)
    floaty = mesh.newFloatBC(displacement, 1, forcebalance_eqn, 1)

    flux = mesh.newFluxBC(stress_flux)

    forcex = mesh.newForceBC(forcebalance_eqn, 0)
    forcey = mesh.newForceBC(forcebalance_eqn, 1)

    bottom = mesh.newPointBoundary('bottomcorners')
    for node in mesh.funcnode_iterator():
        if node.index()==0 or node.index()== meshsize:
            bottom.addNode(node.index(), node)

    top = mesh.getBoundary('top')

    if lower=='fixed':
        bottom.addCondition(fixedx, pprofilex)
        bottom.addCondition(fixedy, pprofiley)
    if lower=='float':
        bottom.addCondition(floatx, pprofilex)
        bottom.addCondition(floaty, pprofiley)
    if lower=='force':
        bottom.addCondition(forcex, pprofilex)
        bottom.addCondition(forcey, pprofiley)

    if upper=='fixed':
        top.addCondition(fixedx, cprofilex)
        top.addCondition(fixedy, cprofiley)
    if upper=='float':
        top.addCondition(floatx, cprofilex)
        top.addCondition(floaty, cprofiley)
    if upper=='flux':
        top.addCondition(flux, fluxprofile)

    mesh.equilibrate(maxiters, tolerance, krylov_dim)
    for node in mesh.funcnode_iterator():
        pos = node.position()
        print displacement.value(mesh, node, 0),\
              displacement.value(mesh, node, 1)

except ErrSetupError, s:
    print "Caught ErrSetupError."
    print "Message string: " + s.message()
