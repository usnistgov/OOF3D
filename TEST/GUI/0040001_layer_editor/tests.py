# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:13:35 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
from layereditortests import *

def sensitivityCheck0():
    return sensitizationCheck(
        {"NewLayer": 1,
         "Send": 1,
         "DisplayMethods:New": 1,
         "DisplayMethods:Edit": 1,
         "DisplayMethods:Copy": 1,
         "DisplayMethods:Delete": 1
        },
        base="OOF2 Graphics Layer Editor")

def sensitivityCheck1():
    return sensitizationCheck(
        {"NewLayer": 1,
         "Send": 0,
         "DisplayMethods:New": 1,
         "DisplayMethods:Edit": 1,
         "DisplayMethods:Copy": 1,
         "DisplayMethods:Delete": 1
        },
        base="OOF2 Graphics Layer Editor")

