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

    # Currently only does anything meaningful for the nonlinear case,
    # the linear stuff is stubbed out.  We can fix this later on once
    # we know what a linear incremental time-step actually is.

    def linearstep(self, subproblem, linsys, time, unknowns, endtime):
        pass


    def _nonlinear_residual(self, linsys, dt, unknowns):
        return (-dt)*linsys.static_residual_MCa(unknowns) # ?
    
    def nonlinearstep(self, subproblem, linsys, time, unknowns, endtime,
                      nonlinearMethod):
        print >> sys.stderr, "IS-NL: ---> Incremental.nonlinearstep."
        print >> sys.stderr, "IS-NL: ---> Calling _do_step."
        print >> sys.stderr, "IS-NL: ---> NL method is ", nonlinearMethod
        return self._do_nonlinear_step(subproblem, linsys, time,
                                       unknowns, endtime,
                                       self._nonlinear_residual,
                                       nonlinearMethod)


    # Nonlinear case is more complicated, you need to advance the bc's
    # and then do the NR loop with the initial guess that is the
    # linear solution of the prior K with the new BC.
    def _do_nonlinear_step(self, subproblem, linsys, time, unknowns, endtime,
                           get_res, nlmethod):
        print >> sys.stderr, "IS_DS----> Inside Incremental _do_nonlinear_step."
        print >> sys.stderr, "A2020 Stepper entrance, targeting ", endtime
        # TODO: Do the incremental thing.
        # This involves, firstly, using the previous K matrix to
        # do an initial solve to get your first guess for u, and then
        # using those u's to build the subsequent matrix, which
        # you solve by NR.  Incremental problems are always "logically"
        # nonlinear, even if they're not actually nonlinear.

        # endtime is the target time from evolve_to, it's generally
        # large, and is not related to our step-size capability, which
        # is set by our driver, which will usually be the
        # UniformDriver.


        print >> sys.stderr, "Incremental nonlinear step, dt = ", endtime - time
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
        mesh = subproblem.getParent()
        femesh = mesh.getObject()
        femesh.setCurrentSubProblem(subproblem.getObject())
        
        # First boolean argument indicates boundaries have been reset.
        # Second boolean argument says field values are not changed.
        print >> sys.stderr, "A2020 Applying bcs."
        print >> sys.stderr, "IS_DS----> Applying bcs at time ", endtime
        # Apparently not working?
        subproblem.apply_bcs(endtime,linsys,True,False)
        
        # This builds the index maps in the linsys.
        
        # Then, actually do a linear solve with
        # the bc's for the target time of this step, but the linearized
        # system from the previous step (or from the static part, if
        # it's the first iteration.)

        # A is linsys.K_MCK(), it's the K matrix from last time.
        # b is linsys.rhs_MCK(), which includes the boundary RHS contributions.
        Amtx = linsys.K_MCK()
        bvec = linsys.rhs_MCK()

        # Xvec needs to be allocated with the right size.  This is a
        # dumb way to do this, but it's easy.
        xvec = bvec.clone()

        print >> sys.stderr, "IS_DS----> Calling linear solver."
        subproblem.matrix_method(_asymmetricIC,subproblem,linsys).solve(
            Amtx,bvec,xvec)

        # Then, once we have X, install it in the subproblem.
        # Needs linsys for the index maps, presuambly.
        print >> sys.stderr, "IS_DS----> Installing linear solution."
        subproblem.installValues(linsys, xvec, time)
        print >> sys.stderr, "IS_DS----> Back from installing linear soln."


        ilfuncs = IncrementalNLFuncs(xvec)
        ildata = IncrementalNLData(subproblem,linsys,time)

        # -----
        # NR loop below here.
        
        # Actually do the NR loop.

        # Modeled after the StaticNLFuncs.

        # self.precomputeNL -> takes as arguments "data", "values",
        #    and the solver.  The solvers promise to call this before
        #    calling compute_residual or compute_jacobian -- this is
        #    the place to put the call to make_linear_system.
        
        # self.compute_residual -> takes as arguments "data",
        #    "values", and the solver, and needs to return the values of
        #    the free equations for the current set of DOFs.

        # self.compute_jacobian -> takes as arguments "data", and
        #     the solver, and returns the matrix of derivatives of the
        #     independent equations with respect to the free dofs.
        
        # self.compute_linear_coef_matrix is used by the Picard solver
        #  but not by the Newton solver, it can be the Jacobian thing
        #  for now, but TODO figure this out.
        
        # endValues -> Candidate solution at input?  (Initial state?)

        # See the StaticNLFuncs object in subproblemcontext.py for clues.
        # What we actually want is more or less the static solution,
        # since we're a quasi-static stepper.

        # TODO: Are these the bad ones?
        # endValues = unknowns.clone()  # -> old way.
        
        # endValues = subproblem.get_unknowns(linsys)
        endValues = xvec.clone()

        print >> sys.stderr, "Endvalues: ", endValues

        print >> sys.stderr, "Incremental calling nlmethod, ", nlmethod
        # Call is:
        nlmethod.solve(subproblem.matrix_method(_asymmetricIC, subproblem,
                                                linsys),
                       ilfuncs.precompute, ilfuncs.compute_residual,
                       ilfuncs.compute_jacobian,
                       ilfuncs.compute_linear_coef_mtx, ildata, endValues)

        # TODO: Build these arguments. "data" is an object which will
        # get populated by the linearized system during precompute,
        # and compute_jacobian and compute_residual will retrieve
        # stuff.

        # Q: We need to tell the property that the new time is
        # finished, how do we do that?  Part of the higher-level
        # self-consistency?  For the straightforward case where the
        # stepper succeeds, it's not actually required to do this.  If
        # there are multiple sub-problems and we need
        # self-consistency, that's different.
    
        # Then:
        # The UniformDriver will fill in the nextStep attribute.
        print >> sys.stderr, "A2020 stepper exit targeting ", endtime
        print >> sys.stderr, "Endvalues: ", endValues
        for i in range(endValues.size()):
                    u = doublevec.DoubleVec(endValues.size())
                    u.unit(i)
                    print >> sys.stderr, i, " : ", endValues.dot(u)
        return timestepper.StepResult(endTime=endtime,
                                      endValues=endValues,
                                      linsys=linsys)
        


def _asymmetricIC(subproblem, linsys):
    # Incremental problems are quasi-static and only involve
    # the K matrix.  If it's asymmetric, then the problem is,
    # nothing else matters.
    return (subproblem.matrix_symmetry_K == symstate.ASYMMETRIC)

class IncrementalNLFuncs(object):
    def __init__(self, unknowns):
        self.unknowns = unknowns

    def precompute(self, data, values, solver):
        # debug.fmsg("requireJacobian=", solver.needsJacobian(),
        #            "requireResidual=", solver.needsResidual())
        data.subproblem.time_stepper.set_unknowns_part('K', data.linsys, values,
                                                       self.unknowns)
        # This step puts the values into the mesh.
        data.subproblem.installValues(data.linsys, self.unknowns, data.time)
        data.linsys = data.subproblem.make_linear_system(data.time, data.linsys)

    def compute_residual(self, data, soln, nlsolver):
        # debug.fmsg()
        return data.linsys.static_residual_ind_part('K')

    def compute_jacobian(self, data, nlsolver):
        # debug.fmsg()
        return data.linsys.J_submatrix('K', 'K')

    def compute_linear_coef_mtx(self, data, nlsolver):
        # debug.fmsg()
        return data.linsys.K_submatrix('K', 'K')

class IncrementalNLData(object):
    def __init__(self,subproblem,linsys,time):
        self.subproblem = subproblem
        self.linsys = linsys
        self.time = time
        
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
