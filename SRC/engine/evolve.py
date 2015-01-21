# -*- python -*-
# $RCSfile: evolve.py,v $
# $Revision: 1.41.2.7 $
# $Author: langer $
# $Date: 2014/10/09 02:50:29 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

import sys

from ooflib.SWIG.common import progress
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.common import utils
from ooflib.common.IO import reporter
from ooflib.engine import meshstatus

maxconsistencysteps = 100 # Can be altered via commands in meshmenu.py.

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# evolve is called by OOF.Mesh.Solve, after acquiring the Mesh's write
# lock.

linsys_dict = {} # SubProblemContext => LinearizedSystem

def evolve(meshctxt, endtime):
    global linsys_dict
    starttime = meshctxt.getObject().latestTime()

    # We're solving a static problem if endtime is the same as the
    # current time, or if there are no non-static steppers and output
    # is requested at at single time.
    staticProblem = (starttime == endtime
                     or (not meshctxt.timeDependent()
                         and meshctxt.outputSchedule.isSingleTime()))
    # "continuing" is true if we're continuing an earlier time
    # evolution, in which case we can assume that all Fields have
    # their correct initial values. "continuing" is never true for
    # static problems.
    continuing = (not staticProblem and
                  isinstance(meshctxt.status, meshstatus.Solved))

    targettime = endtime

    if starttime > endtime:
        raise ooferror2.ErrSetupError("End time must not precede current time.")

    meshctxt.solver_precompute(solving=True)

    meshctxt.setStatus(meshstatus.Solving())
    meshctxt.timeDiff = endtime - starttime # used to get next endtime in GUI

    # Make sure that the starting point has been cached.
    ## TODO OPT: Is it necessary to call cacheCurrentData here?
    meshctxt.restoreLatestData()
    meshctxt.cacheCurrentData()
    meshctxt.releaseLatestData()

    meshctxt.outputSchedule.reset(starttime, continuing)
    prog = ProgressData(starttime, endtime,
                        progress.getProgress("Solving", progress.DEFINITE))
    try:
        # Get an ordered list of subproblems to be solved.  First,
        # create tuples containing a subproblem and its solveOrder.
        subprobctxts = [(s.solveOrder, s) for s in meshctxt.subproblems()
                       if s.time_stepper is not None and s.solveFlag]
        subprobctxts.sort()     # sort by solveOrder
        subprobctxts = [s[1] for s in subprobctxts] # strip solveOrder

        # Initialize statistics.
        for subp in subprobctxts:
            subp.resetStats()

        if not continuing:
            # Initialize static fields in all subproblems.  For static
            # problems, this computes the actual solution.
            try:
                linsys_dict = initializeStaticFields(subprobctxts, starttime,
                                                     prog)
                # Initial output comes *after* solving static fields.
                # For fully static problems, this is the only output.
                _do_output(meshctxt, starttime)
            except ooferror2.ErrInterrupted:
                raise
            except ooferror2.ErrError, exc:
                meshctxt.setStatus(meshstatus.Failed(exc.summary()))
                raise
            except Exception, exc:
                meshctxt.setStatus(meshstatus.Failed(`exc`))
                raise

        if staticProblem:
            meshctxt.setStatus(meshstatus.Solved())
            meshctxt.setCurrentTime(endtime, None)
            return

        time = starttime
        if continuing:
            delta = meshctxt.solverDelta
        else:
            delta = None
        lasttime = None

        # Loop over output times
        for t1 in meshctxt.outputSchedule.times(endtime):
            if t1 == lasttime:
                raise ooferror2.ErrSetupError("Time step is zero!")
            # If t1 <= starttime, there's no evolution to be done, and
            # any output at t1==starttime has already been done after
            # static initialization. 
            if t1 - starttime > max(t1, starttime)*10.*utils.machine_epsilon:
                if t1 > endtime:
                    t1 = endtime
                if delta is None:
                    delta = min(
                        [subp.time_stepper.initial_stepsize(t1-starttime)
                         for subp in subprobctxts])
                try:
                    time, delta, linsys_dict = evolve_to(
                        meshctxt, subprobctxts,
                        time=time, endtime=t1, delta=delta, prog=prog,
                        linsysDict=linsys_dict)
                except ooferror2.ErrInterrupted:
                    # Interruptions shouldn't raise an error dialog
                    debug.fmsg("Interrupted!")
                    meshctxt.setStatus(meshstatus.Failed(
                            "Solution interrupted."))
                    break
                meshctxt.solverDelta = delta
                if time < t1:
                    meshctxt.setStatus(meshstatus.Failed(
                            "Solver failed to reach the target time."))
                    raise ooferror2.ErrSetupError(
                        "Failed to reach target time. target=%s, actual=%s"
                        % (t1, time))
                if not meshctxt.outputSchedule.isConditional():
                    # If there are conditional outputs, _do_output was
                    # already called by evolve_to().
                    _do_output(meshctxt, t1)
                if t1 == endtime:
                    meshctxt.setStatus(meshstatus.Solved())
                    break
            # end if t1 > starttime
            lasttime = t1
        # end loop over output times
    finally:
        meshctxt.solver_postcompute()
        meshctxt.pause_writing()
        meshctxt.outputSchedule.finish()
        meshctxt.resume_writing()
        prog.finish()
        for subp in subprobctxts:
            if len(subprobctxts) == 1:
                head = "--"
            else:
                head = "-- Subproblem %s --" % subp.name()
            subp.solverStats.report(head, reporter.fileobj)
            reporter.report("Matrices were built", subp.newMatrixCount,
                            "time%s." % ("s"*(subp.newMatrixCount!=1)))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Solve for the static fields in each subproblem.  If the subproblem's
# stepper is second order, *also* solve for the first order fields
# (those with 1st time derivatives but not second).  Do this
# self-consistently if there is more than one subproblem.

# Static field initialization works via a multiple dispatch
# scheme,like this:

# The initializeStaticFields function in this file calls each
# SubProblem's initializeStaticFields method, which uses its
# computeStaticFields method to compute the field values, and then
# stores them in the Mesh's DoFs.  computeStaticFields dispatches the
# call through the subproblem's nonlinear solver to determine whether
# or not it should peform a linear or nonlinear calculation.

def initializeStaticFields(subprobctxts, time, prog):
    stepno = 0                  # self-consistency loop counter
    prevresults = {}
    consistent = False
    linsysDict = {}
    for subproblem in subprobctxts:
        # This is the first call to make_linear_system for each
        # subproblem.
        linsysDict[subproblem] = lsys = subproblem.make_linear_system(
            time, None)
        subproblem.startStep(lsys, time) # sets subproblem.startValues
        subproblem.cacheConstraints(lsys, time)

    while (stepno < maxconsistencysteps and not consistent
           and not prog.stopped()):
        stepno += 1
        for subproblem in subprobctxts:
            newconstraints = True
            while newconstraints and not prog.stopped():
                subproblem.initializeStaticFields(linsysDict[subproblem])
                subproblem.solutiontimestamp.increment()
                newconstraints = subproblem.applyConstraints(
                    subproblem.startValues, time)
                # TODO: What happens if more dofs are added?
        # end loop over subprobctxts
        consistent = True
        if len(subprobctxts) > 1:
            # Check self-consistency
            for subproblem in subprobctxts:
                prev = prevresults.get(subproblem, None)
                consistent = (consistent and (prev is not None) and
                              subproblem.cmpDoF(prev, subproblem.startValues))
                prevresults[subproblem] = subproblem.startValues.clone()
        if not consistent:
            for subproblem in subprobctxts:
                subproblem.restoreConstraints()
    # end consistency loop

    if not prog.stopped() and not consistent:
        raise ooferror2.ErrConvergenceFailure(
            "Static self-consistency loop", maxconsistencysteps)
    return linsysDict

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# evolve_to takes as many steps as it needs to advance a quasistatic
# or dynamic problem from time to endtime.  It runs the outputs iff
# there are any conditional outputs.

def evolve_to(meshctxt, subprobctxts, time, endtime, delta, prog,
              linsysDict=None):
    ## debug.fmsg("--------------- time=%g endtime=%g delta=%s"
    ##            % (time, endtime, delta))
    # subprobctxts is a list of SubProblemContexts.
    # delta is an initial suggested stepsize.
    # prog is a Progress object.
    assert endtime > time
    mindelta = None
    if linsysDict is None:
        linsysDict = {}
    starttime = time
    startdelta = delta
    truncated_step = False

    try:
        # Main loop.  There is no explicit limit to the number of
        # iterations of this loop.  Instead, the adaptive stepper's
        # nextStepEstimate function raises an ErrTimeStepTooSmall
        # exception if the step size is too small.
        while time < endtime and not prog.stopped():

            # Choose the time step.  If no delta is provide, just to
            # up to endtime.  If delta is provided, go up to the
            # smaller of time+delta and endtime, unless time+delta is
            # within epsilon of endtime, in which case go up to
            # endtime anyway.  This prevents roundoff errors from
            # requiring an extra infinitesimal step to reach endtime.
            #
            # truncated_step indicates whether we're trying to take a
            # step with the full delta or not. If we're not trying,
            # then the suggested time step for the next step may be
            # too small, because the stepper will make a suggestion
            # based on the delta it has (not the delta it wants or the
            # delta it might have at some future time).
            if delta > 0:
                if time + delta > endtime:
                    targettime = endtime
                    truncated_step = True
                else:           # time + delta <= endtime
                    targettime = time + delta
                    if (endtime-targettime
                        <= 3*endtime*utils.machine_epsilon):
                        targettime = endtime
                    truncated_step = False
            else:               # delta == 0
                targettime = endtime
                truncated_step = False

            for subprob in subprobctxts:
                # Build or update the linearized system at the current
                # time, even if the stepper is fully implicit.  The
                # maps have to be constructed, and they depend on the
                # matrices.
                lsys = subprob.make_linear_system(
                    time, linsysDict.get(subprob, None))
                linsysDict[subprob] = lsys
                subprob.startStep(lsys, time) # sets subprob.startValues
                subprob.cacheConstraints(lsys, time)

            # Iterate over subprobctxts repeatedly until answers are
            # consistent.
            stepno = 0
            prevresults = {}
            newlinsys = {}
            stepTaken = False
            while (stepno < maxconsistencysteps
                   and not (stepTaken or prog.stopped())):
                stepno += 1
                mintime = None  # lowest time attained by any subproblem
                mindelta = None # smallest recommended delta for any subp.
                for subproblem in subprobctxts:
                    newconstraints = True
                    # Take the step from time to targettime and add in
                    # any new constraints encountered.  Do this
                    # repeatedly until there are no changes in the
                    # constraints.
                    while newconstraints and not prog.stopped():
                        # subproblem.nonlinear_solver is a
                        # nonlinearsolver.NonlinearSolverBase
                        # object, whose job it is to call the
                        # appropriate (linear or nonlinear) method of
                        # the subproblem's "time_stepper" object.

                        # subproblem.time_stepper is a StepDriver
                        # object, containing a TimeStepper object.
                        # The StepDriver's [non]linearstep method
                        # calls the TimeStepper's [non]linearstep
                        # method.

                        # The LinearizedSystem must be cloned because
                        # we may need to repeat the step, and stepper
                        # might re-evaluate the LinearizedSystem at an
                        # intermediate or end time.
                        ## TODO TDEP OPT: The cost of the clone can be
                        ## reduced if the LinearizedSystem *doesn't*
                        ## store K_indfree_, etc, or uses
                        ## SparseSubMats for them.
                        lsClone = linsysDict[subproblem].clone()
                        unknowns = subproblem.get_unknowns(lsClone)
                        # Take a timestep.  The return value is a
                        # timestepper.StepResult object.
                        # debug.fmsg("taking step from %g to %g (%g)" %
                        #            (time, targettime, targettime-time))
                        stepResult = subproblem.nonlinear_solver.step(
                            subproblem,
                            linsys=lsClone,
                            time=time,
                            unknowns=unknowns,
                            endtime=targettime)
                        # debug.fmsg("endValues=", stepResult.endValues)
                        if stepResult.ok:
                            # endStep() sets subproblem.endValues
                            assert stepResult.linsys is not None
                            newlinsys[subproblem] = stepResult.linsys
                            subproblem.endStep(linsysDict[subproblem],
                                               stepResult)
                            newconstraints = subproblem.applyConstraints(
                                subproblem.endValues, stepResult.endTime)
                        else:
                            # Don't bother checking constraints if the
                            # step is going to be repeated anyway.
                            newconstraints = False
                    ## End 'while newconstraints' loop.

                    # Keep track of the minimum time achieved and
                    # minimum recommended next step size for all
                    # subproblems.
                    if mintime is None or mintime > stepResult.endTime:
                        mintime = stepResult.endTime
                    if mindelta is None or (stepResult.nextStep is not None
                                            and mindelta > stepResult.nextStep):
                        mindelta = stepResult.nextStep
                ## End loop over subproblems.

                # Check that all subproblems made it to the target
                # time.  If not, try again with a smaller target time.
                if mintime != targettime:
                    assert mindelta is not None
                    targettime = time + mindelta
                    for subproblem in subprobctxts:
                        subproblem.restoreConstraints()
                    continue # goto "while stepno < maxconsistencysteps...

                # All subproblems reached the target time.  Did each
                # get the same answer it got last time?
                consistent= True
                if len(subprobctxts) > 1:
                    for subproblem in subprobctxts:
                        prev = prevresults.get(subproblem, None)
                        consistent = (
                            consistent and (prev is not None) and
                            subproblem.cmpDoF(prev, subproblem.endValues))
                        prevresults[subproblem] = subproblem.endValues.clone()
                if not consistent:
                    for subproblem in subprobctxts:
                        subproblem.restoreConstraints()
                    continue # goto "while stepno < maxconsistencysteps...

                # All subproblems are consistent. Go on to the next time.
                time = targettime
                delta = mindelta
                stepTaken = True
                prog.time(time, delta=mindelta)
                for subproblem in subprobctxts:
                    linsysDict[subproblem] = newlinsys[subproblem]
                    del newlinsys[subproblem]
                    subproblem.solverStats.stepTaken(mindelta, truncated_step)
                    # Copy values at targettime into DoFs.  Set
                    # startValues to current endValues.  Set
                    # subproblem.startTime to current time, and unset
                    # subproblem.endTime.
                    subproblem.moveOn()
                    subproblem.finalizeConstraints(time)
                if truncated_step:
                    meshctxt.setCurrentTime(time, None)
                else:
                    meshctxt.setCurrentTime(time, mindelta)

            ## End of consistency loop.

            if not stepTaken and not prog.stopped():
                raise ooferror2.ErrConvergenceFailure(
                    "Self-consistency loop at t=%s" % time, maxconsistencysteps)
            if meshctxt.outputSchedule.isConditional():
                _do_output(meshctxt, time)

        ## End main loop.

        if prog.stopped():
            raise ooferror2.ErrInterrupted()

    except ooferror2.ErrInterrupted:
        debug.fmsg("Interrupted!")
        meshctxt.setStatus(meshstatus.Failed("Solution interrupted."))
        raise
    except ooferror2.ErrInstabilityError, err:
        debug.fmsg("Instability detected: ", err)
        meshctxt.setStatus(meshstatus.Failed("Solution diverged? "
                                             + err.summary()))
        raise
    except ooferror2.ErrErrorPtr, err:
        debug.fmsg("Caught an ErrError")
        meshctxt.setStatus(meshstatus.Failed(err.summary()))
        raise
    except Exception, exc:
        debug.fmsg("Caught an Exception")
        meshctxt.setStatus(meshstatus.Failed(exc.message))
        raise

    if truncated_step:
        # Since we didn't take a full step, the nextStepEstimate
        # returned by the AdaptiveDriver might be way too small.
        # Reuse the last estimate instead.
        return time, startdelta, linsysDict
    
    return time, mindelta, linsysDict


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# ProgressData just wraps the Progress class so that it can more
# easily convert the time into a fraction of the total time.

class ProgressData:
    def __init__(self, start, end, prog):
        self.start = start
        self.diff = end - start
        self.prog = prog
    def time(self, t, delta=None):
        if self.diff != 0:
            self.prog.setFraction((t-self.start)/self.diff)
        else:
            self.prog.setFraction(1.0)
        if delta is None:
            self.prog.setMessage("time=%s" % t)
        else:
            self.prog.setMessage("time=%13.5g dt=%9.3g" % (t, delta))
    def stopped(self):
        return self.prog.stopped()
    def finish(self):
        self.prog.finish()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def _do_output(meshctxt, time):
    meshctxt.cacheCurrentData()
    meshctxt.pause_writing()
    try:
        switchboard.notify('mesh data changed', meshctxt)
        meshctxt.outputSchedule.perform(time)
    finally:
        meshctxt.resume_writing()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def dumpLinSysRefererrers():
    global linsys
    print >> sys.stderr, "---- dumpLinSysRefererrers ----"
    for lsys in linsys.values():
        print >> sys.stderr, "Referrers for LinearizedSystem", id(lsys)
        debug.dumpReferrers(lsys, 2)


def removeSubProblem(subp):
    # When a SubProblemContext is destroyed, this removes it from
    # linsys_dict, which allows the LinearizedSystem to be destroyed.
    ## TODO: Understand this: for some reason, simply making
    ## linsys_dict a WeakKeyDictionary isn't sufficient.
    global linsys_dict

    # A SubProblemContext that hasn't been solved won't have a
    # LinearizedSystem, so check that it's actually in the dict before
    # deleting it. *Don't* just use try/except KeyError, because the
    # del operation might have side effects that raise a different,
    # more important KeyError.
    if subp in linsys_dict:
        del linsys_dict[subp]
