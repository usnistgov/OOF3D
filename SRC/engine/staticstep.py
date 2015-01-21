# -*- python -*-
# $RCSfile: staticstep.py,v $
# $Revision: 1.24.2.2 $
# $Author: fyc $
# $Date: 2014/07/28 22:16:03 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import sys

from ooflib.SWIG.common import doublevec
from ooflib.SWIG.engine import ooferror2
from ooflib.SWIG.engine import sparsemat
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import xmlmenudump
from ooflib.engine import symstate
from ooflib.engine import timestepper

## StaticDriver just solves the static finite element matrix (K) at
## the end of a time interval.  It's a StepDriver, but it doesn't take
## multiple steps.  It also allows only one kind of TimeStepper,
## _StaticStepper, so it doesn't have a "stepper" Parameter.

## TODO OPT: MAP StaticDriver and _StaticStepper don't have to use MCK
## order. They could eliminate a mapping step and maybe a copy or two
## by using indfree ordering.


class StaticDriver(timestepper.StepDriver):

    def __init__(self):
        super(StaticDriver, self).__init__( stepper=_StaticStepper() )
        
    def get_unknowns(self, linsys, source):
        return linsys.get_unknowns_MCK(source)
    def set_unknowns(self, linsys, vals, dest):
        return linsys.set_unknowns_MCK(vals, dest)

    def initial_stepsize(self, delta):
        # The static stepper doesn't have anything to say about the
        # stepsize.  It just goes along with whatever the rest of the
        # system requests.
        return delta
    
    def n_unknowns(self, linsys):
        return linsys.n_unknowns_MCK()

    # The static solver treats all unknowns as static (in the 'K' part
    # of the dof vector.)
    def get_unknowns_part(self, part, linsys, unknowns):
        if part == 'K':
            return unknowns.clone()
        return doublevec.DoubleVec(0)
    def set_unknowns_part(self, part, linsys, vals, unknowns):
        if part == 'K':
            unknowns.copy_inplace(vals)
    def rhs_ind_part(self, part, linsys):
        if part == 'K':
            return linsys.rhs_MCK()
        return doublevec.DoubleVec(0)
    def n_unknowns_part(self, part, linsys):
        if part == 'K':
            return linsys.n_unknowns_MCK()
        return 0

    def get_derivs_part(self, part, linsys, unknowns):
        # return linsys.get_derivs_part_MCK(part, unknowns)
        return doublevec.DoubleVec(0)
    def set_derivs_part(self, part, linsys, vals, unknowns):
        # return linsys.get_derivs_part_MCK(part, vals, unknowns)
        pass

    def M_submatrix(self, linsys, rowpart, colpart):
        if rowpart == 'K' and colpart == 'K':
            return linsys.M_MCK()
        return sparsemat.SparseMat(0,0)
    def C_submatrix(self, linsys, rowpart, colpart):
        if rowpart == 'K' and colpart == 'K':
            return linsys.C_MCK()
        return sparsemat.SparseMat(0,0)
    def K_submatrix(self, linsys, rowpart, colpart):
        if rowpart == 'K' and colpart == 'K':
            return linsys.K_MCK()
        return sparsemat.SparseMat(0,0)
    def J_submatrix(self, linsys, rowpart, colpart):
        if rowpart == 'K' and colpart == 'K':
            return linsys.J_MCK()
        return sparsemat.SparseMat(0,0)


class _StaticStepper(timestepper.LinearStepper, timestepper.NonLinearStepper):

    def derivOrder(self):
        return 0

    def shortrepr(self):
        return "No time stepping"

    def evaluateBeginning(self):
        # Quasistatic time stepping requires that the matrices are
        # evaluated at the end of the time step.
        return False

    def staticSolve(self, subproblem, linsys, dofs):
        K = linsys.K_MCK()
        rhs = linsys.rhs_MCK()
        subproblem.matrix_method(subproblem.asymmetricK).solve(K, rhs, dofs)

    def linearstep(self, subproblem, linsys, time, unknowns, endtime):
        # This function is called only when solving quasi-static
        # problems.  Fully static problems are solved by
        # SubProblemContext.initializeStaticFields.

        # Use unknowns as an initial guess for the solution.  The
        # calculation is done in place. (evolve.py created the
        # unknowns vector by calling SubProblemContext.get_unknowns,
        # which copied them out of the subproblem's dof list, so we're
        # already working with a copy here.)
        linsys = subproblem.make_linear_system(endtime, linsys)
        self.staticSolve(subproblem, linsys, unknowns)
        return timestepper.StepResult(endTime=endtime, endValues=unknowns,
                                      linsys=linsys)

    def nonlinearstep(self, subproblem, linsys, time, unknowns,
                      endtime, nonlinearMethod):
        data = timestepper.NLData( subproblem, linsys, endtime )
        endValues = unknowns.clone()
        nonlinearMethod.solve(
            subproblem.matrix_method(subproblem.asymmetricK),
            self.precomputeNL,
            self.compute_residual, self.compute_jacobian,
            self.compute_linear_coef_mtx,
            data, endValues )
        return timestepper.StepResult(endTime=endtime, endValues=endValues,
                                      linsys=linsys)

    def compute_residual(self, data, soln, nlsolver):
        return data.linsys.static_residual_MCK()

    def compute_jacobian(self, data, nlsolver):
        return data.linsys.J_MCK()

    def compute_linear_coef_mtx(self, data, nlsolver):
        return data.linsys.K_MCK()


####################################################################

registeredclass.Registration(
    'Static',
    timestepper.StepDriver,
    StaticDriver,
    ordering=0,
    tip="Solve a subproblem as a static or quasi-static system.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/staticdriver.xml'))

# _StaticStepper never appears in the user interface because there's
# only one kind of static stepper, so it doesn't really need a
# Registration.  However, if it doesn't have a Registration its
# __repr__ doesn't work, which hinders debugging.  So here it has a
# Registration, but it's secret.

registeredclass.Registration(
    'Static',
    timestepper.TimeStepper,
    _StaticStepper,
    tip="Used internally by the Static StepDriver",
    secret=True,
    ordering=10000)
