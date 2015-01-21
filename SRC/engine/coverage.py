# -*- python -*-
# $RCSfile: coverage.py,v $
# $Revision: 1.1.2.1 $
# $Author: langer $
# $Date: 2013/03/25 17:42:42 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# This enum is used in boundarybuilder.py and skeletonselectionmod.py
# when extracting objects of one dimensionality (e.g. faces) from a set
# of another dimensionality (e.g. elements).

from ooflib.common import enum

class Coverage(enum.EnumClass(
        ("Exterior", "Select objects on the exterior of the set"),
        ("Interior", "Select objects on the interior of the set"),
        ("All", "Select all objects in the set."))):
    pass
        
