# -*- python -*-
# $RCSfile: testequil.py,v $
# $Revision: 1.4.142.1 $
# $Author: langer $
# $Date: 2014/09/27 22:33:40 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import sys, getopt, string
import oofpath
import oofcppc
#
from SWIG.common import pythonexportable
pythonexportable.initPythonExportable(eval)

from engine import problem
problem.initialize()
from engine.problem import *

# More imports. 
from SWIG.common import trace
from SWIG.engine.material import *
#
# Specific property imports -- shouldn't have to do this, there
# should be a way to systematically/automatically get all props.
from SWIG.engine.property.elasticity.aniso.aniso import HexagonalElasticity
from SWIG.engine.property.orientation.orientation import Orientation
#
from SWIG.engine.eulerangle import EulerAngle
from SWIG.engine.masterelement import *
from engine.ghostmesh import *
#
# Start the mesh manager -- ghostmesh needs it.
import engine.meshmanager
engine.meshmanager.initialize()




# Updated profiling code.
from engine.AUX import profiler
prof = profiler.Profiler('testequil.prof') # Defaults for timer, fudge.


trace.trace_disable()
# trace.trace_enable()

hexmaterial = newMaterial("2d-elastic",
                          HexagonalElasticity("hex", 1.0, 0.5, 0.0, 0.0, 0.0),
                          Orientation("unrotated", EulerAngle(0,0,0)))
  
eltypes = getMasterElementList()

#
# Defaults.
meshsize = 1 
para=0  # Parametricity. 1 == super, 0 == iso, -1 == sub
quad=0  # Quadratitude

# mat = Material("Null")

tolerance = 1.e-5
krylov_dim = 10
maxiters = 100

#
# Arguments are: q for quadratic (default is triangular),
# b for subparametric, p for superparametric, and n <size>.
#

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'qbpn:')
except getopt.error, message:
    print "Usage: python testequil.py [-q] [-b|-p] [-n <size>]"
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


# trace.trace_disable()

try:
    # Simple mechanical boundary conditions.
    topflux   = ContinuumProfile('(0.0, -0.1)')
    bottomfix = ContinuumProfile('0.0')

    fixeddispx = mesh.newFixedBC(displacement, 0, forcebalance_eqn, 0)
    fixeddispy = mesh.newFixedBC(displacement, 1, forcebalance_eqn, 1)
    flux       = mesh.newFluxBC(stress_flux)
    
    bottom = mesh.getBoundary('bottom')
    bottom.addCondition(fixeddispx, bottomfix)
    bottom.addCondition(fixeddispy, bottomfix)

    top = mesh.getBoundary('top')
    top.addCondition(flux, topflux)

    print "BC's defined."
    # trace.trace_enable()

    mesh.equilibrate(maxiters, tolerance, krylov_dim)
    # trace.trace_disable()
    for node in mesh.funcnode_iterator():
        pos = node.position()
        print displacement.value(mesh, node, 0),\
              displacement.value(mesh, node, 1)
        
except ErrSetupError, s:
    print "Caught ErrSetupError."
    print "Message string: " + s.message()
    

# More updatedp profiling code.
prof.stop()

