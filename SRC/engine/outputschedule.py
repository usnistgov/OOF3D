# -*- python -*-
# $RCSfile: outputschedule.py,v $
# $Revision: 1.12.2.5 $
# $Author: langer $
# $Date: 2014/10/03 14:29:57 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import ooferror2
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import utils
from ooflib.common import registeredclass
from ooflib.common.IO import automatic
from ooflib.common.IO import datafile
from ooflib.common.IO import parameter
from ooflib.common.IO import reporter
from ooflib.common.IO import xmlmenudump
import math

################

# The ScheduleType class determines how an output schedule behaves.
# This is separate from the Schedule class because some Schedules can
# work with more than one ScheduleType.

class ScheduleType(registeredclass.RegisteredClass):
    registry = []
    tip="How output Schedules are interpreted."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/scheduletype.xml')

class AbsoluteOutputSchedule(ScheduleType):
    conditional = False
    def setOffset(self, schedule, time0):
        schedule.setOffset(0.0)

registeredclass.Registration(
    'Absolute',
    ScheduleType,
    AbsoluteOutputSchedule,
    ordering=0,
    tip="Output schedule times are absolute.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/absolutesched.xml')
)

class RelativeOutputSchedule(ScheduleType):
    conditional = False
    def setOffset(self, schedule, time0):
        schedule.setOffset(time0)

registeredclass.Registration(
    'Relative',
    ScheduleType,
    RelativeOutputSchedule,
    ordering=1,
    tip="Output schedule times are relative to the start time.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/relativesched.xml')
)
    
class ConditionalOutputSchedule(ScheduleType):
    conditional = True
    def setOffset(self, schedule, time0):
        pass

registeredclass.Registration(
    'Conditional',
    ScheduleType,
    ConditionalOutputSchedule,
    ordering=2,
    tip="Output schedule times are determined on the fly by a given criterion.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/conditionalsched.xml')
)

######################


# The Schedule class determines when scheduled output is produced.
# UnconditionalSchedules determine the output times in advance.
# ConditionalSchedules do it on the fly.
    
class Schedule(registeredclass.RegisteredClass):
    registry = []
    tip="Ways to specify when Scheduled Output will be produced."
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/schedule.xml')
    def __init__(self):
        self.time0 = 0.0
    def reset(self, continuing):
        pass
    def singleTime(self):
        # In subclasses this should return the time if the Schedule
        # contains only a single time, or None if the Schedule
        # contains multiple times.  If it contains a single unknown
        # time (which probably doesn't make sense) it should return
        # None.  This is used to distinguish between static and
        # quasistatic evolutions.
        return None
    def setOffset(self, time0): # adjust for relative vs absolute scheduletypes
        self.time0 = time0

class UnconditionalSchedule(Schedule):
    conditional = False
    def __iter__(self):
        return self

class ConditionalSchedule(Schedule):
    conditional = True

# The OutputScheduleParameter has a widget (defined in
# engine.IO.GUI.schedulewidget) that lists only the Schedules that are
# compatible with the current ScheduleType.

class OutputScheduleParameter(parameter.RegisteredParameter):
    def __init__(self, name, value=None, default=None, tip=None, auxData={}):
        parameter.RegisteredParameter.__init__(self, name,
                                               reg=Schedule,
                                               value=value, default=default,
                                               tip=tip, auxData=auxData)
    def clone(self):
        return self.__class__(self.name, self.value, self.default, self.tip)

#######################

class Once(UnconditionalSchedule):
    def __init__(self, time):
        self.time = time
        self.done = False
        UnconditionalSchedule.__init__(self)
    def reset(self, continuing):
        self.done = False
    def next(self):
        if self.done:
            raise StopIteration
        self.done = True
        return self.time + self.time0
    def singleTime(self):
        return self.time

registeredclass.Registration(
    'Once',
    Schedule,
    Once,
    ordering=1,
    params=[parameter.FloatParameter('time', 0.0, tip='The output time.')],
    tip="Produce output at just one time.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/once.xml'))

class Periodic(UnconditionalSchedule):
    def __init__(self, delay, interval):
        self.delay = delay
        self.interval = interval
        self.count = 0
        UnconditionalSchedule.__init__(self)
    def reset(self, continuing):
        self.count = 0
    def next(self):
        t = self.time0 + self.delay + self.count*self.interval
        self.count += 1
        return t
        
registeredclass.Registration(
    'Periodic',
    Schedule,
    Periodic,
    ordering=0,
    params=[
        parameter.NonNegativeFloatParameter(
            'delay', 0.0, tip='Time before the first output.'),
        parameter.PositiveFloatParameter(
            'interval', 0.0, tip='Time between outputs.')
        ],
    tip="Produce evenly spaced periodic output.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/periodicsched.xml'))


class Geometric(UnconditionalSchedule):
    def __init__(self, timestep, factor):
        self.timestep = timestep
        self.factor = factor
        self.nextstep = timestep
        self.lasttime = None
        UnconditionalSchedule.__init__(self)
    def reset(self, continuing):
        if not continuing:
            self.nextstep = self.timestep
            self.lasttime = None
    def next(self):
        ## TODO 3.1: This doesn't quite do the right thing on the first
        ## step of a continued computation, if the previous step was
        ## truncated to hit the end time exactly.  For example, with
        ## factor=2 and timestep=0.1, the times are 0.1, 0.3, 0.7,
        ## 1.5, etc.  If the end time is 1, the output times will be
        ## 0.1, 0.3, 0.7, and 1.0.  If the solution is continued, the
        ## next time will be 3.1, although it probably should be 1.5.
        if self.lasttime is None:
            self.lasttime = self.time0
        self.lasttime += self.nextstep
        self.nextstep *= self.factor
        debug.fmsg("Geometric returning", self.lasttime)
        return self.lasttime

registeredclass.Registration(
    'Geometric',
    Schedule,
    Geometric,
    ordering=0.5,
    params=[
        parameter.PositiveFloatParameter(
            'timestep', 1.0, tip='Initial timestep.'),
        parameter.PositiveFloatParameter(
            'factor', 2.0,
            tip='Factor by which to increase the timestep on each step.')
        ],
    tip="Increase timestep by a fixed factor on each step.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/geomsched.xml'))


class SpecifiedTimes(UnconditionalSchedule):
    def __init__(self, times):
        self.times = times[:]
        if self.times:
            self.times.sort()
        self.count = 0
        UnconditionalSchedule.__init__(self)
    def reset(self, continuing):
        if not continuing:
            self.count = 0
    def next(self):
        if self.count == len(self.times):
            raise StopIteration
        t = self.times[self.count] + self.time0
        self.count += 1
        return t
    def singleTime(self):
        if len(self.times) == 1:
            return self.times[0] + self.time0
        return None

registeredclass.Registration(
    'Specified Times',
    Schedule,
    SpecifiedTimes,
    ordering=2,
    params=[
        parameter.ListOfFloatsParameter('times', [],
                                        tip="Produce output at these times.")],
    tip="Produce ouput at the specified times.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/specifiedsched.xml')
    )

class EveryTime(ConditionalSchedule):
    def condition(self, meshctxt, time):
        return True

registeredclass.Registration(
    'Every Time',
    Schedule,
    EveryTime,
    ordering=10,
    tip="Produce output at every time step.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/everytime.xml'))

##################################################    

class OutputSchedule(object):
    def __init__(self, meshcontext):
        # outputs is a set of ScheduledOutput objects.  nexttimes is
        # a dictionary, keyed by ScheduledOutput objects, giving the
        # next time that each S.O. should be performed.  When a
        # S.O. has no more scheduled times, it is removed from the
        # dictionary.  After a set of outputs have been performed, the
        # outputs to be performed at the next step are stored in
        # nextoutputs.

        # The order in which outputs are performed is arbitrary.

        self.meshcontext = meshcontext
        self.removeAll()        # initializes self.outputs, etc.
    def nOutputs(self):
        return len(self.outputs)
    def removeAll(self):
        self.outputs = [] # list, so GUI can present them in creation order
        ## Use OrderedSets and OrderedDicts instead of sets and dicts
        ## so that the order of outputs is repeatable, which makes
        ## testing much easier.
        self.nexttimes = utils.OrderedDict() # next time to perform each output
        self.nextoutputs = utils.OrderedSet() # outputs to perform at next time
        self.conditionalOutputs = utils.OrderedSet()
        self.nexttime = None
        self.finished = set()
    def add(self, name, output): 
        output.setName(name)
        self.outputs.append(output)
    def replace(self, name, output, scheduletype, schedule, destination):
        for i, o in enumerate(self.outputs):
            if o.name() == name:
                output.setSchedule(schedule, scheduletype)
                output.setDestination(destination)
                # If the old output was given an automatically
                # generated name, the name must be updated to reflect
                # changes in the output.
                if isinstance(o.name(), automatic.AutomaticName):
                    output.setName(automatic.AutomaticName(
                            self.uniqueName(output.defaultName(), exclude=name)
                            ))
                else:
                    output.setName(name)
                self.outputs[i] = output
                return
        raise ValueError("No such scheduled output: " + name)
    def rename(self, oldname, newname):
        output = self.getByName(oldname)
        newname = self.uniqueName(newname, exclude=oldname)
        # Reassign even if oldname==newname, since one of them may be
        # an AutomaticName.
        output.setName(newname)
    def remove(self, outputname):
        self.outputs.remove(self.getByName(outputname))
    def size(self):
        return len(self.outputs)
    def isConditional(self):
        return len(self.conditionalOutputs) > 0
    def isSingleTime(self):
        # Returns True if all of the outputs operate just once (or not
        # at all), and they do it at the same time.  Used to
        # distinguish between static and quasistatic time evolutions.
        times = [output.schedule.singleTime() for output in self.outputs
                 if output.active and output.fullyDefined()]
        firsttime = None        # first time found in list
        for time in times:
            if time is None:    # singleTime indicated multiple times
                return False
            if firsttime is None:
                firsttime = time
            if time != firsttime:
                return False
        return True
    def getByName(self, name):
        for o in self.outputs:
            if o.name() == name:
                return o
        raise ValueError("No such scheduled output: " + name)
    def uniqueName(self, name, exclude=None):
        return utils.uniqueName(name, self.names(), exclude)
    def names(self):
        return [o.name() for o in self.outputs]
    def reset(self, time0, continuing):
        # Reset all output schedules, and advance them to the first
        # time after time0 (which is the earliest time in the current
        # evolution).
        self.finished.clear()
        self.nexttimes = utils.OrderedDict()
        self.nexttime = None
        self.nextoutputs.clear()
        self.conditionalOutputs.clear()
        for output in self.outputs:
            if (output.active and output.fullyDefined()):
                output.schedule.reset(continuing)
                output.start(self.meshcontext, time0, continuing)
                if output.schedule.conditional:
                    self.conditionalOutputs.add(output)
                else:
                    try:
                        t = roundOffCheck(output.schedule.next(), time0)
                        if continuing:
                            while t <= time0:
                                t = output.schedule.next()
                        else:
                            while t < time0:
                                t = output.schedule.next()
                    except StopIteration:
                        # The schedule has no times in it later than time0.
                        # Just ignore it.
                        pass
                    else:
                        self.nexttimes[output] = t
                        if self.nexttime is None or t < self.nexttime:
                            self.nexttime = t
        self.nextoutputs = utils.OrderedSet(
            [o for (o,t) in self.nexttimes.items() if t == self.nexttime])

    def times(self, endtime):
        if not self.nexttimes:
            self.nexttime = endtime
            yield endtime
        while self.nexttimes:
            self.nexttime = min(self.nexttimes.values()) # min over all Outputs
            self.nextoutputs = utils.OrderedSet(
                [o for (o,t) in self.nexttimes.items() if t == self.nexttime])
            yield self.nexttime
            # Update next times for the outputs that have just been
            # performed.  If output.schedule.next() raises
            # StopIteration, it's finished.
            for output in self.nextoutputs:
                try:
                    self.nexttimes[output] = roundOffCheck(
                        output.schedule.next(), endtime)
                except StopIteration:
                    del self.nexttimes[output]
                    self.finished.add(output)
        # end while self.nexttimes
        if endtime != self.nexttime:
            self.nextoutputs.clear()
            yield endtime
        

    def perform(self, time):
        # perform() can be called before self.nexttime if there are
        # conditional outputs, so we have to check the time here.
        if time == self.nexttime:
            for output in self.nextoutputs:
                # No need to check output.active here.  Only active
                # outputs are in nextoutputs.
                output.perform(self.meshcontext, time)

        for output in self.conditionalOutputs:
            if output.schedule.condition(self.meshcontext, time):
                if output.active:
                    output.perform(self.meshcontext, time)

    def finish(self):
        for output in self.finished:
            output.finish(self.meshcontext)
        for output in self.nexttimes:
            output.finish(self.meshcontext)
        for output in self.conditionalOutputs:
            # Only active outputs are in nexttimes or in finished, but
            # inactive ones may be in conditionalOutputs, so we have
            # to check.
            if output.active:
                output.finish(self.meshcontext)

    def saveAll(self, datafile, meshctxt):
        for output in self.outputs:
            output.save(datafile, meshctxt)


def roundOffCheck(val, target):
    if abs(val - target) < 10.*utils.machine_epsilon*target:
        return target
    return val
