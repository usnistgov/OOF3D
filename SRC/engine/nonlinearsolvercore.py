# -*- python -*-
# $RCSfile: nonlinearsolvercore.py,v $
# $Revision: 1.9.4.3 $
# $Author: fyc $
# $Date: 2014/07/28 22:14:56 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

## Nonlinear solvers in this file are generic, so that they can be
## used independently of the time stepping and finite element
## machinery.

from ooflib.SWIG.common import doublevec
from ooflib.SWIG.common import progress
from ooflib.SWIG.engine import cnonlinearsolver
from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.engine import matrixmethod

import math

# TODO OPT: MAYBE compute_residual() returns a new vector every time
# it's called.  It might be better for it to fill in an existing
# vector instead.

# TODO 3.1: all the computations of norm, inner product and residual computations
# in this file should be replaced with the continuous version, for example
# the norm |f| is now computed with
#
#    sqrt( \sum_i |f_i|^2 )
#
# It should be
#
#    sqrt( \int |f(x)|^2 dx )
#
# approximated by
#
#    \sum_ij f_i M_ij f_j
#
# where M is the mass matrix defined by M_ij = \int N_i N_j dx.
# This modification is critical to get comparisons right in the case
# of nonuniform discretization.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# The trivial case is just a linear solver.

class NoNLSolver(cnonlinearsolver.CNonlinearSolver):
    def __init__(self):
        cnonlinearsolver.CNonlinearSolver.__init__(self, False)
        # False ==> this is really a linear solver

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Base class for the nontrivial nonlinear solvers.  The derived
# classes must define a 'solve' method.

class NLSolver(cnonlinearsolver.CNonlinearSolver):
    def __init__(self, relative_tolerance, absolute_tolerance,
                 maximum_iterations):
        cnonlinearsolver.CNonlinearSolver.__init__(self, True)
        # True ==> this is really a nonlinear solve
        self.relative_tolerance = relative_tolerance
        self.absolute_tolerance = absolute_tolerance
        self.maximum_iterations = maximum_iterations

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    # Utility functions used by the Newton and Picard derived classes.
    # If there are ever any NLSolver derived classes that
    # *don't* use these methods, the methods should be moved out of
    # the NLSolver class.

    def three_pt_parabola_model(self, s2, s1, f0, f2, f1):
        #
        # This function calculates and returns the minimizer s of the
        # parabola that passes through the three points (0,f0),
        # (s2,f2), (s1,f1).  The returned value is min( max( s,
        # sigma0*s2 ), sigma1*s2 ).  sigma0, sigma1 are internal
        # parameters set to 0.1, 0.5 respectively.  That is, s is
        # constrained to be in the range [0.1*s2, 0.5*s2].
        #

        assert s2 > 0

        sigma0 = .1
        sigma1 = .5

        # Compute coefficients of interpolation polynomial.
        #
        #   p(s) = f0 + (c1 s + c2 s^2)/d1
        #
        #   d1 = (s2 - s1)*s2*s1 < 0
        #
        # So, if c2 > 0 we have negative curvature and we default to s
        # = sigma1 * s.

        c2 = s1 * ( f2 - f0 ) - s2 * ( f1 - f0 )

        if c2 >= 0:
            return sigma1 * s2

        c1 = s2 * s2 * ( f1 - f0 ) - s1 * s1 * ( f2 - f0 )

        s = -0.5 * c1 / c2;

#         if s < sigma0 * s2:   s = sigma0 * s2
#         if s > sigma1 * s2:   s = sigma1 * s2
#         return s
        return min(max(sigma0*s2, s), sigma1*s2)

    def step_from_parabolic_model_with_Armijo(self, data, soln, update,
                                              res_norm0,
                                              precompute, compute_residual):
        #
        # This function chooses the step size s in the nonlinear updates
        #
        #    soln(k+1) = soln(k) + s * update
        #
        # using a parabolic model and the Armijo stopping rule.
        #
        # The parabolic model interpolates
        #
        #    F( soln(k) ),  F( soln(k) + s1*update ),  F( soln(k) + s2*update )
        #
        # to model the trend of the step size s.
        #
        # debug.fmsg("res_norm0=%g"%res_norm0, "norm(soln)=%g" % soln.norm())

        maxiter = 20
        alpha = 1.0e-4;  # used in the stopping criterion for line search iters

        tempSoln = soln.clone()  # allocate vectors tempSoln and residual
        # residual = soln.clone()

        # set the initial step size to 1 and compute the resulting residual
        s = 1.0
        s_prev = 1.0
        s_current = s

        tempSoln = soln + s * update;

        self.requireResidual(True)
        self.requireJacobian(False)
        precompute(data, tempSoln, self)
        residual = compute_residual(data, tempSoln, self)
        res_norm = residual.norm()
        # debug.fmsg("intial tempsoln=", tempSoln)
        # debug.fmsg("initial residual=", residual)
        # debug.fmsg("initial res_norm=", res_norm)

        # the residuals corresponding to three step sizes s=0,s1,s2
        # to be used in estimating a good step size with the parabolic model

        f0_sqr        = res_norm0 * res_norm0
        f_sqr_current = res_norm * res_norm
        f_sqr_prev    = res_norm * res_norm

        i = 0
        while (res_norm >= (1 - alpha*s) * res_norm0) and (i < maxiter):

            # calculate the new step size using the three point parabola model
            if i == 0:
                s = 0.5 * s  # the first step is obtained by bisection
            else:
                s = self.three_pt_parabola_model( s_current, s_prev, f0_sqr,
                                                  f_sqr_current, f_sqr_prev )

            # update the soln with the new step size, update s_prev, s_current
            # debug.fmsg("trying s=", s)
            tempSoln  = soln + s * update
            s_prev    = s_current
            s_current = s

            # update the vectors and matrices and compute the residual
            self.requireResidual(True)
            self.requireJacobian(False)
            precompute(data, tempSoln, self)
            residual = compute_residual(data, tempSoln, self)
            res_norm = residual.norm()

            f_sqr_prev    = f_sqr_current
            f_sqr_current = res_norm * res_norm

            i += 1
            # debug.fmsg("Line search iteration", i, ",  residual =", res_norm)

        # debug.fmsg("Done.  s=%s (n=%d, res_norm0=%g, res_norm=%g)"
        #            % (s, i, res_norm0, res_norm))

        # raise error if line search did not converge in maxiter # of
        # iterations
        if (i == maxiter) and (res_norm > (1-alpha*s)*res_norm0):
           raise ooferror2.ErrConvergenceFailure(
               'Nonlinear solver - step size search', maxiter)

        return s, residual

    #### End of function (step_from_parabolic_model_with_Armijo)

    def choose_step_size(self, data, values, update, res_norm0, precompute,
                         compute_residual):
    #     return backtracking_step(data, values, update, res_norm0, precompute,
    #                              compute_residual)
        return self.step_from_parabolic_model_with_Armijo(
            data, values, update, res_norm0, precompute, compute_residual)


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Newton(NLSolver):
    def __init__(self, *args, **kwargs):
        NLSolver.__init__(self, *args, **kwargs)
        self.requireJacobian(True)
        self.requireResidual(True)
    def shortrepr(self):
        return "Newton"
    def solve(self, matrix_method, precompute, compute_residual,
              compute_jacobian, compute_linear_coef_mtx, data, values):

        # matrix_method is function that takes a matrix A, a rhs b and
        # a vector of unknows x and sets x so that A*x = b.

        # 'data' is user defined object that can be used to pass
        # information from the calling function to the callback
        # functions if necessary.  The callback functions are
        # precompute, compute_residual, and compute_jacobian.

        # precompute will be called before calling compute_residual
        # and compute_jacobian, and should perform any calculations
        # shared by those two functions.  Its arguments are 'data'
        # (the user defined object), 'values' (a DoubleVec containing
        # a trial solution) and 'needJacobian' (a boolean indicating
        # whether or not the Jacobian needs to be recomputed).

        # compute_residual is called only after precompute.  Its
        # arguments are 'data' (the same object that was used for
        # precompute), 'values' (the trial solution), and residual
        # (the resulting vector of residuals).

        # compute_jacobian is also called only after precompute.  It
        # only takes the 'data' argument.

        # TODO OPT: The vectors and matrices computed by
        # compute_residual, compute_jacobian, and
        # compute_linear_coef_mtx can be preallocated here and passed
        # to the functions, instead of being repeatedly reallocated on
        # each function call.

        # debug.fmsg("initial values=", values.norm())
        n = values.size()

        update   = doublevec.DoubleVec(n)

        # compute the residual = -K*startValues + rhs
        self.requireResidual(True)
        self.requireJacobian(True)
        precompute(data, values, self)
        residual = compute_residual(data, values, self)

        res_norm0 = residual.norm() # norm of the initial residual
        res_norm  = res_norm0       # we will keep comparing current residual
                                    # with res_norm0 to judge convergence
        # debug.fmsg("initial residual:", res_norm0)

        prog = progress.getProgress("Newton Solver", progress.LOGDEFINITE)
        target_res = self.relative_tolerance*res_norm0 + self.absolute_tolerance
        if res_norm0 > target_res:
            prog.setRange(res_norm0, target_res)
        try:
            # compute Newton updates while residual is large and
            # self.maximum_iterations is not exceeded
            s = 1.
            i = 0
            while (res_norm > target_res and i < self.maximum_iterations
                   and not prog.stopped()):
                # debug.fmsg("iter =", i, ",  res =", res_norm, " s =", s)
                update.zero()
                # solve for the Newton step:  Jacobian * update = -residual
                J = compute_jacobian(data, self)
                # debug.fmsg("J=\n", J.norm())
                residual *= -1.0
                matrix_method.solve( J, residual, update )
                # debug.fmsg("update=", update.norm())

                # choose step size for the Newton update.  This resets
                # self.requireXXX.
                s, residual = self.choose_step_size(
                    data, values, update, res_norm,
                    precompute, compute_residual)
                # debug.fmsg("s=", s)
                # correct the soln with the Newton update
                values += s * update

                res_norm = residual.norm()
                if res_norm <= target_res:
                    break

                # update the linear system
                self.requireJacobian(True)
                self.requireResidual(True)
                # debug.fmsg("norm updated values=", values.norm())
                precompute(data, values, self)
                # compute the residual
                residual = compute_residual(data, values, self)
                res_norm = residual.norm()
                #debug.fmsg("Current residual: [%s] (%g)" %(residual, res_norm))
                # debug.fmsg("new residual =", res_norm)
                prog.setMessage("%g/%g" % (res_norm, target_res))
                prog.setFraction(res_norm)

                i += 1
                # end of Newton iterations

            if prog.stopped():
                prog.setMessage("Newton solver interrupted")
                #progress.finish()
                raise ooferror2.ErrInterrupted();
        finally:
            prog.finish()
        # raise error if Newton's method did not converge in maximum_iterations
        if i >= self.maximum_iterations and res_norm > target_res:
            raise ooferror2.ErrConvergenceFailure(
                'Nonlinear solver - Newton iterations', self.maximum_iterations)
        # debug.fmsg("final values=", values)
        # debug.fmsg("-------------------")
        return i, res_norm

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Picard(NLSolver):
    def __init__(self, *args, **kwargs):
        NLSolver.__init__(self, *args, **kwargs)
        self.requireJacobian(False)
        self.requireResidual(True)
    def shortrepr(self):
        return "Picard"
    def solve(self, matrix_method, precompute, compute_residual,
              compute_jacobian, compute_linear_coef_mtx, data, values):
        # initialize: set soln = startValues, update = 0
        # debug.fmsg("-----------------------------")
        # debug.fmsg("initial values=", values.norm())
        n = values.size()
        update   = doublevec.DoubleVec(n)
        # residual = doublevec.DoubleVec(n)

        # compute the residual = -K*startValues + rhs
        self.requireResidual(True)
        self.requireJacobian(False)
        precompute(data, values, self)
        residual = compute_residual(data, values, self)

        res_norm0 = residual.norm() # this is the norm of the initial residual
        # debug.fmsg("res_norm0=%g:" % res_norm0)
        res_norm  = res_norm0       # we will keep comparing current residual
                                    # with res_norm0 to judge convergence

        target_res = self.relative_tolerance*res_norm0 + self.absolute_tolerance
        prog = progress.getProgress('Picard Solver', progress.LOGDEFINITE)
        if res_norm > target_res:
            prog.setRange(res_norm0, target_res)

        try:
            # compute Picard updates while residual is large and
            # self.maximum_iterations is not exceeded
            s = 1.0
            i = 0
            while (res_norm > target_res and i < self.maximum_iterations
                   and not prog.stopped()):
                # debug.fmsg("iteration %d" % i)
                update.zero()  # start with a zero update vector

                # solve for the Picard step:  K * update = -residual
                K = compute_linear_coef_mtx(data, self)
                residual *= -1.0

                # debug.fmsg("residual=", residual.norm())
                matrix_method.solve( K, residual, update )
                # debug.fmsg("update=", update.norm())

                # choose step size for the Picard update
                s, residual = self.choose_step_size(
                    data, values, update, res_norm,
                    precompute, compute_residual)
                # debug.fmsg("line search s=", s)

                # correct the soln with the Picard update
                values += s * update
                res_norm = residual.norm()
                if res_norm <= target_res:
                    break

                # update the linear system
                self.requireResidual(True)
                self.requireJacobian(False)
                precompute(data, values, self)

                # compute the residual
                residual = compute_residual(data, values, self)
                res_norm = residual.norm()
                # debug.fmsg("Current residual:", res_norm)
                prog.setMessage("%g/%g" % (res_norm, target_res))
                prog.setFraction(res_norm)

                i = i+1
                # end of Picard iterations

            if prog.stopped():
                prog.setMessage("Picard solver interrupted")
                #prog.finish()
                raise ooferror2.ErrInterrupted()
        finally:
            prog.finish()

        # debug.fmsg("Done: res_norm=%g" % res_norm)
        # raise error if Picard's iterations did not converge in
        # maximum_iterations
        if i >= self.maximum_iterations and res_norm > target_res:
             raise ooferror2.ErrConvergenceFailure(
                 'Nonlinear solver - Picard iterations',
                 self.maximum_iterations)
        return i, res_norm


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Obsolete?

def backtracking_step(data, soln, update, res_norm0, precompute,
                      compute_residual):
    #
    # This function chooses the step size for the updates of
    # the nonlinear solver. Typically the updates of an iterative
    # scheme, such as the Newton's method, are made with unit
    # step size, i.e. s = 1
    #
    #    soln(k+1) = soln(k) + update
    #
    # For purposes of robustness, it is better to use a line
    # search technique that reduces the step size to ensure
    # that the residual is decreased, we choose s such that
    #
    #    soln(k+1) = soln(k) + s * update
    #    norm( F( soln(k+1) ) < norm( F( soln(k) ) )
    #
    # where F(..) denotes the nonlinear functional in
    #    F( soln ) = 0
    #

    maxiter = 20
    s = 2.0
    i = 0

    tempSoln = soln.clone()
    # residual = soln.clone()
    res_norm = 2.0 * res_norm0 # ensures that while-loop iterates at least once

    while (res_norm > res_norm0) and (i < maxiter):

        s /= 2.0  # halve the step size

        # copy current soln to temp and add update with step size
        tempSoln.copy_inplace( soln )
        tempSoln += s * update

        # update the linear system with the current temp soln
        precompute(data, tempSoln, self)

        # compute the residual and its norm
        residual = compute_residual(data, tempSoln, self)
        res_norm = residual.norm()

        i = i+1
#         debug.fmsg("Line search iteration", i, ",  residual =", res_norm)

#     debug.fmsg("Step size =", s,
#                "(%d iterations, initial residual =%g, final residual =%g)"
#                % (i, res_norm0, res_norm))

    # raise error if line search did not converge in maxiter # of iterations
    if (i >= maxiter) and (res_norm > res_norm0):
       raise ooferror2.ErrConvergenceFailure('Nonlinear solver - step size search', maxiter)

    return s;


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# def apply_preconditioner(vector_in, vector_out, matrix_method, subproblem, linearizedsystem):

#     # K = linearizedsystem.K_indfree()
#     # matrix_method.solve( K, vector_in, vector_out )
#     vector_out.copy_inplace( vector_in )



# def nonlin_pcg_solver(matrix_method, subproblem, linearizedsystem,
#                       time, startValues, endtime, endValues,
#                       compute_residual, relTol, absTol, maxiter):

#     linsys = linearizedsystem

#     # max_restart_count specifies when to restart the conjugate directions
#     max_restart_count = math.ceil( math.sqrt( startValues.size() ) ) # sqrt of problem size

#     # initialize soln = startValues, residual allocated here, initialized later
#     soln     = startValues.clone()
#     residual = startValues.clone()  # allocation of residual vector
#     temp_vec = startValues.clone()  # temp vector needed for computation of update

#     # compute the residual, also set update = residual
#     compute_residual( soln, linsys, residual )
#     update   = residual.clone()

#     # compute the preconditioned residual = M^-1 * residual (M is the preconditioner)
#     preconditioned_residual = residual.clone()
#     apply_preconditioner( residual, preconditioned_residual,
#                           matrix_method, subproblem, linsys )

#     # compute the norm of the residual, this will be used for the stopping criterion
#     res_norm0 = residual.norm() # this is the norm of the initial residual
# #     debug.fmsg("Initial residual:", res_norm0)
#     res_norm  = res_norm0       # we will keep comparing current residual
#                                 # with res_norm0 to judge convergence

#     # compute delta_new needed for beta to update the vector 'update'
#     delta_new = residual.dot( update )

#     # compute Picard updates while residual is large and maxiter is not exceeded
#     i = 0
#     restart_count = 0
#     while (res_norm > (relTol * res_norm0 + absTol)) and (i < maxiter):

#         # choose step size for the update
#         s = choose_step_size( subproblem, linsys, soln, update,
#                               res_norm, endtime, compute_residual )

#         # correct the soln with the update
#         soln += s * update

#         # update the linear system
#         subproblem.installValues( linsys, soln, endtime )
#         linsys = subproblem.make_linear_system( endtime, False )

#         # compute the residual
#         compute_residual( soln, linsys, residual )
#         res_norm = residual.norm()
# #         debug.fmsg("Current residual:", res_norm)

#         # update the quantities delta and compute beta for the update vector
#         delta_old = delta_new
#         delta_mid = residual.dot( preconditioned_residual )
#         apply_preconditioner( residual, preconditioned_residual,
#                               matrix_method, subproblem, linsys )
#         delta_new = residual.dot( preconditioned_residual )

#         beta = (delta_new - delta_mid) / delta_old  # Polak-Ribiere beta parameter

#         # check if we need to restart conjugate direction and update accordingly
#         restart_count = restart_count + 1

#         if (restart_count > max_restart_count) or (beta <= 0.):
#             update.copy_inplace( residual )
#             restart_count = 0
#         else:
#             temp_vec.copy_inplace( residual )
#             temp_vec.axpy( beta, update )
#             update.copy_inplace( temp_vec )

#         i = i+1
#         # end of PCG iterations


#     # copy the soln to end values and start values
#     endValues.copy_inplace( soln )
#     startValues.copy_inplace( soln )

#     # raise error if nonlinear PCG did not converge in maxiter # of iterations
#     if (i >= maxiter) and (res_norm > (relTol * res_norm0 + absTol)):
#          raise ooferror2.ErrConvergenceFailure('NL solver - Conjugate Gradient iterations', maxiter)

# #### End of function (nonlin_pcg_solver)
