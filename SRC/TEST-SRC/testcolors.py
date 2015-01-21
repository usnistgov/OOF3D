# -*- python -*-
# $RCSfile: testcolors.py,v $
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

import oofpath
import sys, getopt, string
from oof import *  # imports oofcpp and problem.

trace_disable()
# trace_enable()

thermomaterial = newMaterial("workshop-demo",
                             ThermoElasticity("soft-shear",
                                              1.0, 0.0, 150.0, -0.01),
                             IsoHeatConductivity("heatcond", 1.0),
                             Orientation("unrotated", EulerAngle(0,0,0)),
                             ColorProperty("gray",0.5))

isomaterial = newMaterial("Iso-elastic",
                          IsoElasticity("test", 0.5, 0.0),
                          Orientation("unrotated", EulerAngle(0,0,0)))

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
maxiters = 10000

#
# Arguments are: q for quadratic (default is triangular),
# b for subparametric, p for superparametric, and n <size>.
#

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'qbpn:f:g:')
except getopt.error, message:
    print "Usage: python testthermoelastic.py [-q] [-b|-p] [-n <size>] [-f <out.ps>]"
    print "   or: python testthermoelastic.py -g <ghostmesh.py> [-b|-p] [-f <out.ps>]"
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
    gm = quad_ghost_mesh(thermomaterial, 2, meshsize, 1.0, 1.0)
    if para == -1:
        mesh = gm.mesh(quad=eltypes['Subparametric 8-node quadrilateral'])
    elif para == 0:
        mesh = gm.mesh(quad=eltypes['Isoparametric 4-node quadrilateral'])
    elif para == 1:
        mesh = gm.mesh(quad=eltypes['Superparametric 8-node quadrilateral'])
else:
    print "Triangles."
    gm = tri_ghost_mesh(thermomaterial, ghost_mesh.liberal,
                        2, meshsize, 1.0, 1.0)
    print "ghost mesh constructed"
    if para == -1:
        mesh = gm.mesh(triangle=eltypes['Subparametric 6-node triangle'])
    elif para == 0:
        mesh = gm.mesh(triangle=eltypes['Isoparametric 3-node triangle'])
    elif para == 1:
        mesh = gm.mesh(triangle=eltypes['Superparametric 6-node triangle'])

print "mesh constructed"

temperature.set_in_plane(mesh, 1)

mesh.define_field(temperature)

trace_disable()

try:

    # Simple thermal boundary conditions.
    lefttemp = ContinuumProfile('0.0')
    righttemp = ContinuumProfile('140.0')

    fixedtemp = mesh.newFixedBC(temperature, 0, heat_eqn, 0)

    left = mesh.getBoundary('left')
    left.addCondition(fixedtemp, lefttemp)

    right = mesh.getBoundary('right')
    right.addCondition(fixedtemp, righttemp)
    
    print "BC's defined."
    # trace_enable()

    mesh.activate_field(temperature)
    mesh.activate_equation(heat_eqn)

    mesh.equilibrate(maxiters, tolerance, krylov_dim)

    if psfilename:
        thermalOutput = output.outputTypes['scalar field'].clone()
        thermalOutput.plugParameter(temperature, "field")
        rscl = outputClones.RescaleOutput.clone()
        rscl.plugInput(thermalOutput)
        rscl.plugParameter(0.0, "minimum")
        rscl.plugParameter(1.0, "maximum")

        import psoutput
        import display
        import displaymethods
        import color
        psdriver = psoutput.PSoutput(psfilename)

        display = display.Display()
        fill = display.add_method(
            displaymethods.CenterFillDisplay(outputClones.posOutput, rscl))
        fill.set_param('colormap', color.SpectralMap(saturation=0.9))
        display.draw(mesh, psdriver)

    
except ErrSetupError, s:
    print "Caught ErrSetupError."
    print "Message string: " + s.message()
    
