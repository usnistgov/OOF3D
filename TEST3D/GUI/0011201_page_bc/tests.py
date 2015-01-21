# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.3 $
# $Author: langer $
# $Date: 2014/09/27 22:35:00 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from generics import *

def boundaryConditionCheck(names):
    return names == [x for x in treeViewColValues('OOF3D:Boundary Conditions Page:Condition:BCScroll:BCList', 0)]

def boundaryConditionSelectedCheck(name):
    return name == treeViewSelectCheck('OOF3D:Boundary Conditions Page:Condition:BCScroll:BCList', 0)
