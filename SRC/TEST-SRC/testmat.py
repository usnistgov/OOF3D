# -*- python -*-
# $RCSfile: testmat.py,v $
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

##from oofcpp import *
##from problem import *
from oof import *

trace_disable()


hexmaterial = newMaterial("2d-elastic",
                          HexagonalElasticity("hex", 1.0, 0.5, 0.0, 0.0, 0.0),
                          Orientation("unrotated", EulerAngle(0,90,0)),
                          ColorProperty("gray",0.5))
print "created hexmaterial"
print hexmaterial

try:
    nosuchprop = hexmaterial.fetchProperty("elaxtixity")
except ErrNoSuchProperty, msg:
    print "Error!", msg

try:
    incompletematerial = newMaterial("incomplete", CubicElasticity("cubic", 1,2,4))
except ErrPropertyMissing, msg:
    print "Error!", msg

cprop = CubicElasticity("cubic", 1, 2, 3)

print "Creating 'badmaterial' with a redundant property"
badmaterial = newMaterial("redundant",
                       cprop,
                       CubicElasticity("another one", 4,5,6),
                       Orientation("bi", EulerAngle(1,2,3)))

print badmaterial

print "---\nRemoving duplicate property from 'badmaterial'"
badmaterial.removeProperty(cprop)
print badmaterial

print "---\nCopying material 2d-elastic"
h2 = hexmaterial.copy('hex2')
print h2

print "---\nRetrieving properties by registration name from 2d-elastic"
for name in ("Elasticity", "Orientation", "Color"):
    try:
        prop = hexmaterial.fetchProperty(name)
        if prop:
            print name, "=", prop
    except NameError, msg:
        print "NameError:", msg

