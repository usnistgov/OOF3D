# -*- python -*-
# $RCSfile: testnodeiterator.py,v $
# $Revision: 1.5.142.1 $
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
import oofpath
import oofcppc

# Initialize PythonExportable.
import SWIG.common.pythonexportable

from engine import problem
problem.initialize()
from engine.problem import *

# More imports.  This is hopefully temporary, just to see what's
# needed to actually run something.
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
#

trace.trace_disable()


hexmaterial = newMaterial("2d-elastic",
                       HexagonalElasticity("hex", 1.0, 0.5, 0.0, 0.0, 0.0),
                       Orientation("unrotated", EulerAngle(0,0,0)))
  
eltypes = getMasterElementList()

#
# Defaults.
meshsize = 1 
para=0  # Parametricity. 1 == super, 0 == iso, -1 == sub
quad=0  # Quadratitude

#
# Arguments are: q for quadratic (default is triangular),
# b for subparametric, p for superparametric, and n <size>.
#

try:
    optlist, args = getopt.getopt(sys.argv[1:], 'qbpn:')
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


trace.trace_enable()

def test_iterator(iter):
    for node in iter(): print node
    print " --- offset by 1"
    it = iter()
    jt = it + 1
    for node in jt: print node
    print " --- offset and reset"
    jt = it + 1
    jt.set_start()
    for node in jt: print node
    
for element in mesh.element_iterator():
    print "--- All Nodes"
    test_iterator(element.node_iterator)
    print "--- Map Nodes"
    test_iterator(element.mapnode_iterator)
    print "--- Func Nodes"
    test_iterator(element.funcnode_iterator)
    print "--- Corner Nodes"
    test_iterator(element.cornernode_iterator)
    

