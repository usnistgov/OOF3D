# -*- python -*-
# $RCSfile: symstate.py,v $
# $Revision: 1.4.2.1 $
# $Author: langer $
# $Date: 2013/11/08 20:44:54 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Strings indicating the stiffness matrix symmetry state are also used
# in messages to the user, so be polite.  These are used as values of
# the subproblem's self.matrix_symmetry attribute, and are set in
# conjugate.py's check_symmetry function.

import types

SYMMETRIC="Symmetric"
ASYMMETRIC="Asymmetric"
INCONSISTENT="Symmetry unknown"

class SymState(object):
    def __init__(self, tag=INCONSISTENT):
        self.tag = tag
    def __repr__(self):
        return self.tag
    def __eq__(self, other):
        if type(other) is types.StringType:
            return self.tag == other
        return self.tag == other.tag
    def reset(self):
        self.tag = INCONSISTENT
    def set_inconsistent(self):
        if self.tag != ASYMMETRIC:
            self.tag = INCONSISTENT
    def set_symmetric(self):
        if self.tag != ASYMMETRIC:
            self.tag = SYMMETRIC
    def set_asymmetric(self):
        self.tag = ASYMMETRIC


