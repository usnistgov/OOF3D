# -*- python -*-
# $RCSfile: euler.py,v $
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

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Euler stepping and variants of it.  Most variants are simple
# parametrizations of GeneralizedEuler, but ForwardEuler and
# BackwardEuler are implemented explicitly for efficiency.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class ForwardEuler(timestepper.LinearStepper, timestepper.NonLinearStepper,
                   timestepper.FirstOrderStepper):

    def derivOrder(self):
        return 1

    def errorOrder(self):
        return 2.0

    def shortrepr(self):
        return "Forward Euler"

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

    # def nonlinearstep(self, subproblem, linsys, time, unknowns,
    #                   endtime, nonlinearMethod):
    #     return self.linearstep(subproblem, linsys, time, unknowns, endtime)

# Asymmetry detector for ForwardEuler.  This is identical to
# _asymmetric() in rk.py.

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
    'Forward Euler',
    timestepper.TimeStepper,
    ForwardEuler,
    ordering=0,
    explicit=True,
    tip="Fully explicit first order time stepping.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/euler.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Generalized Euler: everything between Forward Euler and Backward
# Euler.  self.theta is defined in subclasses.

class NLDataGE(timestepper.NLData):
    def __init__(self, subproblem, linsys0, endtime, dt, unknowns, theta):
        self.dt = dt
        self.C = linsys0.C_MCKa()
        # resid0 is the part of the residual that can be computed at
        # startTime, with the linsys0 that's passed into this function.
        # resid0 = -C u_n + (1-theta) dt F(u_n, t)
        self.resid0 = self.C * unknowns
        self.resid0 *= -1.0
        res = linsys0.static_residual_MCKa(unknowns)
        self.resid0.axpy( (1-theta)*dt, res )
        timestepper.NLData.__init__(self, subproblem, linsys0, endtime)


class GeneralizedEuler(timestepper.LinearStepper, timestepper.NonLinearStepper,
                       timestepper.FirstOrderStepper):
    def derivOrder(self):
        return 1
    def errorOrder(self):
        return self.error_order
    def shortrepr(self):
        return "Generalized Euler"

    def linearstep(self, subproblem, linsys, time, unknowns, endtime):
        # C du/dt + K u = f
        # C, K, and f might have explicit time dependence, but don't
        # depend on u.

        # Write du/dt = (u_{n+1}-u_n)/dt,
        # K u = (1-theta) K_n u_n + theta K_{n+1} u_{n+1}
        # f = (1-theta) f_n + theta f_{n+1}

        # (C + dt theta K_{n+1}) u_{n+1} =
        #   (C - dt (1-theta) K_n) u_n + (1-theta) dt f_n + theta dt f_{n+1}

        # Because GeneralizedEuler mixes C and K in the matrix to be
        # solved, it doesn't have to worry that C can be singular,
        # unlike ForwardEuler.  It can work with the full MCKa matrix,
        # and doesn't have to explicitly solve the static equations.

        dt = endtime - time

        # Evaluate quantities at start time.
        K0 = linsys.K_MCKa() # K_n
        f0 = linsys.rhs_MCKa() # f_n
        C = linsys.C_MCKa()

        # Evaluate quantities at endtime, in case of explicit time
        # dependence of rhs_ind or K_eff.
        linsys1 = subproblem.make_linear_system( endtime, linsys )
        K1 = linsys1.K_MCKa() # K_{n+1}
        f1 = linsys1.rhs_MCKa()  # f_{n+1}

        # Compute C + dt theta K_{n+1}, which is the matrix to be solved.
        A = C.clone()
        A.add(self.theta*dt, K1)

        # Compute the rhs of the matrix equation.
        v = (dt*(1.0 - self.theta))*f0
        v.axpy(self.theta*dt, f1) # v = (1-theta) dt f_n + theta dt f_{n+1}
        K0.axpy(-dt*(1-self.theta), unknowns, v) # ... - dt (1-theta) K_n u_n
        C.axpy(1.0, unknowns, v) # ... + C u_n

        subproblem.matrix_method(_asymmetricGE, subproblem).solve(A, v, unknowns)
        return timestepper.StepResult(endTime=endtime, nextStep=dt,
                                      endValues=unknowns, linsys=linsys1)


    def nonlinearstep(self, subproblem, linsys, time, unknowns,
                      endtime, nonlinearMethod):
        # C du/dt + F(u,t) = 0
        # C (u_{n+1}-u_n)/dt + theta F(u_{n+1}, t+dt) + (1-theta)F(u_n, t) = 0
        #  or
        # C u_{n+1} + theta dt F(u_{n+1}, t+dt)
        #         - C u_n + (1-theta)dt F(u_n,t) = 0

        dt = endtime - time

        data = NLDataGE(subproblem, linsys, endtime, dt, unknowns, self.theta)
        endValues = unknowns.clone()
        nonlinearMethod.solve(subproblem.matrix_method(_asymmetricGE,
                                                       subproblem),
                              self.precomputeNL,
                              self.compute_residual, self.compute_jacobian,
                              self.compute_linear_coef_mtx,
                              data, endValues)
        return timestepper.StepResult(endTime=endtime, nextStep=dt,
                                      endValues=endValues, linsys=linsys)

    def compute_residual(self, data, soln, nlsolver):
        residual = data.resid0.clone()
        data.C.axpy( 1.0, soln, residual )
        residual.axpy( self.theta*data.dt,
                       data.linsys.static_residual_MCKa(soln) )
        return residual

    def compute_jacobian(self, data, nlsolver):
        # J2 = C + dt J(soln,t+dt)
        J = data.C.clone()
        J.add( data.dt * self.theta, data.linsys.J_MCKa() )
        return J

    def compute_linear_coef_mtx(self, data, nlsolver):
        # CK = C_eff + dt K_eff(soln,t)
        CK = data.C.clone()
        CK.add( data.dt * self.theta, data.linsys.K_MCKa() )
        return CK

# Asymmetry detector for Generalized Euler.
def _asymmetricGE(subproblem):
    # The matrix is (C + dt theta K), where C and K are C_eff and
    # K_eff if there are second order fields.  K_eff is always
    # asymmetric.
    return (subproblem.second_order_fields() or
            subproblem.matrix_symmetry_C == symstate.ASYMMETRIC or
            subproblem.matrix_symmetry_K == symstate.ASYMMETRIC)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Subclasses of GeneralizedEuler differ only in their theta
# parameters, names, and error_orders.

class CrankNicolson(GeneralizedEuler):
    theta = 0.5
    error_order = 3.0

    def shortrepr(self):
        return "Crank Nicolson"

registeredclass.Registration(
    'Crank-Nicolson',
    timestepper.TimeStepper,
    CrankNicolson,
    tip="Semi-implicit first order time stepping, theta=0.5.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/cranknicolson.xml'),
    ordering=1.1)


class Liniger(GeneralizedEuler):
    theta = 0.878
    error_order = 2.0

    def shortrepr(self):
        return "Liniger"

registeredclass.Registration(
    'Liniger',
    timestepper.TimeStepper,
    Liniger,
    tip="Semi-implicit first order time stepping, theta=0.878.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/liniger.xml'),
    ordering=1.2)


class Galerkin(GeneralizedEuler):
    theta = 2./3.
    error_order = 2.0

    def shortrepr(self):
        return "Galerkin"

registeredclass.Registration(
    'Galerkin',
    timestepper.TimeStepper,
    Galerkin,
    tip="Semi-implicit first order time stepping, theta=2/3.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/galerkin.xml'),
    ordering=1.3)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Backward Euler

class NLDataBE(timestepper.NLData):
    def __init__(self, subproblem, linsys0, endtime, dt, unknowns):
        linsys = subproblem.make_linear_system(endtime, linsys0)
        self.dt = dt
        self.C = linsys.C_MCKa()
        # self.CK = None     # CK = C + dt K0, used by Picard iterations
        self.nonlin_offset = self.C * unknowns
        self.nonlin_offset.scale( -1.0 )
        timestepper.NLData.__init__(self, subproblem, linsys0, endtime)


class BackwardEuler(timestepper.LinearStepper, timestepper.NonLinearStepper,
                    timestepper.FirstOrderStepper):
    def derivOrder(self):
        return 1
    def errorOrder(self):
        return 2.0
    def shortrepr(self):
        return "Backward Euler"
    def evaluateBeginning(self):
        return False

    def linearstep(self, subproblem, linsys, time, unknowns, endtime):
        # C du/dt + K u = f
        # C, K, and f might depend on time explicitly, but not on u
        #
        # Write du/dt = (u_{n+1}-u_n)/dt,  K u = K_{n+1} u_{n+1},  f = f_{n+1}
        #
        # (C + dt K_{n+1}) u_{n+1} = C u_{n} + dt f_{n+1}

        dt = endtime - time

        # Evaluate quantities at endtime.
        linsys1 = subproblem.make_linear_system( endtime, linsys )
        K1 = linsys1.K_MCKa()    # K_{n+1}
        f1 = linsys1.rhs_MCKa()  # f_{n+1}
        C  = linsys1.C_MCKa()

        # Construct  A = C + dt K_{n+1}, which is the matrix to be inverted.
        A = C.clone()
        A.add( dt, K1 )

        # Compute the rhs of the matrix equation.
        v = dt * f1
        C.axpy( 1.0, unknowns, v )

        # Solve the linear system.  unknowns is updated in-place.
        subproblem.matrix_method(_asymmetricGE, subproblem).solve(
            A, v, unknowns )

        return timestepper.StepResult(endTime=endtime, nextStep=dt,
                                      endValues=unknowns, linsys=linsys)


    def nonlinearstep(self, subproblem, linsys, time, unknowns,
                      endtime, nonlinearMethod):
        # C du/dt + F = 0
        # K, and f might depend on time and u explicitly

        # Write du/dt = (u_{n+1}-u_n)/dt,
        # F(u,t) = F( u_{n+1}, t_{n+1} )

        # So we need to solve the following nonlinear eqn for v
        # to obtain u_{n+1}

        # C v + dt F(v,t+dt) - C u_{n} = 0
        dt = endtime - time

        data = NLDataBE(subproblem, linsys, endtime, dt, unknowns)
        endValues = unknowns.clone()
        nonlinearMethod.solve(
            subproblem.matrix_method(_asymmetricGE, subproblem),
            self.precomputeNL,
            self.compute_residual, self.compute_jacobian,
            self.compute_linear_coef_mtx,
            data, endValues)
        return timestepper.StepResult(endTime=endtime, nextStep=dt,
                                      endValues=endValues, linsys=linsys)

    def compute_residual(self, data, soln, nlsolver):
        # residual = C soln + dt static_residual(soln,t+dt) - C unknowns
        residual = data.nonlin_offset.clone() # copy  (- C unknowns)
        residual.axpy( data.dt, data.linsys.static_residual_MCKa(soln) )
        data.C.axpy( 1.0, soln, residual )
        return residual

    def compute_jacobian(self, data, nlsolver):
        # J2 = C + dt J(soln,t+dt)
        J = data.C.clone()
        J.add( data.dt, data.linsys.J_MCKa() )
        return J

    def compute_linear_coef_mtx(self, data, nlsolver):
        # C + dt K(soln,t)
        ## TODO OPT: If K_MCKa is constant, then we can store and
        ## re-use CK.  This should be fixed in other steppers too.
        CK = data.C.clone()
        CK.add(data.dt, data.linsys.K_MCKa())
        return CK

registeredclass.Registration(
    'Backward Euler',
    timestepper.TimeStepper,
    BackwardEuler,
    tip="Fully implicit first order time stepping.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/backwardeuler.xml'),
    ordering=1.0)


