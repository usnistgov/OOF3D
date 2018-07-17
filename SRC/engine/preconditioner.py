# -*- python -*-

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

## In the Eigen matrix method templates, the preconditioner isn't a
## separate object from the solver.  These classes here are just
## placeholders that are used in the PreconditionedMatrixMethod
## classes in matrixmethod.py to choose the correct Eigen routine.

class PreconditionerBase(registeredclass.RegisteredClass):
    registry = []
    tip = "Preconditioners for efficient solution of matrix equations."
    discussion = xmlmenudump.loadFile('DISCUSSIONS/engine/reg/preconditioner.xml')
    def shortrepr(self):
        return self.__class__.__name__

class UnPreconditioner(PreconditionerBase):
    name = "Un"

class JacobiPreconditioner(PreconditionerBase):
    name = "Diag"

class ILUTPreconditioner(PreconditionerBase):
    name = "ILUT"

# ILU preconditioner actually points to ILUT preconditioner
class ILUPreconditioner(PreconditionerBase):
    name = "ILU"

registeredclass.Registration(
    "Null",
    PreconditionerBase,
    UnPreconditioner,
    ordering=2000,
    params=[],
    tip="Be bold (or foolhardy) and attempt to solve the mesh without a preconditioner")

registeredclass.Registration(
    "Jacobi",
    PreconditionerBase,
    JacobiPreconditioner,
    ordering=500,
    params=[],
    tip="A light-weight preconditioner, that simply inverts the diagonal part of the matrix.")

registeredclass.Registration(
    "IncompleteLUT",
    PreconditionerBase,
    ILUTPreconditioner,
    ordering=100,
    params=[],
    tip="Incomplete LU-factorization with dual thresholding.")

registeredclass.Registration(
    "ILU",
    PreconditionerBase,
    ILUPreconditioner,
    ordering=101,
    params=[],
    tip="ILU is not supported. It points to IncompleteLUT instead.") 
