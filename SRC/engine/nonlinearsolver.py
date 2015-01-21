# -*- python -*-
# $RCSfile: nonlinearsolver.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2014/10/15 20:53:46 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Nonlinear solvers for use by subproblems.  These are derived from
# the classes in nonlinearsolvercore.py, which do the actual work, but
# are agnostic about subproblems.

import sys

from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import nonlinearsolvercore


class NonlinearSolverBase(registeredclass.RegisteredClass):
    registry = []
    tip="Base class for nonlinear solvers, including the null solver."
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/nonlinearsolverbase.xml')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# NoNonlinearSolver is actually a linear solver.  The order of the
# base classes is important to prevent swig 1.1 from complaining
# about the type of the "self" arg to CNonlinearSolver::nonlinear.

class NoNonlinearSolver(nonlinearsolvercore.NoNLSolver, NonlinearSolverBase):
    def step(self, subproblem, *args, **kwargs):
        self.requireResidual(False) # Sets flags in CNonlinearSolver.
        self.requireJacobian(False) # Ditto.
        v = subproblem.time_stepper.linearstep(subproblem, *args, **kwargs)
        return v
            
    def computeStaticFields(self, subprobctxt, linsys, unknowns):
        # Called by SubProblemContext.initializeStaticFields.
        return subprobctxt.computeStaticFieldsL(linsys, unknowns)
    def shortrepr(self):
        return "None"
    def __repr__(self):
        return registeredclass.RegisteredClass.__repr__(self)

registeredclass.Registration(
    'None',
    NonlinearSolverBase,
    NoNonlinearSolver,
    ordering = 0,
    tip = "Use linear equation solvers.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/nononlinear.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class NonlinearSolver(NonlinearSolverBase):
    def step(self, subprob, *args, **kwargs):
        return subprob.time_stepper.nonlinearstep(
            subprob, nonlinearMethod=self, *args, **kwargs)
    def computeStaticFields(self, subprobctxt, linsys, unknowns):
        # Called by SubProblemContext.initializeStaticFields.
        return subprobctxt.computeStaticFieldsNL(linsys, unknowns)

# Shared parameters for the nontrivial solvers.

nonlin_params = [
    parameter.FloatParameter(
        'relative_tolerance', 1.e-8,
        tip="Relative tolerance for convergence to a nonlinear solution."),
    parameter.FloatParameter(
        'absolute_tolerance', 1.e-13,
        tip="Absolute tolerance for convergence to a nonlinear solution."),
    parameter.IntParameter(
        'maximum_iterations', 200,
        tip="Maximum number of iterations for convergence to a nonlinear solution.")
    ]


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Newton(nonlinearsolvercore.Newton, NonlinearSolver):
    def __init__(self, *args, **kwargs):
        nonlinearsolvercore.Newton.__init__(self, *args, **kwargs)
    def solve(self, *args, **kwargs):
        niters, residual = nonlinearsolvercore.Newton.solve(
            self, *args, **kwargs)
        self.subproblem.solverStats.nonlinearSolution(niters, residual)
    def __repr__(self):
        return registeredclass.RegisteredClass.__repr__(self)

registeredclass.Registration(
    'Newton',
    NonlinearSolverBase,
    Newton,
    ordering = 1,
    params   = nonlin_params,
    tip      = "Solve nonlinear equations with Newton's method.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/newton.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Picard(nonlinearsolvercore.Picard, NonlinearSolver):
    def __init__(self, *args, **kwargs):
        nonlinearsolvercore.Picard.__init__(self, *args, **kwargs)
    def solve(self, *args, **kwargs):
        niters, residual = nonlinearsolvercore.Picard.solve(
            self, *args, **kwargs)
        self.subproblem.solverStats.nonlinearSolution(niters, residual)
    def __repr__(self):
        return registeredclass.RegisteredClass.__repr__(self)

registeredclass.Registration(
    'Picard',
    NonlinearSolverBase,
    Picard,
    ordering = 2,
    params   = nonlin_params,
    tip      = "Solve nonlinear equations with Picard iteration. Picard converges more slowly than Newton's method, but does less work per iteration.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/picard.xml')
    )


