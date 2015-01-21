# -*- python -*-
# $RCSfile: solverstats.py,v $
# $Revision: 1.5.4.2 $
# $Author: langer $
# $Date: 2013/11/08 20:44:51 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.common import debug
import math

class SolverStats(object):
    def __init__(self):
        self.matrixStats = {}
        self.nonlinearStats = NonlinearStats()
        self.stepperStats = StepperStats()
    def matrixSolution(self, size, niters, residual):
        try:
            stats = self.matrixStats[size]
        except KeyError:
            stats = self.matrixStats[size] = MatrixStats(size)
        stats.add(niters, residual)
    def nonlinearSolution(self, niters, residual):
        self.nonlinearStats.add(niters, residual)
    def stepTaken(self, timestep, truncated):
        self.stepperStats.add(timestep, truncated)
    def report(self, title, out):
        print >> out, title
        mstats = self.matrixStats.values()
        mstats.sort(key=MatrixStats.size)
        for ms in mstats:
            ms.report(out)
        self.nonlinearStats.report(out)
        self.stepperStats.report(out)
    def reset(self):
        self.matrixStats = {}
        self.nonlinearStats.reset()
        self.stepperStats.reset()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class IterationStats(object):
    def __init__(self):
        self.reset()
    def reset(self):
        self.ncalls = 0
        self.iters = StatKeeper()
        self.residuals = StatKeeper()
    def add(self, niters, residual):
        self.ncalls += 1
        self.iters.add(niters)
        self.residuals.add(residual)
    def report(self, out):
        if self.ncalls > 0:
            print >> out, self.name(), "statistics"
            print >> out, " # of solutions:", self.ncalls
            print >> out, "     iterations:", self.iters
            print >> out, "       residual:", self.residuals

class MatrixStats(IterationStats):
    name = "Matrix solution"
    def __init__(self, size):
        self._size = size
        IterationStats.__init__(self)
    def size(self):
        return self._size
    def name(self):
        return "%dx%d matrix solution" % (self._size, self._size)

class NonlinearStats(IterationStats):
    def name(self):
        return "Nonlinear solver"

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class StepperStats(object):
    def __init__(self):
        self.reset()
    def reset(self):
        self.nsteps = 0
        self.ntruncated = 0
        self.stepstats = StatKeeper()
        self.untruncatedstepstats = StatKeeper()
    def add(self, timestep, truncated):
        self.nsteps += 1
        if timestep is not None:
            self.stepstats.add(timestep)
        if truncated:
            self.ntruncated += 1
        else:
            if timestep is not None:
                self.untruncatedstepstats.add(timestep)
    def report(self, out):
        if self.nsteps > 0:
            print >> out, "Time step statistics"
            print >> out, "           all steps: n=%d"%self.nsteps,\
                self.stepstats
            if self.ntruncated > 0:
                print >> out, " non-truncated steps: n=%d" \
                    % (self.nsteps-self.ntruncated), self.untruncatedstepstats


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class StatKeeper(object):
    def __init__(self, val=None):
        self.reset()
        if val is not None:
            self.add(val)
    def reset(self):
        self.n = 0
        self.sum = 0
        self.sum2 = 0
        self.min = None
        self.max = None
    def add(self, val):
        self.sum += val
        self.sum2 += val*val
        self.n += 1
        if self.min is None or val < self.min:
            self.min = val
        if self.max is None or val > self.max:
            self.max = val
    def average(self):
        if self.n > 0:
            return self.sum/float(self.n)
    def deviation(self):
        if self.n > 0:
            a = self.average()
            return math.sqrt(self.sum2/float(self.n) - a*a)
    def range(self):
        return (self.min, self.max)
    def __repr__(self):
        if self.n > 1:
            return "average=%s, min=%s, max=%s" % (self.average(), self.min,
                                                   self.max)
        return `self.sum`

