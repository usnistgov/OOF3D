# -*- python -*-
# $RCSfile: rk.py,v $
# $Revision: 1.6.2.3 $
# $Author: langer $
# $Date: 2014/09/17 21:26:55 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import doublevec
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import xmlmenudump
from ooflib.engine import matrixmethod
from ooflib.engine import symstate
from ooflib.engine import timestepper

class RKBase(timestepper.LinearStepper, timestepper.NonLinearStepper,
             timestepper.FirstOrderStepper):
    def derivOrder(self):
        return 1

    # Linear and nonlinear versions just differ in how they evaluate
    # the static residual part.  The linear version uses K*u-f.  The
    # nonlinear version doesn't.  linearstep and nonlinearstep both
    # call _do_step to do the work, but pass it different functions
    # to compute the residual.

    def linearstep(self, subproblem, linsys, time, unknowns, endtime):
        return self._do_step(subproblem, linsys, time, unknowns,
                                endtime, self._linear_residual)

    def nonlinearstep(self, subproblem, linsys, time, unknowns, endtime,
                      nonlinearMethod):
        return self._do_step(subproblem, linsys, time, unknowns,
                                endtime, self._nonlinear_residual)

    def _linear_residual(self, linsys, unknowns):
        v = linsys.rhs_MCa()
        # K_MCa is really (MCa)x(MCKa), so we can multiply by
        # unknowns, which includes the K part.
        K = linsys.K_MCa()        # really (MCa)x(MCKa)
        K.axpy(-1.0, unknowns, v) # v = (f - K u)
        return v

    def _nonlinear_residual(self, linsys, unknowns):
        return (-1.)*linsys.static_residual_MCa(unknowns)



## Fourth order Runge-Kutta

## For y' = g(t, y):
## y_{n+1} = y_n + (h/6)(k_1 + 2 k_2 + 2 k_3 + k_4) + O(h^5)
## k_1 = g(t_n, y_n)
## k_2 = g(t_n + h/2, y_n + h/2 k_1)
## k_3 = g(t_n + h/2, y_n + h/2 k_2)
## k_4 = g(t_n + h, y_n + h k_3)

## Our eqn is C du/dt + K u = f, so g(t, u) = C^{-1} (f - K u),
## where C, K, and f are effective values arising from reducing second
## order time equations to first order.

class RK4(RKBase):
    def errorOrder(self):
        return 5.0
    def shortrepr(self):
        return "Runge Kutta 4"

    def _do_step(self, subprobctxt, linsys, time, unknowns, endtime, get_res):
        nK = linsys.n_unknowns_part('K') # number of static DoFs
        staticEqns = nK > 0

        dt = endtime - time
        n = unknowns.size() - nK
        halftime = time + 0.5*dt
        
        C = linsys.C_MCa()
        v = get_res(linsys, unknowns)
        # K = linsys.K_MCa()                     # really (MCa)x(MCKa)
        # v = linsys.rhs_MCa() - K*unknowns      # (f - K u)
        k1 = linsys.extract_MCa_dofs(unknowns) # initial guess for k1
        assert k1.size() == n
        subprobctxt.matrix_method(_asymmetric, subprobctxt, linsys).solve(
            C, v, k1)
        if staticEqns:
            linsys.expand_MCa_dofs(k1); # include room for static dofs in k1

        y = unknowns + (0.5*dt)*k1
        subprobctxt.installValues(linsys, y, halftime)
        linsys = subprobctxt.make_linear_system(halftime, linsys)
        if staticEqns:
            subprobctxt.computeStaticFields(linsys, y)
        C = linsys.C_MCa()
        # K = linsys.K_MCa()
        # v = linsys.rhs_MCa() - K*y
        v = get_res(linsys, y)
        k2 = linsys.extract_MCa_dofs(y)
        subprobctxt.matrix_method(_asymmetric, subprobctxt, linsys).solve(
            C, v, k2)
        if staticEqns:
            linsys.expand_MCa_dofs(k2)

        y = unknowns + (0.5*dt)*k2
        subprobctxt.installValues(linsys, y, halftime)
        linsys = subprobctxt.make_linear_system(halftime, linsys)
        if staticEqns:
            subprobctxt.computeStaticFields(linsys, y)
        C = linsys.C_MCa()
        # K = linsys.K_MCa()
        # v = linsys.rhs_MCa() - K*y
        v = get_res(linsys, y)
        k3 = linsys.extract_MCa_dofs(y)
        subprobctxt.matrix_method(_asymmetric, subprobctxt, linsys).solve(
            C, v, k3)
        if staticEqns:
            linsys.expand_MCa_dofs(k3)

        y = unknowns + dt*k3
        subprobctxt.installValues(linsys, y, endtime)
        linsys = subprobctxt.make_linear_system(endtime, linsys)
        if staticEqns:
            subprobctxt.computeStaticFields(linsys, y)
        C = linsys.C_MCa()
        # K = linsys.K_MCa()
        # v = linsys.rhs_MCa() - K*y
        v = get_res(linsys, y)
        k4 = linsys.extract_MCa_dofs(y)
        subprobctxt.matrix_method(_asymmetric, subprobctxt, linsys).solve(
            C, v, k4)
        if staticEqns:
            linsys.expand_MCa_dofs(k4)

        unknowns.axpy(dt/6., k1)
        unknowns.axpy(dt/3., k2)
        unknowns.axpy(dt/3., k3)
        unknowns.axpy(dt/6., k4)
        if staticEqns:
            subprobctxt.installValues(linsys, unknowns, endtime)
            linsys = subprobctxt.make_linear_system(endtime, linsys)
            subprobctxt.computeStaticFields(linsys, unknowns)

        return timestepper.StepResult(endTime=endtime, nextStep=dt,
                                      endValues=unknowns, linsys=linsys)
        
    # def nonlinearstep(self, subproblem, linsys, time, unknowns,
    #                   endtime, nonlinearMethod):
    #     return self.linearstep(subproblem, linsys, time, unknowns, endtime)

# Asymmetry detector.  This is identical in _asymmetricFE() in
# euler.py.

def _asymmetric(subproblem, linsys):
    # If the problem has second order time derivatives, then we'll be
    # using C_eff, which is symmetric if M and C are both symmetric
    # and if C21 is zero.
    #
    # If the problem has no second order time derivatives, we'll just
    # be using C.  M's symstate will be INCONSISTENT and C21 will be
    # empty.
    
    ## TODO 3.1: This calculation more logically belongs in
    ## LinearizedSystem, but it doesn't know the matrix_symmetries.

    return (subproblem.matrix_symmetry_M == symstate.ASYMMETRIC or
            subproblem.matrix_symmetry_C == symstate.ASYMMETRIC or
            linsys.C21_nonempty())

registeredclass.Registration(
    '4th order Runge-Kutta',
    timestepper.TimeStepper,
    RK4,
    ordering=2.1,
    explicit=True,
    tip="Fourth order Runge-Kutta time stepping.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/rk4.xml')
    )

## Second order Runge-Kutta

## y_{n+1} = y_n + h k_2 + O(h^3)
## k_1 = g(t_n, y_n)
## k_2 = g(t_n + h/2, y_n + h/2 k_1)

## g(t, u) = C^{-1} (f - K u)


class RK2(RKBase):
    def errorOrder(self):
        return 3.0
    def shortrepr(self):
        return "Runge Kutta 2"
    def _do_step(self, subprobctxt, linsys, time, unknowns, endtime, get_res):

        nK = linsys.n_unknowns_part('K') # number of static DoFs
        staticEqns = nK > 0

        dt = endtime - time
        n = unknowns.size() - nK

        C = linsys.C_MCa()
        # K = linsys.K_MCa()
        # v = linsys.rhs_MCa() - K*unknowns
        v = get_res(linsys, unknowns)
        k1 = linsys.extract_MCa_dofs(unknowns) # initial guess for k1
        subprobctxt.matrix_method(_asymmetric, subprobctxt, linsys).solve(
            C, v, k1)
        if staticEqns:
            linsys.expand_MCa_dofs(k1)

        y = unknowns + (0.5*dt)*k1
        subprobctxt.installValues(linsys, y, time+0.5*dt)
        linsys = subprobctxt.make_linear_system(time + 0.5*dt, linsys)
        if staticEqns:
            subprobctxt.computeStaticFields(linsys, y)
        C = linsys.C_MCa()
        # K = linsys.K_MCa()
        # v = linsys.rhs_MCa() - K*y
        v = get_res(linsys, y)
        k2 = linsys.extract_MCa_dofs(y) 
        subprobctxt.matrix_method(_asymmetric, subprobctxt, linsys).solve(
            C, v, k2)
        if staticEqns:
            linsys.expand_MCa_dofs(k2)

        unknowns.axpy(dt, k2)
        if staticEqns:
            subprobctxt.installValues(linsys, unknowns, endtime)
            linsys = subprobctxt.make_linear_system(endtime, linsys)
            subprobctxt.computeStaticFields(linsys, unknowns)

        return timestepper.StepResult(endTime=endtime, nextStep=dt,
                                      endValues=unknowns, linsys=linsys)

    def nonlinearstep(self, subprobctxt, linsys, time, unknowns,
                      endtime, nonlinearMethod):
        return self.linearstep(subprobctxt, linsys, time, unknowns, endtime)

registeredclass.Registration(
    '2nd order Runge-Kutta',
    timestepper.TimeStepper,
    RK2,
    tip="Second order Runge-Kutta time stepping.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/rk2.xml'),
    explicit=True,
    ordering=2)
