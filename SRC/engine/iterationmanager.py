# -*- python -*-
# $RCSfile: iterationmanager.py,v $
# $Revision: 1.1.2.2 $
# $Author: langer $
# $Date: 2011/10/11 15:06:40 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import progress
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
import math
import sys


class IterationManager(registeredclass.RegisteredClass):
    registry = []
    def update(self, delta, total, rate, count, prog):
        pass

    def goodToGo(self):
        # boolean
        pass
    
    def reportSomething(self, delta, total, rate, count):
        if total:
            reduce = abs(100.0*delta/total)
        else:
            reduce = 0.0
        reporter.report("Iteration %d: E = %10.4e, deltaE=%10.4e (%6.3f%%), Acceptance Rate = %4.1f%%"
                        % (count, total, delta, reduce, 100.*rate))

    def reportNothing(self, count):
        reporter.report("Iteration %d: No attempts made, no nodes moved!"
                        % count)
        
    tip = "Stopping criteria for iterative Skeleton modifiers."

    discussion = """<para>
    <classname>IterationManagers</classname> control the repeated
    application of certain <link
    linkend='RegisteredClass:SkeletonModifier'><classname>SkeletonModifiers</classname></link>,
    such as <xref linkend='RegisteredClass:Anneal'/> and <xref
    linkend='RegisteredClass:Smooth'/>.
    </para>"""

    
class FixedIteration(IterationManager):
    def __init__(self, iterations):
        self.iterations = iterations
        self.count = 0

    def update(self, delta, total, rate, count, prog):
        self.count = count
        # reporting
        if delta is not None and rate is not None:
            self.reportSomething(delta, total, rate, count)
        else:
            self.reportNothing(count)
        prog.setFraction(float(count)/self.iterations)
        prog.setMessage("iteration %d/%d" % (count, self.iterations))
        
    def goodToGo(self):
        if self.count < self.iterations:
            return 1
        else:
            return 0
        
    def get_progressbar_type(self):
        return progress.DEFINITE
    
registeredclass.Registration(
    'Fixed Iterations',
    IterationManager,
    FixedIteration, 0,
    params=[
    parameter.IntParameter('iterations', 5,
                        tip='Number of iterations to perform.  Each node is addressed once per iteration.')],
    tip="Repeat operation a fixed number of times.",
    discussion="""<para>
    Repeat a <link linkend='RegisteredClass:SkeletonModifier'>Skeleton
    modification</link> operation a fixed number of times.
    </para>""")

# Convergence condition candidates:
# 1. Acceptance Rate: Accepted_Nodes/Total_Nodes*100
#    Cheap and convenient but sometimes misleading.
#    If A.R. stays below the specified threshold for a specified number of
#    times, the process stops.

# 2. Energy Reduction Rate: Reduced_Energy/Total_Energy*100
#    Expensive but more accurate.
#    If energy reduction stays below the specified threshold for
#    a specified number of times, the process stops.

class ConditionSelector(registeredclass.RegisteredClass):
    registry = []

    tip = "Stopping criteria for conditional iteration of Skeleton modifiers."
    discussion = """<para>

    When using the <xref
    linkend='RegisteredClass:ConditionalIteration'/> <xref
    linkend='RegisteredClass:IterationManager'/> to iterate a <xref
    linkend='RegisteredClass:SkeletonModifier'/>, the actual stopping
    criterion is specified with an object of the
    <classname>ConditionSelector</classname> class.
    </para>"""

class ReductionRateCondition:
    def reductionRateFailed(self, delta, total):
	if delta is None:
	    return 1
        # delta is negative, if energy is going down
        reduction = -delta/total*100.
        return reduction < self.reduction_rate

reductionRateParam = parameter.FloatRangeParameter(
    'reduction_rate', (0., 100., 0.1), value=0.1, 
    tip="Minimum allowable energy reduction rate as a percentage of the total energy.")

class AcceptanceRateCondition:
    def acceptanceRateFailed(self, rate):
	if rate is None:
	    return 1
        return rate*100. < self.acceptance_rate

acceptanceRateParam = parameter.FloatRangeParameter(
    'acceptance_rate', (0., 100., 0.1), value=7,
    tip='Minimum allowable move acceptance rate as a percentage of the number of movable nodes.'
    )

class Either(ConditionSelector,
             ReductionRateCondition, AcceptanceRateCondition):
    def __init__(self, reduction_rate, acceptance_rate):
        self.reduction_rate = reduction_rate
        self.acceptance_rate = acceptance_rate
    def __call__(self, delta, total, rate, count):
        return self.reductionRateFailed(delta, total) or \
               self.acceptanceRateFailed(rate)
    
registeredclass.Registration(
    'Either',
    ConditionSelector,
    Either, 3,
    params=[acceptanceRateParam, reductionRateParam],
    tip="Iteration stops when either the energy reduction rate or move acceptance rate falls below the given thresholds.",
    discussion="""<para>
    When the <varname>condition</varname> parameter of a <xref
    linkend='RegisteredClass:ConditionalIteration'/> is set to
    <classname>Either</classname>, iteration of a <xref
    linkend='RegisteredClass:SkeletonModifier'/> will stop when either
    the <xref linkend='RegisteredClass:AcceptanceRate'/> or <xref
    linkend='RegisteredClass:ReductionRate'/> criterion is satisfied.
    </para>""")

class Both(ConditionSelector,
           ReductionRateCondition, AcceptanceRateCondition):
    def __init__(self, reduction_rate, acceptance_rate):
        self.reduction_rate = reduction_rate
        self.acceptance_rate = acceptance_rate
    def __call__(self, delta, total, rate, count):
        return self.reductionRateFailed(delta, total) and \
               self.acceptanceRateFailed(rate)
    
registeredclass.Registration(
    'Both',
    ConditionSelector,
    Both, 2,
    params=[reductionRateParam, acceptanceRateParam],
    tip="Iteration stops when both the energy reduction rate and move acceptance rate fall below the given thresholds.",
    discussion="""<para>
    When the <varname>condition</varname> parameter of a <xref
    linkend='RegisteredClass:ConditionalIteration'/> is set to
    <classname>Both</classname>, iteration of a <xref
    linkend='RegisteredClass:SkeletonModifier'/> will stop when both
    the <xref linkend='RegisteredClass:AcceptanceRate'/> or <xref
    linkend='RegisteredClass:ReductionRate'/> criteria are satisfied.
    </para>""")
                 
class ReductionRate(ConditionSelector, ReductionRateCondition):
    def __init__(self, reduction_rate):
        self.reduction_rate = reduction_rate
    def __call__(self, delta, total, rate, count):
        return self.reductionRateFailed(delta, total)
                 
registeredclass.Registration(
    'Energy Reduction Rate',
    ConditionSelector,
    ReductionRate, 1,
    params=[reductionRateParam],
    tip="Iteration stops when the energy reduction rate falls below the given threshold.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/reduction_rate.xml'))

class AcceptanceRate(ConditionSelector, AcceptanceRateCondition):
    def __init__(self, acceptance_rate):
        self.acceptance_rate = acceptance_rate
    def __call__(self, delta, total, rate, count):
        return self.acceptanceRateFailed(rate)
                 
registeredclass.Registration(
    'Acceptance Rate',
    ConditionSelector,
    AcceptanceRate, 0,
    params=[acceptanceRateParam],
    tip="Iteration stops when the move acceptance rate falls below the given threshold.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/acceptance_rate.xml'))

class ConditionalIteration(IterationManager):
    def __init__(self,
                 condition,
                 extra,
                 maximum):
        self.condition = condition
        self.maximum = maximum          # max no. of steps allowed
        self.extra = extra              # allow this many consecutive bad steps
        self.nbad = 0                   # no. of consecutive bad steps
        self.count = 0                  # total no. of steps

    def update(self, delta, total, rate, count, prog):
        self.count = count
        if self.condition(delta, total, rate, count):
            self.nbad += 1
        else:
            self.nbad = 0
        # reporting
        if delta is not None and rate is not None:
            self.reportSomething(delta, total, rate, count)
        else:
            self.reportNothing(count)
        prog.pulse()

    def goodToGo(self):
        return not (self.nbad > self.extra or self.count >= self.maximum)
    def get_progressbar_type(self):
        return progress.INDEFINITE

registeredclass.Registration(
    'Conditional Iteration',
    IterationManager,
    ConditionalIteration, 1,
    params=[
    parameter.RegisteredParameter('condition', ConditionSelector,
                                  tip='Which exit condition to use.'),
    parameter.IntParameter('extra', 0,
                           tip="Number of extra steps to take to ensure that the condition is met."),
    parameter.IntParameter('maximum', 100,
                        tip="Maximum number of iterations, despite the exit condition.")],
    tip='Iteration stops when a given condition is satisfied.',
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/conditional_iteration.xml'))
            
#############################################################
