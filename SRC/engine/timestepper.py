# -*- python -*-
# $RCSfile: timestepper.py,v $
# $Revision: 1.12.2.4 $
# $Author: fyc $
# $Date: 2014/08/06 19:35:43 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import sys

from ooflib.SWIG.engine import ooferror2
from ooflib.SWIG.engine import steperrorscaling
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## StepDriver is a base class for the different ways in which
## single time steps can be combined into a full time evolution:
## Static, Uniform, and Adaptive.

## StaticDriver is defined in staticstep.py, rather than here, to
## avoid an import loop.

class StepDriver(registeredclass.RegisteredClass):
    registry = []
    tip="How to use time steps: dynamically or not at all."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/stepdriver.xml')

    def __init__(self, stepper):
        assert isinstance(stepper, (TimeStepper, QCTimeStepper))
        self.stepper = stepper  # A TimeStepper or QCTimeStepper object
    def derivOrder(self):
        return self.stepper.derivOrder()

    # evaluateBeginning indicates whether or not matrices should be
    # evaluated at the beginning of each time interval.  Steppers
    # that need matrices in the beginning should return True, even if
    # they also required evaluations at other times.  If they require
    # it only at the end, they should return False.
    ## TODO 3.1: What about steppers that require matrix evaluation only
    ## in the middle of a step?
    def evaluateBeginning(self):
        return self.stepper.evaluateBeginning()

    ## require_timederiv indicates whether the stepping method
    ## requires that first order time derivative fields be defined
    ## even if the equations being solved do not contain second order
    ## time derivatives.  Usually this isn't the case.  If it is,
    ## though, the stepper's Registration should contain
    ## 'require_timederiv=True'.
    def require_timederiv_field(self):
        return self.stepper.require_timederiv_field()

    def explicit(self):
        return self.stepper.explicit()

    ## The default linearstep and nonlinearstep methods just call the
    ## TimeStepper's methods.  Subclasses of StepDriver may
    ## override these.
    def linearstep(self, *args, **kwargs):
        return self.stepper.linearstep(*args, **kwargs)
    def nonlinearstep(self, *args, **kwargs):
        return self.stepper.nonlinearstep(*args, **kwargs)

    def n_unknowns(self, linsys):
        return self.stepper.n_unknowns(linsys)
    def get_unknowns(self, linsys, source):
        return self.stepper.get_unknowns(linsys, source)
    def set_unknowns(self, linsys, vals, startvals):
        return self.stepper.set_unknowns(linsys, vals, startvals)
    def get_unknowns_part(self, part, linsys, unknowns):
        return self.stepper.get_unknowns_part(part, linsys, unknowns)
    def set_unknowns_part(self, part, linsys, vals, unknowns):
        return self.stepper.set_unknowns_part(part, linsys, vals, unknowns)
    def get_derivs_part(self, part, linsys, unknowns):
        return self.stepper.get_derivs_part(part, linsys, unknowns)
    def set_derivs_part(self, part, linsys, vals, unknowns):
        return self.stepper.set_derivs_part(part, linsys, vals, unknowns)

    def M_submatrix(self, linsys, rowpart, colpart):
        return self.stepper.M_submatrix(linsys, rowpart, colpart)
    def C_submatrix(self, linsys, rowpart, colpart):
        return self.stepper.C_submatrix(linsys, rowpart, colpart)
    def K_submatrix(self, linsys, rowpart, colpart):
        return self.stepper.K_submatrix(linsys, rowpart, colpart)
    def J_submatrix(self, linsys, rowpart, colpart):
        return self.stepper.J_submatrix(linsys, rowpart, colpart)

    def rhs_ind_part(self, part, linsys):
        return linsys.rhs_ind_part(part)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## TimeStepper is the base class for various ways of taking a single
## time step.  All subclasses must be derived from LinearStepper,
## NonLinearStepper, or both.

## TimeStepper Registrations must have function data member (ie, a
## function which is not a class method) called "asymmetric".  This
## function returns a boolean indicating whether or not the method
## constructs asymmetric matrices.  The SubProblemContext is the only
## argument to the function.  The function can assume that
## matrix_symmetry_* values have been set in the SubProblemContext.
## The function is called by MatrixMethodFactory.

class TimeStepper(registeredclass.RegisteredClass):
    registry = []
    tip="Ways of taking a single time step."
    discussion=xmlmenudump.loadFile("DISCUSSIONS/engine/reg/timestepper.xml")

    def initialize(self, *args):
        pass
    def shortrepr(self):
        return self.__class__.__name__

    # Does the stepper *always* require the time derivative Fields to
    # be defined?
    def require_timederiv_field(self):
        # See if the Registration has a 'require_timederiv' attribute.
        # If it doesn't, or if there's no Registration, then the
        # stepper is assumed not to need time derivative fields unless
        # the equations are second order.
        try:
            return self.getRegistration().require_timederiv
        except:
            return False

    def explicit(self):
        try:
            return self.getRegistration().explicit
        except:
            return False

    # Does the stepper require the linear system to be evaluated at
    # the beginning of the time interval?  Subclasses that need it
    # only at the end should redefine this function.
    def evaluateBeginning(self):
        return True

class LinearStepper(TimeStepper):
    # Subclasses must define linearstep() with arguments:
    #  subproblem
    #  linearizedsystem
    #  time
    #  startValues
    #  endtime
    # It must return a StepResult object.
    pass

class NonLinearStepper(TimeStepper):
    # Subclasses must define nonlinearstep() with arguments:
    #  subproblem
    #  linearizedsystem
    #  time
    #  startValues
    #  endtime
    #  nonlinearSolverMethod
    # It must return a StepResult object.

    def precomputeNL(self, data, values, solver):
        # precomputeNL is called by the nonlinear solver just before
        # it calls compute_residual, compute_jacobian, and/or
        # compute_linear_coef_mtx.  It should compute any common
        # intermediate results needed by those methods. 'data' is an
        # NLData object. 'solver' is a NonlinearSolverBase object.
        # Derived classes may have to redefine this function.
        # debug.fmsg("time=", data.time)
        data.subproblem.installValues(data.linsys, values, data.time)
        data.linsys = data.subproblem.make_linear_system(data.time,
                                                         data.linsys)

# NLData is used to pass data through to the nonlinearsolvers.
# NonLinearStepper subclasses can use this class, derive from it, or
# define their own data container if necessary.

class NLData(object):
    def __init__(self, subproblem, linsys, time):
        # The LinearizedSystem that's passed in as the linsys argument
        # will only be used in NonLinearStepper.precomputeNL to
        # install the initial values.  It will then be
        # recomputed. SubProblemContext.make_linear_system is supposed
        # to be smart about not recomputing things that don't have to
        # be recomputed, so this isn't an expensive operation.  If it
        # becomes expensive, the right place to fix it is in
        # SubProblemContext.  Maybe.
        self.subproblem = subproblem
        self.linsys = linsys
        self.time = time


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## TODO 3.1: CLEANUP This proliferation of dispatch routines for
## LinearizedSystem methods would be greatly simplified if there were
## a class hierarchy for storage schemes for the unknowns, with
## different subclasses for MCK, MCKa, MCKd, etc.  Then the
## timestepper could simply create an UnknownStorage instance and hand
## it to the LinearizedSystem, which would use it to return the
## correct submatrices and subvectors.

class NonStaticStepper(object):
    def rhs_ind_part(self, part, linsys):
        return linsys.rhs_ind_part(part)

    ## TODO 3.1: CLEANUP These rely on the fact that all of the storage
    ## schemes put M, C, and K in the same order.  Like
    ## get_unknowns_part, etc, these functions really ought to be
    ## defined in FirstOrderStepper and SecondOrderStepper, as well as
    ## StaticStepper. If we had an UnknownStorage class, these
    ## functions would be in it, and not here.
    def M_submatrix(self, linsys, rowpart, colpart):
        return linsys.M_submatrix(rowpart, colpart)
    def C_submatrix(self, linsys, rowpart, colpart):
        return linsys.C_submatrix(rowpart, colpart)
    def K_submatrix(self, linsys, rowpart, colpart):
        return linsys.K_submatrix(rowpart, colpart)
    def J_submatrix(self, linsys, rowpart, colpart):
        return linsys.J_submatrix(rowpart, colpart)
    def set_unknowns_part(self, part, linsys, vals, unknowns):
        linsys.set_unknowns_part(part, vals, unknowns)
    def get_unknowns_part(self, part, linsys, unknowns):
        return linsys.get_unknowns_part(part, unknowns)

class FirstOrderStepper(NonStaticStepper):
    def derivOrder(self):
        return 1
    def get_unknowns(self, linsys, source):
        return linsys.get_unknowns_MCKa(source)
    def set_unknowns(self, linsys, vals, dest):
        return linsys.set_unknowns_MCKa(vals, dest)
    def n_unknowns(self, linsys):
        return linsys.n_unknowns_MCKa()
    def n_unknowns_part(self, part, linsys):
        return linsys.n_unknowns_part_MCKa(part)
    def get_derivs_part(self, part, linsys, unknowns):
        return linsys.get_derivs_part_MCKa(part, unknowns)
    def set_derivs_part(self, part, linsys, vals, unknowns):
        linsys.set_derivs_part_MCKa(part, vals, unknowns)
    def get_fields_from_unknowns(self, linsys, unknowns):
        return unknowns
    def n_unknowns(self, linsys):
        return linsys.n_unknowns_MCKa()
    def error_estimation_dofs(self, linsys, unknowns):
        return unknowns
        

class SecondOrderStepper(NonStaticStepper):
    def derivOrder(self):
        return 2
    def get_unknowns(self, linsys, source):
        return linsys.get_unknowns_MCKd(source)
    def set_unknowns(self, linsys, vals, dest):
        return linsys.set_unknowns_MCKd(vals, dest)
    def n_unknowns(self, linsys):
        return linsys.n_unknowns_MCKd()
    def n_unknowns_part(self, part, linsys):
        return linsys.n_unknowns_part_MCKd(part)
    def get_derivs_part(self, part, linsys, unknowns):
        return linsys.get_derivs_part_MCKd(part, unknowns)
    def set_derivs_part(self, part, linsys, vals, unknowns):
        return linsys.set_derivs_part_MCKd(part, vals, unknowns)
    def n_unknowns(self, linsys):
        return linsys.n_unknowns_MCKd()
    def get_fields_from_unknowns(self, linsys, unknowns):
        return linsys.get_fields_from_unknowns_MCKd(unknowns)
    def error_estimation_dofs(self, linsys, unknowns):
        return linsys.error_estimation_dofs_MCKd(unknowns)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## QCTimeStepper is the base class for various ways of taking a
## *single* "quality controlled" time step (using the Numerical
## Recipes term).  It's used as the "stepper" argument for
## AdaptiveDriver constructors.

class QCTimeStepper(registeredclass.RegisteredClass):
    registry = []
    tip='Ways of taking a "Quality Controlled" time step.'
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/qcstepper.xml')
    ## Subclasses must have linearstep and/or nonlinearstep functions
    ## that take the same arguments as the TimeStepper methods, plus a
    ## StepErrorScaling object called "errorscaling".  They should
    ## return the error.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class StepResult(object):
    def __init__(self, endTime=None, endValues=None, nextStep=None,
                 errorEstimate=None, linsys=None):
        self.endTime = endTime
        self.endValues = endValues
        self.nextStep = nextStep
        self.errorEstimate = errorEstimate
        self.linsys = linsys
        self.ok = True          # AdaptiveDriver may set this to False
        

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Subclasses of StepDriver

class AdaptiveDriver(StepDriver):
    def __init__(self, stepper, tolerance, errorscaling, initialstep, minstep):
        self.tolerance = tolerance
        self.errorscaling = errorscaling
        self.initialstep = initialstep
        self.minstep = minstep
        super(AdaptiveDriver, self).__init__(stepper)
    def initial_stepsize(self, delta):
        return self.initialstep or delta
    def shortrepr(self):
        return "Adaptive / " + self.stepper.shortrepr()
    def linearstep(self, subproblem, time, endtime, *args, **kwargs):
        # self.stepper is a QCTimeStepper.  It returns the return
        # value of self.errorscaling.
        result = self.stepper.linearstep(subproblem=subproblem,
                                         time=time, endtime=endtime,
                                         errorscaling=self.errorscaling,
                                         *args, **kwargs)
        return self.nextStepEstimate(time, result)
    def nonlinearstep(self, subproblem, time, endtime, *args, **kwargs):
        result = self.stepper.nonlinearstep(subproblem=subproblem,
                                            time=time, endtime=endtime,
                                            errorscaling=self.errorscaling,
                                            *args, **kwargs)
        return self.nextStepEstimate(time, result)
    def nextStepEstimate(self, time, stepResult):
        dt = stepResult.endTime - time
        assert(dt >= 0)
        maxstep = 5.0*dt        # max size for next step
        # debug.fmsg("dt=", dt, "err=", stepResult.errorEstimate)
        if(stepResult.errorEstimate == 0.0):
            stepResult.nextStep = maxstep
        else:
            ## globfix adjusts the exponent to account for
            ## errorscalings that include a factor of dt (so that the
            ## global error is controlled, not the individual step
            ## error).
            if self.errorscaling.globalscaling():
                globfix = 1
            else:
                globfix = 0
            exponent = 1./(self.stepper.errorOrder()-globfix)
            newstep = dt*((self.tolerance/stepResult.errorEstimate)**exponent)
            # *Don't* simply compare err and tolerance.  If
            # err=tolerance+epsilon, newstep may equal dt by roundoff,
            # and the repeated step will be exactly the same as the
            # previous one. Instead, compare the old endtime with the
            # new endtime, if the step were to be repeated with the
            # new timestep.  This guarantees that the step won't be
            # repeated with an insignificantly different dt.
            if(time + newstep < stepResult.endTime):
                # decrease stepsize and repeat step
                # debug.fmsg("delta delta t=%15g t=%15g dt=%15g not ok" %
                #            (dt-newstep, time, newstep))
                if newstep < self.minstep or time + newstep == time:
                    raise ooferror2.ErrTimeStepTooSmall(newstep)
                # If the error is just slightly more than the
                # tolerance, we'll be making a very small change in
                # the stepsize, and it may take many iterations to
                # make it small enough, so we include an extra factor
                # of 0.9.
                ## TODO 3.1: Get rid of the factor.  It shouldn't be
                ## necessary if the step size adjustment is being done
                ## correctly.
                stepResult.nextStep = 0.9*newstep
                stepResult.endTime = time
                stepResult.ok = False
                # debug.fmsg("BAD decreased step size to", stepResult.nextStep)
            else:        # increase stepsize and go on to next step
                # debug.fmsg("err=%15g t=%15g dt=%15g ok" %
                #            (stepResult.errorEstimate, stepResult.endTime,
                #             min(newstep, maxstep)))
                # debug.fmsg("endValues=", stepResult.endValues)
                stepResult.nextStep = min(newstep, maxstep)
                # debug.fmsg("OK increased step size to", stepResult.nextStep)
                stepResult.ok = True
        return stepResult
        

registeredclass.Registration(
    'Adaptive',
    StepDriver,
    AdaptiveDriver,
    ordering=1,
    params=[
        parameter.FloatParameter(
            'tolerance', 1.e-4, tip="Maximum permissable error."),
        parameter.FloatParameter(
            "initialstep", 0.1, tip="Initial step size."),
        parameter.FloatParameter(
            'minstep', 1.e-5, tip="Minimum time step size."),
        parameter.RegisteredParameter(
            'errorscaling', steperrorscaling.StepErrorScaling,
            value=steperrorscaling.AbsoluteErrorScaling(),
            tip="How to compute the error for each degree of freedom."),
        parameter.RegisteredParameter('stepper', QCTimeStepper,
                                      tip="Time stepping method.")
        ],
    tip="Take variable sized timesteps.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/adaptivedriver.xml')
   )

############

class UniformDriver(StepDriver):
    def __init__(self, stepper, stepsize):
        self.stepsize = stepsize
        super(UniformDriver, self).__init__(stepper)
    def linearstep(self, *args, **kwargs):
        result = self.stepper.linearstep(*args, **kwargs)
        result.nextStep = self.stepsize
        return result
    def nonlinearstep(self, *args, **kwargs):
        result = self.stepper.nonlinearstep(*args, **kwargs)
        result.nextStep = self.stepsize
        return result
    def initial_stepsize(self, delta):
        return self.stepsize or delta
    def shortrepr(self):
        return "Uniform / " + self.stepper.shortrepr()


registeredclass.Registration(
    'Uniform',
    StepDriver,
    UniformDriver,
    ordering=2,
    params=[
        parameter.RegisteredParameter('stepper', TimeStepper,
                                      tip='Time stepping method.'),
        parameter.PositiveFloatParameter('stepsize', 1.0, tip='Time step size.')
            ],
    tip="Take fixed, uniform timesteps.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/uniformdriver.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# "Basic" versions of the drivers don't require users to choose a
# stepping method.  They just have to select Static, Uniform or
# Adaptive, and provide a tolerance and min step size for Adaptive.

class BasicStepDriver(registeredclass.RegisteredClass):
    registry = []
    tip="Ways of taking time steps, with simple options."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/basicdriver.xml')

class BasicStaticDriver(BasicStepDriver):
    def resolve(self, subproblemcontext, existingStepper):
        from ooflib.engine import staticstep
        if isinstance(existingStepper, staticstep.StaticDriver):
            return existingStepper
        return staticstep.StaticDriver()

registeredclass.Registration(
    'Static',
    BasicStepDriver,
    BasicStaticDriver,
    ordering=0,
    tip="Solve a time independent problem.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/basicstatic.xml'))

############

class BasicAdaptiveDriver(BasicStepDriver):
    def __init__(self, tolerance, minstep):
        self.tolerance = tolerance
        self.minstep = minstep
    def resolve(self, subproblemcontext, existingStepper):
        # Return a new AdaptiveDriver object (not a Basic one)
        # appropriate for the given subproblem.  If the
        # existingStepper is still appropriate, return it instead.
        from ooflib.engine import twostep
        from ooflib.SWIG.engine import steperrorscaling
        if subproblemcontext.second_order_fields():
            from ooflib.engine import ss22
            if (isinstance(existingStepper, AdaptiveDriver) and 
                isinstance(existingStepper.stepper , twostep.TwoStep) and
                isinstance(existingStepper.stepper.singlestep, ss22.SS22)):
                return existingStepper
            singlestep = ss22.SS22(theta1=0.5, theta2=0.5)
        else:                   # no second order fields
            from ooflib.engine import euler
            if (isinstance(existingStepper, AdaptiveDriver) and
                isinstance(existingStepper.stepper, twostep.TwoStep) and
                isinstance(existingStepper.stepper.singlestep,
                           euler.CrankNicolson)):
                return existingStepper
            singlestep = euler.CrankNicolson()
        return AdaptiveDriver(
            stepper=twostep.TwoStep(singlestep),
            tolerance=self.tolerance,
            errorscaling=steperrorscaling.AbsoluteErrorScaling(),
            initialstep=0.0,
            minstep=self.minstep)
    def shortrepr(self):
        return "Adaptive"
        
registeredclass.Registration(
    'Adaptive',
    BasicStepDriver,
    BasicAdaptiveDriver,
    ordering=1,
    params=[
        parameter.FloatParameter(
            'tolerance', 1.e-4, tip="Maximum permissable error."),
        parameter.FloatParameter(
            'minstep', 1.e-5, tip="Minimum time step size."),
        ],
    tip="Take variable sized time steps.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/basicadaptive.xml'))

############

class BasicUniformDriver(BasicStepDriver):
    # The BasicUniformDriver chooses SS22 for second order problems
    # and Crank-Nicolson for first order.
    def __init__(self, stepsize):
        self.stepsize = stepsize
    def resolve(self, subproblemcontext, existingStepper):
        # Return a new UniformDriver object (not a Basic one)
        # appropriate for the given subproblem.  If the
        # existingStepper is still appropriate, return it instead.
        if subproblemcontext.second_order_fields():
            from ooflib.engine import ss22
            if (isinstance(existingStepper, UniformDriver) and 
                isinstance(existingStepper.stepper , ss22.SS22)):
                return existingStepper
            return UniformDriver(stepper=ss22.SS22(theta1=0.5, theta2=0.5), 
                                 stepsize=self.stepsize)
        else:
            from ooflib.engine import euler
            if (isinstance(existingStepper, UniformDriver) and
                isinstance(existingStepper.stepper, euler.CrankNicolson)):
                return existingStepper
            return UniformDriver(stepper=euler.CrankNicolson(), 
                                 stepsize=self.stepsize)
    def shortrepr(self):
        return "Uniform"

registeredclass.Registration(
    'Uniform',
    BasicStepDriver,
    BasicUniformDriver,
    ordering=2,
    params=[
        parameter.PositiveFloatParameter('stepsize', 1.0,
                                         tip='Time step size.')
        ],
    tip="Take fixed, uniform time steps.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/basicuniform.xml'))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class BasicStepDriverParameter(parameter.RegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        super(BasicStepDriverParameter, self).__init__(
            name, BasicStepDriver, value, default, tip, auxData)
    
class AdvancedStepDriverParameter(parameter.RegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        super(AdvancedStepDriverParameter, self).__init__(
            name, StepDriver, value, default, tip, auxData)
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# TODO 3.1: Move RKF45 to its own file, and finish writing it.
class RKF45(QCTimeStepper):
    def shortrepr(self):
        return "RKF45"

# registeredclass.Registration(
#      'Runge-Kutta-Fehlberg 4/5',
#      QCTimeStepper,
#      RKF45,
#      ordering=1)

