# -*- python -*-
# $RCSfile: tests.py,v $
# $Revision: 1.1.2.1 $
# $Author: fyc $
# $Date: 2013/07/10 16:10:24 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@ctcms.nist.gov. 

from generics import *
import os

# Make sure that the skeleton.dat output file doesn't already exist.
removefile('skeleton.dat')

def skeletonElementSelectionSizeCheck(skeleton, n):
    from ooflib.common.IO import whoville
    sc = whoville.getClass('Skeleton')[skeleton]
    return sc.elementselection.size() == n

def skeletonSizeCheck(skeleton, nel, nnode):
    from ooflib.common.IO import whoville
    skel = whoville.getClass('Skeleton')[skeleton].getObject()
    return skel.nelements() == nel and skel.nnodes() == nnode
