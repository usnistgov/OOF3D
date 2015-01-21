# -*- python -*-
# $RCSfile: testthermalexpansion.py,v $
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

import oofpath
import sys, getopt, string
from oof import *  # imports oofcpp and problem.

trace_disable()
# trace_enable()

thermomaterial = newMaterial("test-expansion",
                             ThermalExpansion("test", 0.1, 0.1, 0.0, 6.0),
                             HexagonalElasticity("hex", 1.0, 0.5, 0.0, 0.0, 0.0),
                             IsoHeatConductivity("heatcond", 5.0),
                             Orientation("unrotated", EulerAngle(0,0,0)),
                             ColorProperty("gray",0.5))

# isomaterial = newMaterial("Iso-elastic",
#                           IsoElasticity("test", 0.5, 0.0),
#                           Orientation("unrotated", EulerAngle(0,0,0)))

eltypes = getMasterElementList()

#
# Defaults.
meshsize = 1 
para=0  # Parametricity. 1 == super, 0 == iso, -1 == sub
quad=0  # Quadratitude
psfilename = 0
ghostmeshfilename = 0

# mat = Material("Null")

tolerance = 1.e-8
krylov_dim = 10
maxiters = 1000

#
# Arguments are: q for quadratic (default is triangular),
# b for subparametric, p for superparametric, and n <size>.
#

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'qbpn:f:g:')
except getopt.error, message:
    print "Usage: python testthermalexpansion.py [-q] [-b|-p] [-n <size>] [-f <out.ps>]"
    print "   or: python testthermalexpansion.py -g <ghostmesh.py> [-b|-p] [-f <out.ps>]"
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
        psfilename = opt[1]
    elif opt[0] == '-g':
        ghostmeshfilename = opt[1]
    
if ghostmeshfilename:
    revaluator.restricted.r_execfile(ghostmeshfilename)
    gm = revaluator.restricted.r_eval("gmesh()")  # defined in ghostmeshfile
    if para == -1:
        mesh = gm.mesh(quad=eltypes['Subparametric 8-node quadrilateral'],
                       triangle=eltypes['Subparametric 6-node triangle'])
    elif para == 0:
        mesh = gm.mesh(quad=eltypes['Isoparametric 4-node quadrilateral'],
                       triangle=eltypes['Isoparametric 3-node triangle'])
    elif para == 1:
        mesh = gm.mesh(quad=eltypes['Superparametric 8-node quadrilateral'],
                       triangle=eltypes['Superparametric 6-node triangle'])
elif quad:
    print "Quadrilaterals."
    gm = quad_ghost_mesh(thermomaterial, meshsize, meshsize, 1.0, 1.0)
    if para == -1:
        mesh = gm.mesh(quad=eltypes['Subparametric 8-node quadrilateral'])
    elif para == 0:
        mesh = gm.mesh(quad=eltypes['Isoparametric 4-node quadrilateral'])
    elif para == 1:
        mesh = gm.mesh(quad=eltypes['Superparametric 8-node quadrilateral'])
else:
    print "Triangles."
    gm = tri_ghost_mesh(thermomaterial, ghost_mesh.liberal,
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
temperature.set_in_plane(mesh, 1)

mesh.define_field(temperature)
mesh.define_field(displacement)
# mesh.define_field(temperature)

trace_disable()

try:

    mesh.activate_field(displacement)
    # mesh.activate_field(temperature)

    mesh.activate_equation(heat_eqn)
    # mesh.activate_equation(forcebalance_eqn)
    
    mesh.activate_field(temperature)
    # mesh.activate_field(displacement)

    mesh.activate_equation(forcebalance_eqn)
    # mesh.activate_equation(heat_eqn)


    # Simple thermal boundary conditions.
    lefttemp = ContinuumProfile('5.0')
    righttemp = ContinuumProfile('5.0')

    fixedtemp = mesh.newFixedBC(temperature, 0, heat_eqn, 0)

    left = mesh.getBoundary('left')
    left.addCondition(fixedtemp, lefttemp)

    right = mesh.getBoundary('right')
    right.addCondition(fixedtemp, righttemp)
    
    print "BC's defined."
    # trace_enable()

    # Finished with temp, now do mechanical part.

    topflux   = ContinuumProfile('(0.0, 0.1)')
    bottomfix = ContinuumProfile('0.0')
    pointfix = DiscreteProfile({0:0.0})

    floatdispx = mesh.newFloatBC(displacement, 0, forcebalance_eqn, 0)
    fixeddispy = mesh.newFixedBC(displacement, 1, forcebalance_eqn, 1)
    fixeddispx = mesh.newFixedBC(displacement, 0, forcebalance_eqn, 0)
    flux       = mesh.newFluxBC(stress_flux)
    
    bottom = mesh.getBoundary('bottom')
    bottom.addCondition(fixeddispy, bottomfix)

    bottomleft = mesh.getBoundary('bottomleft')
    bottomleft.addCondition(fixeddispx, pointfix)
    
    # top = mesh.getBoundary('top')
    # top.addCondition(flux, topflux)

    # temperature.init(mesh, lambda:1.0) 
    
    # for node in mesh.funcnode_iterator():
    #     temperature.setvalue(mesh, node, 0, 1.0)

    
    mesh.equilibrate(maxiters, tolerance, krylov_dim)

    if psfilename:
        deformOutput = outputClones.VectorFieldOutput.clone()
        deformOutput.plugParameter(displacement,"field")
        positionSum = outputClones.VFieldSumOutput.clone()
        positionSum.plugInput(deformOutput)
        positionSum.plugInput(outputClones.posOutput)

        thermalOutput = output.outputTypes['scalar field'].clone()
        thermalOutput.plugParameter(temperature, "field")
        rscl = outputClones.RescaleOutput.clone()
        rscl.plugInput(thermalOutput)
        rscl.plugParameter(0.0, "minimum")
        rscl.plugParameter(0.95, "maximum")


        import drawmesh
        import psoutput
        import color
        psdriver = psoutput.PSoutput(psfilename)
        psdriver.set_colormap(color.SpectralMap())
        drawmesh.draw_mesh(mesh, psdriver,
                           [positionSum, outputClones.posOutput],
                           valueOutput=rscl,
                           drawedges=0)
##        psgfx.psoutput(mesh, psfilename, psgfx.PSgeometry(),
##                       [positionSum,outputClones.posOutput],
##                       valueOutput=colormap,
##                       drawedges=1)

    else:
        for node in mesh.funcnode_iterator():
            pos = node.position()
            print displacement.value(mesh, node, 0), \
                  displacement.value(mesh, node, 1), \
                  temperature.value(mesh, node, 0)
    
except ErrSetupError, s:
    print "Caught ErrSetupError."
    print "Message string: " + s.message()
    
