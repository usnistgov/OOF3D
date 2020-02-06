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

    # TODO: Linear and nonlinear might be the same?  We care
    # about the residual.  Compare with ForwardEuler, for example.

    def linearstep(self, subproblem, linsys, time, unknowns, endtime):
        return self._do_step(subproblem, linsys, time, unknowns, endtime,
                             self._linear_residual, None)

    def nonlinearstep(self, subproblem, linsys, time, unknowns, endtime,
                      nonlinearMethod):
        print >> sys.stderr, "IS-NL: ---> Incremental.nonlinearstep."
        print >> sys.stderr, "IS-NL: ---> Calling _do_step."
        print >> sys.stderr, "IS-NL: ---> NL method is ", nonlinearMethod
        return self._do_step(subproblem, linsys, time, unknowns, endtime,
                             self._nonlinear_residual, nonlinearMethod)

    def _linear_residual(self, linsys, dt, unknowns):
        v = dt*linsys.rhs_MCa()
        # K_MCa is really (MCa)x(MCKa), so we can multiply by
        # unknowns, which includes the K part.
        K = linsys.K_MCa()       # really (MCa)x(MCKa)
        K.axpy(-dt, unknowns, v) # v = dt*(f - K u)
        return v

    def _nonlinear_residual(self, linsys, dt, unknowns):
        return (-dt)*linsys.static_residual_MCa(unknowns)

    # TODO: At the moment, both lienarstep and nonlinearstep call this
    # _do_step routine, but this might not be right -- nonlinear
    # methods need the "nlmethod" arg, which is just "None" for the
    # linear call, which is broken.  The linear case is just static,
    # so it can be separate, it's (probably) much easier.
    def _do_step(self, subproblem, linsys, time, unknowns, endtime,
                 get_res, nlmethod):
        print >> sys.stderr, "IS_DS----> Inside Incremental _do_step."
        # TODO: Do the incremental thing.
        # This involves, firstly, using the previous K matrix to
        # do an initial solve to get your first guess for u, and then
        # using those u's to build the subsequent matrix, which
        # you solve by NR.  Incremental problems are always "logically"
        # nonlinear, even if they're not actually nonlinear.
        #
        # Steps:
        # 1: Set up the current boundary conditions, and do an
        #    initial solve with the previous K matrix.  This is
        #    just linear algebra, no NR.
        # 2: Use the resulting DOFs as the starting guess for a
        #    full NR iteration, including of course rebuilding  the
        #    DOF-dependent K matrix. 
        # 3: Once 2 is converged, we're done. 

        # get_res is self._nonlinear_residual, which is actually
        # implemented above.  

        # Problem(?): The boundary conditions are manipulated inside
        # the subproblemcontext, but we have a special requirement to
        # move the Dirichlet boundaries without updating the matrix so
        # we can build a good initial condition for our NR lop.  See
        # the BC code in subproblemcontext.make_linear_system for
        # clues.
        #
        # To start, apply the bc's and do a linear solve:
        # mesh = subproblem.getParent()
        # femesh = mesh.getObject()
        # femesh.setCurrentSubProblem(subproblem.getObject())
        # femesh.invoke_fixed_bcs(subproblem.getObject(),linsys, target_time)
        # This builds the index maps in the linsys, but actually sets
        # the values in the FEMesh object's dofvalues array.
        # Q: Maybe we want to re-apply all the bc's?  
        # If so:  BC code at line 817 of subproblemcontext.py.
        # Break it out into a separate function, be careful about the time.
        
        # Then, actually do a linear solve with
        # the bc's for the target time of this step, but the linearized
        # system from the previous step (or from the static part, if
        # it's the first iteration.)
        
        # subprobctxt.matrix_method(_assymetricIC,subprobctxt,linsys).solve(A,b,x)

        # This solves Ax=b for x, it's linear.

        # The matrix we want is the K matrix from the linsys object.
        # Get K from linsys.K_MCK(). 
        # What is b? It's just linsys.rhs_MCK(), this problem looks like
        # a static problem from the point of view of the linearized system.

        # This does not include the fixed BC contribution to the RHS
        # -- how to do that?
        
        # Then, once we have X, install it in the subproblem
        # (with subproblemcontext.installValues()?).
        

        # Then, finally, solve the system at the target time.
        # See the "nonlinearstep" method of backward Euler.
        # Call is:
        # nlmethod.solve(subproblem.matrixmethod(_asymmetricIC, subproblem),
        #                self.precomputeNL, self.compute_residual,
        #                self.compute_linear_coef_matrix, data, endValues)
        # TODO: Figure out if we have these arguments, and where the
        # data goes.

        # Then:
        # return timestepper.StepResults(endTime=?, nextStep=dt,
        #                                endValues=endValues,
        #                                linsys=linsys)
        

        # Obsolete below this line.
        
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
        print >> sys.stderr, "IS_DS:----> Calling matrix method.solve:"
        subproblem.matrix_method(_asymmetricFE, subproblem, linsys).solve(
            C, v, x )
        print >> sys.stderr, "IS-DS:----> Back from matrix method solve."
        linsys.inject_MCa_dofs(x, endValues)
        print >> sys.stderr, "IS-DS:----> Back from linsys modification."

        
        endValues += unknowns

        if staticEqns:
            # Re-solve the static equations at endtime.
            subproblem.installValues(linsys, endValues, endtime)
            linsys = subproblem.make_linear_system(endtime, linsys)
            subproblem.computeStaticFields(linsys, endValues)

        return timestepper.StepResult(endTime=endtime, nextStep=dt,
                                      endValues=endValues, linsys=linsys)

def _asymmetricIC(subproblem, linsys):
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
