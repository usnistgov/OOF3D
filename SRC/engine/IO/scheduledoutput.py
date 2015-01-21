# -*- python -*-
# $RCSfile: scheduledoutput.py,v $
# $Revision: 1.8.4.5 $
# $Author: langer $
# $Date: 2014/07/08 20:50:54 $

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
from ooflib.common import registeredclass
from ooflib.common.IO import automatic
from ooflib.common.IO import parameter
from ooflib.common.IO import gfxmanager
from ooflib.common.IO import xmlmenudump
from ooflib.engine import analysisdomain
from ooflib.engine import analysissample
from ooflib.engine.IO import analyze
from ooflib.engine.IO import meshparameters
from ooflib.engine.IO import output
from ooflib.engine.IO import outputdestination
import ooflib.engine.mesh
import math
import sys

_noutputs = 0

class ScheduledOutput(registeredclass.RegisteredClass):
    registry = []
    # Subclasses whose destination can't be set by the user should set
    # settableDestination to False.
    settableDestination = True
    tip='Output operations for time evolution.'
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/schedout.xml')
    def __init__(self):
        global _noutputs
        self._name = None
        self.id = _noutputs
        _noutputs += 1
        self.active = True
        self.scheduleType = None
        self.schedule = None
        self.destination = None
        self.started = False
    def name(self):
        return self._name
    def activate(self, active):
        self.active = active
    def __hash__(self):
        return hash(self.id)
    def __eq__(self, other):
        return isinstance(other, ScheduledOutput) and self.id == other.id
    ## __del__ was commented out because it was leading to
    ## OutputDestinations being closed too often in some tests (eg,
    ## solver_test.ElasticTimeSteppers("CNPlaneStrainSaveRestore").
    ## If it's necessary to restore __del__, make sure to fix the
    ## error, and explain here why __del__ is required.
    # def __del__(self):
    #     if self.destination is not None:
    #         self.destination.close()
    def setSchedule(self, schedule, scheduleType):
        self.schedule = schedule
        self.scheduleType = scheduleType
    def deleteSchedule(self):
        self.schedule = None
        self.scheduleType = None
    def setDestination(self, destination):
        if not isinstance(destination, self.getRegistration().destinationClass):
            raise ooferror2.ErrInvalidDestination()
        self.destination = destination
    def deleteDestination(self, meshctxt):
        self.finish(meshctxt)
        self.destination = None
    def fullyDefined(self):
        return (self.destination is not None and self.schedule is not None)
    def setName(self, name):
        self._name = name
    def __iter__(self):
        return self.schedule
    def start(self, meshcontext, time, continuing):
        # start() is called at the beginning of an evolution.  It may
        # be redefined in a derived class, but the new definition
        # should make sure to call the base class method as well.
        self.scheduleType.setOffset(self.schedule, time)
        # if not continuing:
        #     self.destination.rewind()
        self.destination.open()
        self.started = True
    def perform(self, meshcontext, time):
        # perform() is called at each scheduled time.
        pass
    def finish(self, meshcontext):
        # finish() is called when the time evolution is done. 
        if self.started:
            self.started = False
            self.destination.close()
    def defaultName(self):
        # Name used for a ScheduledOutput when the user chooses
        # 'automatic'.
        return self.__class__.__name__
    def clone(self):
        bozo = registeredclass.RegisteredClass.clone(self)
        if self.schedule is not None:
            bozo.setSchedule(self.schedule.clone(), self.scheduleType.clone())
        if self.destination is not None:
            bozo.setDestination(self.destination.clone())
        return bozo

    def save(self, datafile, meshctxt):
        # ScheduledOutputs that use a Named[Bulk,Bdy]Analysis must
        # override this function so that the named analysis is defined
        # first.
        from ooflib.engine.IO import meshIO
        datafile.startCmd(meshIO.meshmenu.Scheduled_Output.New)
        datafile.argument('mesh', meshctxt.path())
        datafile.argument('name', self._name)
        datafile.argument('output', self)
        datafile.argument('scheduletype', self.scheduleType)
        datafile.argument('schedule', self.schedule)
        datafile.argument('destination', self.destination)
        datafile.endCmd()

class ScheduledOutputParameter(parameter.StringParameter):
    pass

###################

class GraphicsUpdate(ScheduledOutput):
    settableDestination = False
    def __init__(self):
        ScheduledOutput.__init__(self)
        self.destination = outputdestination.GfxWindowDestination()
        
    def perform(self, meshcontext, time):
        # Set the displayTime in all graphics windows.
        for gfxwin in gfxmanager.gfxManager.getAllWindows():
            gfxwin.setTimeCB(None, time)
        # Actually redraw
        switchboard.notify("redraw")
    def finish(self, meshcontext):
        switchboard.notify("redraw")
        ScheduledOutput.finish(self, meshcontext)

registeredclass.Registration(
    'Update Graphics',
    ScheduledOutput,
    GraphicsUpdate,
    ordering=0,
    destinationClass=outputdestination.GfxWindowDestination,
    tip="Update all graphics windows",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/gfxupdate.xml'))

###################

class ScheduledAnalysis(ScheduledOutput):
    def __init__(self, data, operation, domain, sampling):
        self.data = data
        self.operation = operation
        self.domain = domain
        self.sampling = sampling
        ScheduledOutput.__init__(self)
    def start(self, meshcontext, time, continuing):
        self.domain.set_mesh(meshcontext.path())
        self.sampling.make_samples(self.domain)
        ScheduledOutput.start(self, meshcontext, time, continuing)
    def perform(self, meshcontext, time):
        self.destination.printHeadersIfNeeded(self)
        self.operation(time, self.data, self.domain, self.sampling,
                       self.destination)
    def finish(self, meshcontext):
        self.domain.set_mesh(None)
        self.sampling.clearSamples()
        ScheduledOutput.finish(self, meshcontext)
    def defaultName(self):
        return "%s//%s" % (self.data.shortrepr(),
                           self.operation.shortrepr())
    def printHeaders(self, destination):
        from ooflib.engine.IO import analyzemenu
        analyzemenu.printHeaders(destination, self.operation, self.data,
                                     self.domain, self.sampling)


registeredclass.Registration(
    'Analysis',
    ScheduledOutput,
    ScheduledAnalysis,
    ordering=0.5,
    destinationClass=outputdestination.TextOutputDestination,
    params=[
        output.ValueOutputParameter(
            'data', tip="The output data source."),
        parameter.RegisteredParameter(
            'operation', analyze.DataOperation,
            tip='What to do to the data.'),
        parameter.RegisteredParameter(
            'domain', analysisdomain.Domain,
            tip="Where on the mesh to compute the data."),
        analysissample.SamplingParameter(
            'sampling', tip="How to sample the domain.")
        ],
    tip="Compute Fields, Fluxes, etc. on the Mesh.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/bulkanalysis.xml')
)

###################

class StepStatistics(ScheduledOutput):
    def __init__(self):
        self.initialized = False
        ScheduledOutput.__init__(self)
    def start(self, meshcontext, time, continuing):
        ScheduledOutput.start(self, meshcontext, time, continuing)
        if not continuing or not self.initialized:
            self.starttime = time
            self.lasttime = time
            self.dt2sum = 0.0
            self.nsteps = 0
            self.minstep = None
            self.maxstep = None
            self.initialized = True
    def perform(self, meshcontext, time):
        dt = time - self.lasttime
        if dt > 0:
            self.lasttime = time
            self.dt2sum += dt*dt
            self.nsteps += 1
            if self.minstep is None or dt < self.minstep:
                self.minstep = dt
            if self.maxstep is None or dt > self.maxstep:
                self.maxstep = dt
    def finish(self, meshcontext):
        if self.nsteps > 0:
            avgstep = (self.lasttime - self.starttime)/self.nsteps
            dev2 = self.dt2sum/self.nsteps - avgstep*avgstep
            if dev2 < 0.0:      # roundoff
                dev2 = 0.0
            self.destination.printHeadersIfNeeded(self)
            print >> self.destination, avgstep, math.sqrt(dev2), \
                self.minstep, self.maxstep, self.nsteps
        ScheduledOutput.finish(self, meshcontext)
    def printHeaders(self, destination):
        destination.comment(
            "average time step, deviation, min step, max step, number of steps")

registeredclass.Registration(
    'Time Step Statistics',
    ScheduledOutput,
    StepStatistics,
    ordering=2,
    destinationClass=outputdestination.TextOutputDestination,
    tip="Print time stepping statistics. For meaningful results, schedule this with Conditional/Every Time.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/stepstats.xml'))


