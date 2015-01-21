# -*- python -*-
# $RCSfile: twostep.py,v $
# $Revision: 1.10.2.2 $
# $Author: fyc $
# $Date: 2014/07/28 22:16:10 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import sys

from ooflib.SWIG.common import doublevec
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import timestepper

debugcounter = 0

# TwoStep is a QCTimeStepper (Quality Controlled time stepper) that is
# used by AdaptiveDriver.  It takes one timestep and compares the
# result to two half timesteps in order to get an error estimate.

class TwoStep(timestepper.QCTimeStepper):
    def __init__(self, singlestep):
        self.singlestep = singlestep
    # Most TwoStep methods just pass off the work to the underlying
    # stepper.
    def derivOrder(self):
        return self.singlestep.derivOrder()
    def errorOrder(self):
        return self.singlestep.errorOrder()
    def require_timederiv_field(self):
        return self.singlestep.require_timederiv_field()
    def evaluateBeginning(self):
        return self.singlestep.evaluateBeginning()
    def initialize(self, *args):
        self.singlestep.initialize(*args)
    def shortrepr(self):
        return "TwoStep / " + self.singlestep.shortrepr()
    def computeStaticFieldsL(self, *args, **kwargs):
        self.singlestep.computeStaticFieldsL(*args, **kwargs)
    def computeStaticFieldsNL(self, *args, **kwargs):
        self.singlestep.computeStaticFieldsNL(*args, **kwargs)

    def get_unknowns(self, linsys, source):
        return self.singlestep.get_unknowns(linsys, source)
    def set_unknowns(self, linsys, vals, dest):
        return self.singlestep.set_unknowns(linsys, vals, dest)
    def get_derivs_part(self, part, linsys, unknowns):
        return self.singlestep.get_derivs_part(part, linsys, unknowns)
    def set_derivs_part(self, part, linsys, vals, unknowns):
        return self.singlestep.set_derivs_part(part, linsys, vals, unknowns)
    def n_unknowns(self, linsys):
        return self.singlestep.n_unknowns(linsys)
    def get_unknowns_part(self, part, linsys, unknowns):
        return self.singlestep.get_unknowns_part(part, linsys, unknowns)
    def set_unknowns_part(self, part, linsys, vals, unknowns):
        return self.singlestep.set_unknowns_part(part, linsys, vals, unknowns)

    def M_submatrix(self, linsys, rowpart, colpart):
        return self.singlestep.M_submatrix(linsys, rowpart, colpart)
    def C_submatrix(self, linsys, rowpart, colpart):
        return self.singlestep.C_submatrix(linsys, rowpart, colpart)
    def K_submatrix(self, linsys, rowpart, colpart):
        return self.singlestep.K_submatrix(linsys, rowpart, colpart)
    def J_submatrix(self, linsys, rowpart, colpart):
        return self.singlestep.J_submatrix(linsys, rowpart, colpart)

    def rhs_ind_part(self, part, linsys):
        return self.singlestep.rhs_ind_part(part, linsys)

    def linearstep(self, *args, **kwargs):
        v = self._step(stepper=self.singlestep.linearstep, *args, **kwargs)
        return v

    def explicit(self):
        return self.singlestep.explicit()

    def nonlinearstep(self, *args, **kwargs):
        return self._step(stepper=self.singlestep.nonlinearstep,
                          *args, **kwargs)

    def _step(self, subproblem, linsys, time, unknowns,
             endtime, errorscaling, stepper, *args, **kwargs):
        # If stepper is a nonlinear stepper, then kwargs includes
        # nonlinearMethod.
        #
        # errorscaling is a steperrorscaling.StepErrorScaling
        # instance.

        unknownsCopy = unknowns.clone()
        lsCopy = linsys.clone()

        # Take a single step to endtime.
        # debug.fmsg("taking full step")
        result1 = stepper(subproblem, linsys, time, unknowns, endtime,
                          *args, **kwargs)
        # debug.fmsg("full step norm=", result1.endValues.norm(),
        #            "time=", endtime, "n=", len(result1.endValues))

        # Take a half step.
        halftime = 0.5*(time + endtime)
        midresult = stepper(subproblem, lsCopy, time, unknownsCopy, halftime,
                            *args, **kwargs)
        # debug.fmsg("first half step norm=", midresult.endValues.norm(),
        #            "time=", halftime)

        # Take the second half step to endtime.
        subproblem.installValues(lsCopy, midresult.endValues, halftime)
        linsys = subproblem.make_linear_system( halftime, lsCopy )

        result2 = stepper(subproblem, linsys, halftime, midresult.endValues,
                          endtime, *args, **kwargs)
        # debug.fmsg("second half step norm=", result2.endValues.norm(),
        #            "time=", endtime)

        result2.errorEstimate = errorscaling(
            endtime-time,
            self.singlestep.error_estimation_dofs(linsys, unknowns),
            self.singlestep.error_estimation_dofs(linsys, result1.endValues),
            self.singlestep.error_estimation_dofs(linsys, result2.endValues))

        ## TODO MER: recombine single and double step results to get one
        ## higher order?  This should be done *after* error
        ## estimation, if at all, according to NR.

        return result2


registeredclass.Registration(
    'Two Step',
    timestepper.QCTimeStepper,
    TwoStep,
    ordering=0,
    params=[
        parameter.RegisteredParameter(
            'singlestep', timestepper.TimeStepper,
            tip="Method for individual steps.")],
    tip="Compare the results of one big step to two smaller steps, and adjust the step size to keep the difference within the given tolerance.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/twostep.xml')
)

