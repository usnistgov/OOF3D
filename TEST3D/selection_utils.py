# -*- python -*-
# $RCSfile: selection_utils.py,v $
# $Revision: 1.1.2.1 $
# $Author: langer $
# $Date: 2013/04/11 19:08:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.engine import cskeletonselectable

uidOffset = None

def initialize():
    global uidOffset
    uidOffset = cskeletonselectable.peekUID()

def selectedElementIDs(skelctxt):
    return [e.uiIdentifier()
            for e in skelctxt.elementselection.retrieve()]

def selectedFaceIDs(skelctxt):
    return [f.uiIdentifier()-uidOffset
            for f in skelctxt.faceselection.retrieve()]

def selectedSegmentIDs(skelctxt):
    return [s.uiIdentifier()-uidOffset
            for s in skelctxt.segmentselection.retrieve()]

def selectedNodeIDs(skelctxt):
    return [n.uiIdentifier()
            for n in skelctxt.nodeselection.retrieve()]

def offsetFaceID(face):
    return face.uiIdentifier() - uidOffset

# CyclicList is a list-like object that can be compared to a list.
# The CyclicList and the list are equal if any cyclic permutation of
# the CyclicList matches the list.  It's used when checking that the
# nodes of a face occur in the correct order, when all that really
# matters is the orientation of the face.  Cyclic permutations of the
# nodes don't change the orientation.

class CyclicList(object):
    def __init__(self, vals):
        self.vals = vals
    def __eq__(self, other):
        if len(self.vals) != len(other):
            return False
        for i in range(len(self.vals)):
            if self.vals[i:] + self.vals[:i] == other:
                return True
        return False

