# -*- python -*-
# $RCSfile: incremental.py,v $
# $Revision: 1.17.2.3 $
# $Author: langer $
# $Date: 2014/10/09 02:50:29 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import doublevec
from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import xmlmenudump
from ooflib.engine import symstate
from ooflib.engine import timestepper

import sys
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# The incremental stepper.  Motivated by plasticity, it's for
# quasistatic properties where some or most of the action in
# evolving the system is actually in the properties themselves,
# which compute state-dependent deltas, and accumulate history,
# out of sight of the stepping process.  Possbily fluid flow
# is like this too, but we're not (currently) doing that.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Incremental(timestepper.LinearStepper, timestepper.NonLinearStepper,
                  timestepper.FirstOrderStepper):

    def derivOrder(self):
        return 1

    def errorOrder(self):
        return 2.0  # TODO: Really?

    def shortrepr(self):
        return "Incremental"

    # Linear and nonlinear versions just differ in how they evaluate
    # the static residual part.  The linear version uses K*u-f.  The
    # nonlinear version doesn't.  linearstep and nonlinearstep both
    # call _do_step to do the work, but pass it different functions
    # to compute the residual.

    def linearstep(self, subproblem, linsys, time, unknowns, endtime):
        return self._do_step(subproblem, linsys, time, unknowns, endtime,
                             self._linear_residual)

    def nonlinearstep(self, subproblem, linsys, time, unknowns, endtime,
                      nonlinearMethod):
        print >> sys.stderr, "---> Incremental.nonlinearstep."
        print >> sys.stderr, "---> Calling _do_step."
        print >> sys.stderr, "---> NL method is ", nonlinearMethod
        return self._do_step(subproblem, linsys, time, unknowns, endtime,
                             self._nonlinear_residual)

    def _linear_residual(self, linsys, dt, unknowns):
        v = dt*linsys.rhs_MCa()
        # K_MCa is really (MCa)x(MCKa), so we can multiply by
        # unknowns, which includes the K part.
        K = linsys.K_MCa()       # really (MCa)x(MCKa)
        K.axpy(-dt, unknowns, v) # v = dt*(f - K u)
        return v

    def _nonlinear_residual(self, linsys, dt, unknowns):
        return (-dt)*linsys.static_residual_MCa(unknowns)

    def _do_step(self, subproblem, linsys, time, unknowns, endtime, get_res):
        print >> sys.stderr, "----> Inside Incremental _do_step."
        # TODO: Do the incremental thing.
        # This involves, firstly, using the previous K matrix to
        # do an initial solve to get your first guess for u, and then
        # using those u's to build the subsequent matrix, which
        # you solve by NR.  Incremental problems are always nonlinear.

        # Below here is obsolete.
        # Solve C(u_{n+1} - u_n) = dt*(f - K u_n)
        # C and K are effective matrices, coming from the reduction of
        # a second order problem to a system of first order problems.

        # If C has empty rows, the static solution of those rows has
        # already been computed by initializeStaticFields() or by a
        # previous Euler step, and we only have to solve the remaining
        # nonempty rows here.  Unlike GeneralizedEuler, here we're
        # solving an unmodified C, so it can't contain empty rows.
        staticEqns = linsys.n_unknowns_part('K') > 0
        
        dt = endtime - time
        # v = dt * linsys.rhs_MCa() # v = dt*f 

        # # K_MCa is really (MCa)x(MCKa), so we can multiply by
        # # unknowns, which includes the K part.
        # K = linsys.K_MCa()
        # K.axpy(-dt, unknowns, v) # v = dt*(f - K u)
        v = get_res(linsys, dt, unknowns)

        C = linsys.C_MCa()
        # solve() stores u_{n+1}-u_n in endValues.  Before calling
        # solve, set endValues to a good guess for u_{n+1}-u_n.
        # Assuming that the step size is small, a good guess is zero.
        endValues = doublevec.DoubleVec(unknowns.size())
        endValues.zero()

        x = linsys.extract_MCa_dofs(endValues)
        print >> sys.stderr, "----> Calling matrix method.solve:"
        subproblem.matrix_method(_asymmetricFE, subproblem, linsys).solve(
            C, v, x )
        linsys.inject_MCa_dofs(x, endValues)

        endValues += unknowns

        if staticEqns:
            # Re-solve the static equations at endtime.
            subproblem.installValues(linsys, endValues, endtime)
            linsys = subproblem.make_linear_system(endtime, linsys)
            subproblem.computeStaticFields(linsys, endValues)

        return timestepper.StepResult(endTime=endtime, nextStep=dt,
                                      endValues=endValues, linsys=linsys)

def _asymmetricFE(subproblem, linsys):
    # If the problem has second order time derivatives, then we'll be
    # using C_eff, which is symmetric if M and C are both symmetric
    # and if C21 is zero.
    
    # If the problem has no second order time derivatives, we'll just
    # be using C.  M's symstate will be INCONSISTENT and C21 will be
    # empty.
    
    return (subproblem.matrix_symmetry_M == symstate.ASYMMETRIC or
            subproblem.matrix_symmetry_C == symstate.ASYMMETRIC or
            linsys.C21_nonempty())


registeredclass.Registration(
    'Incremental',
    timestepper.TimeStepper,
    Incremental,
    ordering=5,
    explicit=True,
    tip="Incremental time stepper.",
    # discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/incremental.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
