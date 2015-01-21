# -*- python -*-
# $RCSfile: ss22.py,v $
# $Revision: 1.11.2.1 $
# $Author: langer $
# $Date: 2013/11/08 20:44:52 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import doublevec
from ooflib.SWIG.engine import ooferror2
from ooflib.SWIG.engine import sparsemat
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import symstate
from ooflib.engine import timestepper

class SS22(timestepper.SecondOrderStepper, timestepper.LinearStepper,
           timestepper.NonLinearStepper):

    def __init__(self, theta1, theta2):
        self.theta1 = theta1
        self.theta2 = theta2

    def errorOrder(self):
        return 3.0

    def shortrepr(self):
        return "SS22"

    def linearstep(self, subprobctxt, linsys, time, unknowns, endtime):
        dt = endtime - time
        ## The matrix equation to be solved (for alpha) is A*alpha=x,
        ## where
        ## A = M + theta1 dt C + 1/2 theta2 dt^2 K
        ## x = -(C + theta1 dt K) adot - K a + rhs

        ## Note that   rhs = -f.
        ## We work with   M (d2/dt2) u + C (d/dt) u + K u = rhs
        ## instead of     M (d2/dt2) u + C (d/dt) u + K u + f = 0

        ## a is the known vector of dofs, adot is its known first time
        ## derivative.  rhs is a weighted average of the right hand sides
        ## over the time interval:
        ## rhs = (1-theta1) rhs(t) + theta1 rhs(t+dt)

        ## Values at t+dt are
        ##    a    <- a + dt adot + 1/2 dt^2 alpha
        ##    adot <- adot + dt alpha

        K = linsys.K_MCK()
        C = linsys.C_MCK()
        M = linsys.M_MCK()

        ## This relies on the Fields and their time derivative Fields
        ## having the same global dof ordering!
        A = M.clone()
        A.add(self.theta1*dt, C)
        A.add(0.5*self.theta2*dt*dt, K)
        A.consolidate()

        x  = linsys.rhs_MCK() # x = rhs(t_n)
        x *= (1.0 - self.theta1)        # x = (1-theta1) rhs(t_n)
        ## Compute the rhs at t = endtime.
        linsys1 = subprobctxt.make_linear_system(endtime, linsys)
        # x = (1-theta1) rhs(t_n) + theta1  rhs(t_{n+1})
        x.axpy(self.theta1, linsys1.rhs_MCK())

        # Separate the field and deriv parts of unknowns
        a    = linsys.get_fields_MCKd(unknowns)
        adot = linsys.get_derivs_MCKd(unknowns)

        K.axpy(-1.0, a, x)               # x = - K a + rhs
        C.axpy(-1.0, adot, x)            # x = -C adot - K a + rhs
        K.axpy(-self.theta1*dt, adot, x) # ... -theta1 dt K adot

        alpha = doublevec.DoubleVec(len(a))
        subprobctxt.matrix_method(_asymmetric, subprobctxt).solve(A, x, alpha)
        
        ## update a and adot, then copy them into endValues
        a.axpy(dt, adot)
        a.axpy(0.5*dt*dt, alpha)
        adot.axpy(dt, alpha)

        endValues = doublevec.DoubleVec(unknowns.size())
        linsys.set_fields_MCKd(a, endValues)
        linsys.set_derivs_MCKd(adot, endValues)

        return timestepper.StepResult(endTime=endtime, nextStep=dt,
                                      endValues=endValues, linsys=linsys)


    def nonlinearstep(self, subproblem, linsys, time, unknowns,
                      endtime, nonlinearMethod):
        # M d2u/dt2 + C du/dt + F(u,t) = 0
        # F might depend on time and u explicitly
        # M and C might depend on time

        dt = endtime - time

        data = NLDataSS22(subproblem, linsys, endtime,
                          dt, unknowns, self.theta1, self.theta2)

        alpha = doublevec.DoubleVec(linsys.n_unknowns_MCK()) # not MCKd

        nonlinearMethod.solve(subproblem.matrix_method(_asymmetric, subproblem),
                              self.precomputeNL,
                              self.compute_residual,
                              self.compute_jacobian,
                              self.compute_linear_coef_mtx,
                              data,
                              alpha)

        # Update a and adot, reusing the storage in data.a0 and data.a0dot.
        data.a0.axpy(dt, data.a0dot)
        data.a0.axpy(0.5*dt*dt, alpha)
        data.a0dot.axpy(dt, alpha)
        endValues = doublevec.DoubleVec(unknowns.size())
        linsys.set_fields_MCKd(data.a0, endValues)
        linsys.set_derivs_MCKd(data.a0dot, endValues)
        return timestepper.StepResult(endTime=endtime, nextStep=dt,
                                      endValues=endValues, linsys=linsys)


    def precomputeNL(self, data, alphas, nlsolver): 
        values = doublevec.DoubleVec(data.linsys.n_unknowns_MCKd())
        data.linsys.set_fields_MCKd(data.a11+(0.5*data.dt*data.dt)*alphas,
                                    values)
        data.linsys.set_derivs_MCKd(data.a0dot + data.dt*alphas, values)

        # Base class precomputeNL computes linsys.
        timestepper.NonLinearStepper.precomputeNL(self, data, values, nlsolver)

        data.M1 = data.linsys.M_MCK()
        data.C1 = data.linsys.C_MCK()

        data.F1 = data.linsys.static_residual_MCK()

        data.Mstar = data.Mstar0.clone()
        data.Mstar.add(self.theta1, data.M1)
        data.Mstar.add(data.dt*self.theta2, data.C1)


    def compute_residual(self, data, soln, nlsolver):
        # soln is the proposed solution from the nonlinear solver
        # routine. It's a set of alphas, not actual field values.

        # residual = M* alpha + C* adot + F*.
        #          = (M0* + M1*) alpha + (C0* + C1*) adot + (F0* + F1*)
        # resid0 = C0* * adot + F0* is already computed
        residual = data.resid0.clone()

        data.Mstar0.axpy(1.0, soln, residual)

        # M1* = self.theta1*data.M1 + (data.dt*self.theta2)*data.C1
        Mstar1 = self.theta1 * data.M1
        Mstar1.add(data.dt*self.theta2, data.C1)
        Mstar1.axpy(1.0, soln, residual) # residual += M1* * alpha

        # Add C1* * adot, using C1* = theta1 * C1.
        data.C1.axpy(self.theta1, data.a0dot, residual)

        # Add F1* = theta1*F1.
        residual.axpy(1-self.theta1, data.linsys.static_residual_MCK())
        return residual

    def compute_jacobian(self, data, nlsolver):
        # DF2 = M* + 1/2 theta1 dt^2 DF(soln, endtime)
        J = data.Mstar.clone()
        J.add(0.5*self.theta1*data.dt*data.dt, data.linsys.J_MCK())
        return J

    def compute_linear_coef_mtx(self, data, nlsolver):
        # K2 = M_star + 0.5 * theta1 * dt^2 * K(soln,t)
        K = data.Mstar.clone()
        K.add( 0.5*self.theta1*data.dt*data.dt, data.linsys.K_MCK() )
        return K


class NLDataSS22(timestepper.NLData):
    def __init__(self, subproblem, linsys, endtime,
                 dt, unknowns, theta1, theta2):
        self.dt = dt
        M0 = linsys.M_MCK()
        C0 = linsys.C_MCK()
        self.a0 = linsys.get_fields_MCKd(unknowns)
        self.a0dot = linsys.get_derivs_MCKd(unknowns)
        self.a11 = self.a0.clone() # a1 to first order, without alpha term
        self.a11.axpy(self.dt, self.a0dot)
        self.Mstar0 = (1-theta1)*M0
        self.Mstar0.add(dt*(theta1-theta2), C0)

        # resid0 is the part of the residual that we can compute
        # without knowing any data at endtime.
        #  = C0star*a0dot + F0star
        self.resid0 = linsys.static_residual_MCK();
        self.resid0 *= (1-theta1)
        C0.axpy(1-theta1, self.a0dot, self.resid0)    # ... + (1-theta)*C0*a0dot

        timestepper.NLData.__init__(self, subproblem, linsys, endtime)

def _asymmetric(subproblem):
    return ((subproblem.second_order_fields() and
            subproblem.matrix_symmetry_M == symstate.ASYMMETRIC)
            or
            subproblem.matrix_symmetry_C == symstate.ASYMMETRIC
            or
            subproblem.matrix_symmetry_K == symstate.ASYMMETRIC)

registeredclass.Registration(
    'SS22',
    timestepper.TimeStepper,
    SS22,
    params=[
        parameter.FloatRangeParameter(
            'theta1', (0.0, 1.0, 0.1), 0.5,
            tip='First moment of the weight function for time averages.'),
        parameter.FloatRangeParameter(
            'theta2', (0.0, 1.0, 0.1), 0.5,
            tip='Second moment of the weight function for time averages.')
        ],
    ordering=3.0,
    require_timederiv = True,
    tip="Zienkowicz and Taylor's SS22 algorithm for solving equations with second order time derivatives.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/ss22.xml'))


