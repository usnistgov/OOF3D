# -*- python -*-
# $RCSfile: solvermode.py,v $
# $Revision: 1.8.4.2 $
# $Author: langer $
# $Date: 2013/11/08 20:44:51 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import matrixmethod
from ooflib.engine import nonlinearsolver
from ooflib.engine import timestepper


class SolverMode(registeredclass.RegisteredClass):
    registry = []
    tip='How to choose the solution methods.'
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/solvermode.xml')

class BasicSolverMode(SolverMode):
    def __init__(self, time_stepper, matrix_method):
        self.time_stepper = time_stepper
        self.matrix_method = matrix_method
    def get_time_stepper(self, subproblemcontext, existingStepper):
        return self.time_stepper.resolve(subproblemcontext, existingStepper)
    def get_nonlinear_solver(self, subproblemcontext, existingNLSolver):
        if subproblemcontext.nonlinear_activefields():
            return nonlinearsolver.Newton(relative_tolerance=1.e-5,
                                          absolute_tolerance=1.e-15,
                                          maximum_iterations=200)
        return nonlinearsolver.NoNonlinearSolver()
    def get_symmetric_solver(self, subproblemcontext, existingSolver):
        return self.matrix_method.resolve_symmetric(existingSolver)
    def get_asymmetric_solver(self, subproblemcontext, existingSolver):
        return self.matrix_method.resolve_asymmetric(subproblemcontext, 
                                                     existingSolver)
    def derivOrder(self, subproblemcontext):
        pass
    def require_timederiv_field(self, subproblemcontext):
        pass
    def shortrepr(self):
        return '%s | %s' % (self.time_stepper.shortrepr(), 
                            self.matrix_method.shortrepr())

registeredclass.Registration(
    "Basic",
    SolverMode,
    BasicSolverMode,
    ordering=0,
    params=[
        timestepper.BasicStepDriverParameter(
            'time_stepper',
            tip='How to take time steps.'),
        parameter.RegisteredParameter(
            'matrix_method',
            matrixmethod.BasicMatrixMethod,
            tip='How to solve matrix equations.')
        ],
    tip="Let OOF2 choose many solution parameters.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/basicsolvermode.xml')
    )

def _rep(obj):
    if obj is None:
        return '---'
    return obj.shortrepr()

class AdvancedSolverMode(SolverMode):
    def __init__(self, time_stepper, nonlinear_solver, 
                 symmetric_solver, asymmetric_solver):
        self.time_stepper = time_stepper
        self.nonlinear_solver = nonlinear_solver
        self.symmetric_solver = symmetric_solver
        self.asymmetric_solver = asymmetric_solver
    def get_time_stepper(self, *args):
        return self.time_stepper
    def get_nonlinear_solver(self, *args):
        return self.nonlinear_solver
    def get_symmetric_solver(self, *args):
        return self.symmetric_solver
    def get_asymmetric_solver(self, *args):
        return self.asymmetric_solver
    def shortrepr(self):
        return "%s | %s | %s | %s" % (_rep(self.time_stepper),
                                      _rep(self.nonlinear_solver),
                                      _rep(self.symmetric_solver),
                                      _rep(self.asymmetric_solver))

registeredclass.Registration(
    "Advanced",
    SolverMode,
    AdvancedSolverMode,
    ordering=1,
    params=[
        parameter.RegisteredParameter(
            'time_stepper', timestepper.StepDriver,
            tip="How to take time steps."),
        parameter.RegisteredParameter(
            'nonlinear_solver', nonlinearsolver.NonlinearSolverBase,
            tip="How to solve nonlinear equations."),
        matrixmethod.SymmetricMatrixMethodParam(
            'symmetric_solver',
            tip='How to solve symmetric matrix equations.'),
        matrixmethod.AsymmetricMatrixMethodParam(
            'asymmetric_solver',
            tip='How to solve asymmetric matrix equations.')
        ],
    tip="Choose all solution parameters yourself.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/advancedsolvermode.xml'))
