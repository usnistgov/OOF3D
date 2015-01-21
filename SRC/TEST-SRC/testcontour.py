# -*- python -*-
# $RCSfile: testcontour.py,v $
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
from math import *

trace_disable()
# trace_enable()

thermomaterial = newMaterial("workshop-demo",
                             ThermoElasticity("soft-shear",
                                              1.0, 0.0, 150.0, -0.01),
                             IsoHeatConductivity("heatcond", 1.0),
                             Orientation("unrotated", EulerAngle(0,0,0)),
                             ColorProperty("gray",0.5))


eltypes = getMasterElementList()

#
# Defaults.
meshsize = 1 
para=0  # Parametricity. 1 == super, 0 == iso, -1 == sub
quad=0  # Quadratitude
psfilename = None
ghostmeshfilename = 0

# mat = Material("Null")

tolerance = 1.e-8
krylov_dim = 10
maxiters = 10000

contourbins = 5
nlevels = 5

profilefile = None

def testfun(x,y, *spots):
    for spot in spots:
        if (x-spot[0])*(x-spot[0]) + (y-spot[1])*(y-spot[1]) < spot[2]*spot[2]:
            return (spot[0]-0.25)*(spot[1]-0.25)
    return (x-0.25)*(y-0.25)


#
# Arguments are: q for quadratic (default is triangular),
# b for subparametric, p for superparametric, and n <size>.
#

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'qbpn:o:g:N:l:L:f:P:')
except getopt.error, message:
    print message
    print "Usage: python testcontour.py [-q] [-b|-p] [-n <size>] [-N <contour bins>] [-o <out.ps>] [-l <nlevels>] [-L '[level list]'] [-f <function>] [-P <profile file>]"
    print "   or: python testcontour.py -g <ghostmesh.py> [-b|-p] [-o <out.ps>] [-N <contour bins>] [-l <nlevels>] [-L '[level list]'] [-f <function>] [-P <profile file>]"
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
    elif opt[0] == '-o':
        psfilename = opt[1]
    elif opt[0] == '-g':
        ghostmeshfilename = opt[1]
    elif opt[0] == '-N':
        contourbins = string.atoi(opt[1])
    elif opt[0] == '-l':
        nlevels = string.atoi(opt[1])
    elif opt[0] == '-L':
        nlevels = eval(opt[1])
    elif opt[0] == '-f':
        function = eval('lambda x,y:' + opt[1])
    elif opt[0] == '-P':
        profilefile = opt[1]
    
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
    gm = tri_ghost_mesh(thermomaterial, ghost_mesh.moderate,
                        meshsize, meshsize, 1.0, 1.0)
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
    righttemp = ContinuumProfile('140.0*(1+5*y*(1-y))')

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
        # Get the temperature Field
        thermalOutput = outputClones.ScalarFieldOutput.clone()
        thermalOutput.plugParameter(temperature, "field")

        # create a display object
        import display
        display = display.Display()

        import contourdisplay
        import displaymethods
        import color

        edisp = display.add_method(
            displaymethods.EdgeDisplay(outputClones.posOutput))
        edisp.set_param('width', 0.0)
        edisp.set_param('color', color.black)

        perimdisp = display.add_method(
            displaymethods.PerimeterDisplay(outputClones.posOutput))
        perimdisp.set_param('width', 0.01)
        perimdisp.set_param('color', color.red)

        funcOutput = outputClones.FunctionOutput.clone()
        funcOutput.plugParameter(function, 'f')

        contourdisp = display.add_method(
            contourdisplay.PlainContourDisplay(outputClones.posOutput,
                                                funcOutput))
        contourdisp.set_param('levels', nlevels)
        contourdisp.set_param('nbins', contourbins)
        contourdisp.set_param('width', .005)
        contourdisp.set_param('color', color.blue)
        
        # get an output device
        import psoutput
        device = psoutput.PSoutput(psfilename)

        if profilefile:
            import profiler
            prof = profiler.Profiler(profilefile)
        display.draw(mesh, device)
        if profilefile:
            prof.stop()


except ErrSetupError, s:
    print "Caught ErrSetupError."
    print "Message string: " + s.message()
    
