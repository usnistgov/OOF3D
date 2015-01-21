# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:14:10 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

def homogindex(val, tolerance=1.e-10):
    lines = gtkTextviewGetLines(
        'OOF2:Skeleton Page:Pane:StatusScroll:SkeletonText')
    # Look for a line of the form "Homogeneity Index: xxx"
    for line in lines:
        if line.startswith("Homogeneity Index"):
            try:
                homog = float(line.split()[2])
                return abs(homog - val) <= tolerance
            except:
                # line isn't of the expected form
                return False
    
