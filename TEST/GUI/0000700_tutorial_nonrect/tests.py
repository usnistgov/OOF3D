# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:36 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *

def skeletonBdySensitizationCheck0():
    return sensitizationCheck(
        {'New' : 1,
         'Modify' : 0,
         'Rename' : 0,
         'Delete' : 0
         },
        base='OOF2:Skeleton Boundaries Page:Pane:Boundaries')

def skeletonBdySensitizationCheck1():
    return sensitizationCheck(
        {'New' : 1,
         'Modify' : 1,
         'Rename' : 1,
         'Delete' : 1
         },
        base='OOF2:Skeleton Boundaries Page:Pane:Boundaries')
    

def skeletonBdySizeCheck(skeleton, bdyname, size):
    from ooflib.common.IO import whoville
    sc = whoville.getClass('Skeleton')[skeleton]
    bdy = sc.getBoundary(bdyname)
    return bdy.current_size() == size
