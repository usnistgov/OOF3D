# -*- python -*-
# $RCSfile: testbcs.py,v $
# $Revision: 1.4.142.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:39 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import oofpath
import sys, getopt, string
# import oof 
from oof import *  # imports oofcpp and problem.
##from boundary import *
##from ghostmesh import *

import outputClones
import output
# import psgfx
# import meshGUI

trace_disable()
# trace_enable()

hexmaterial = newMaterial("2d-elastic",
                          HexagonalElasticity("hex", 1.0, 0.5, 0.0, 0.0, 0.0),
                          Orientation("unrotated", EulerAngle(0,0,0)))
  
eltypes = getMasterElementList()

#
# Defaults.
meshsize = 1 
para=0  # Parametricity. 1 == super, 0 == iso, -1 == sub
quad=0  # Quadratitude
outfile = None

# mat = Material("Null")

tolerance = 1.e-5
krylov_dim = 10
maxiters = 300

#
# Arguments are: q for quadratic (default is triangular),
# b for subparametric, p for superparametric, and n <size>.
#

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'qbpn:f:')
except getopt.error, message:
    print "Usage: python testbcs.py [-q] [-b|-p] [-n <size>] [-f <out.ps>]"
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
        outfile = opt[1]
    

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
    print "ghost mesh constructed"
    if para == -1:
        mesh = gm.mesh(triangle=eltypes['Subparametric 6-node triangle'])
    elif para == 0:
        mesh = gm.mesh(triangle=eltypes['Isoparametric 3-node triangle'])
    elif para == 1:
        mesh = gm.mesh(triangle=eltypes['Superparametric 6-node triangle'])

print "mesh constructed"

displacement.set_in_plane(mesh, 1)
mesh.define_field(displacement)
mesh.activate_field(displacement)
mesh.activate_equation(forcebalance_eqn)


# trace_disable()

try:
    # Simple mechanical boundary conditions.
    fluxprof   = ContinuumProfile('(0.0, -0.1666666666)')
    fixedprof = ContinuumProfile('0.0')

    llfixedprof = DiscreteProfile({0: 0.0})
    lrfixedprof = DiscreteProfile({meshsize: 0.0})

    fixeddispx = mesh.newFixedBC(displacement, 0, forcebalance_eqn, 0)
    fixeddispy = mesh.newFixedBC(displacement, 1, forcebalance_eqn, 1)
    flux       = mesh.newFluxBC(stress_flux)
    floatdispy = mesh.newFloatBC(displacement, 1, forcebalance_eqn, 1)
    
    # left = mesh.getBoundary('left')
    # left.addCondition(flux, fluxprof)
    # left.addCondition(fixeddispy, fixedprof)

    # right = mesh.getBoundary('right')
    # right.addCondition(flux, fluxprof)
    # right.addCondition(fixeddispy, fixedprof)

    bottom = mesh.getBoundary('bottom')
    bottom.addCondition(fixeddispx, fixedprof)
    bottom.addCondition(fixeddispy, fixedprof)

    top = mesh.getBoundary('top')
    top.addCondition(fixeddispx, fixedprof)
    top.addCondition(floatdispy, fixedprof)
    top.addCondition(flux, fluxprof)

    print "BC's defined."
    # trace_enable()


    mesh.equilibrate(maxiters, tolerance, krylov_dim)

    if outfile:
        import display
        display = display.Display()

        import color
        import displaymethods

        edgedisp = display.add_method(
            displaymethods.EdgeDisplay(outputClones.posOutput))
        edgedisp.set_param('width',0.001)
        edgedisp.set_param('color',color.Gray(0.5))

        import psoutput
        device = psoutput.PSoutput(outfile)

        display.draw(mesh,device)
        
##        import psgfx
##        deformOutput = outputClones.VectorFieldOutput.clone()
##        deformOutput.plugParameter(displacement,"field")
##        positionSum = outputClones.VFieldSumOutput.clone()
##        positionSum.plugInput(deformOutput)
##        positionSum.plugInput(meshGUI.posOutput)

##        psgfx.psoutput(mesh, outfile, psgfx.PSgeometry(),
##                       [positionSum, meshGUI.posOutput])
        
    else:
        for node in mesh.funcnode_iterator():
            pos = node.position()
            print displacement.value(mesh, node, 0),\
                  displacement.value(mesh, node, 1)
        
except ErrSetupError, s:
    print "Caught ErrSetupError."
    print "Message string: " + s.message()
    
