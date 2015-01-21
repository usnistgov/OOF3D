# -*- python -*-
# $RCSfile: meshstatus.py,v $
# $Revision: 1.7.2.1 $
# $Author: langer $
# $Date: 2013/11/08 20:44:34 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump

# MeshStatus is a RegisteredClass because the status is set in Mesh
# data files via a command that uses a RegisteredParameter.  It's
# never set explicitly by the user.  Its subclasses are not documented
# automatically like other RegisteredClasses are, but are discussed in
# the Mesh section of the manual.

class MeshStatus(registeredclass.RegisteredClass):
    registry = []
    secret = True
    def __init__(self, details=""):
        self.details = details
    def getDetails(self):
        return self.details

# Subclasses have to have two data members.  "tag" is a string that
# appears in the Status box on the Solver page.  "solvable" is a bool
# that says whether or not the mesh can be solved in its current
# state.  It's used to sensitize the "Solve" button on the Solver
# page.

class Unsolved(MeshStatus):
    tag = "Unsolved"
    solvable = True

registeredclass.Registration(
    "Unsolved",
    MeshStatus,
    Unsolved,
    params=[parameter.StringParameter("details")],
    ordering=0,
    tip=parameter.emptyTipString)

class Unsolvable(MeshStatus):
    tag = "Unsolvable"
    solvable = False

registeredclass.Registration(
    "Unsolvable",
    MeshStatus,
    Unsolvable,
    params=[parameter.StringParameter("details")],
    ordering=1,
    tip=parameter.emptyTipString)

class Solving(MeshStatus):
    tag = "Solving..."
    solvable = False

registeredclass.Registration(
    "Solving",
    MeshStatus,
    Solving,
    params=[parameter.StringParameter("details")],
    ordering=2,
    tip=parameter.emptyTipString)

class Solved(MeshStatus):
    tag = "Solved"
    solvable = True

registeredclass.Registration(
    "Solved",
    MeshStatus,
    Solved,
    params=[parameter.StringParameter("details")],
    ordering=3,
    tip=parameter.emptyTipString)

class Failed(MeshStatus):
    tag = "Solution failed"
    solvable = True

registeredclass.Registration(
    "Failed",
    MeshStatus,
    Failed,
    params=[parameter.StringParameter("details")],
    ordering=4,
    tip=parameter.emptyTipString)

# OutOfSync indicates that the Skeleton has changed and the Mesh is
# invalid.

class OutOfSync(MeshStatus):
    tag = "Out of sync with Skeleton"
    solvable = False

registeredclass.Registration(
    "Out Of Sync",
    MeshStatus,
    OutOfSync,
    ordering=5,
    tip=parameter.emptyTipString)
