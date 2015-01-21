# -*- python -*-
# $RCSfile: namedanalysis.py,v $
# $Revision: 1.8.4.4 $
# $Author: langer $
# $Date: 2014/07/17 15:13:23 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Store and retrieve named sets of analysis parameters

from ooflib.SWIG.common import lock
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common import utils
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine.IO import analyze
from ooflib.engine.IO import scheduledoutput
from ooflib.engine.IO import outputdestination

_namedAnalyses = utils.OrderedDict()
namelock = lock.SLock()

class _nameResolver(object):
    # Callable object for creating a unique name for a bulk or
    # boundary analysis.  
    def __init__(self, defaultname):
        self.defaultname = defaultname
    def __call__(self, param, name):
        if param.automatic():
            basename = self.defaultname
        else:
            basename = name
        return utils.uniqueName(basename, 
                                _namedAnalyses.keys())

nameResolver = _nameResolver('analysis')

class NamedAnalysis(object):
    def __init__(self, name, operation, data, domain, sampling):
        self.name = name
        self.operation = operation
        self.data = data
        self.domain = domain
        self.sampling = sampling
        namelock.acquire()
        try:
            _namedAnalyses[name] = self
        finally:
            namelock.release()
    def start(self, meshcontext, time, continuing):
        self.domain.set_mesh(meshcontext.path())
        self.sampling.make_samples(self.domain)
    def perform(self, namedoutput, meshcontext, time, destination):
        self.domain.set_mesh(meshcontext.path())
        self.domain.read_lock()
        try:
            self.operation(time, self.data, self.domain, self.sampling,
                           destination)
        finally:
            self.domain.read_release()
    def finish(self, meshcontext):
        self.domain.set_mesh(None)

    def printHeaders(self, destination):
        from ooflib.engine.IO import analyzemenu
        analyzemenu.printHeaders(destination, self.operation, self.data,
                                     self.domain, self.sampling)

    def destroy(self):
        namelock.acquire()
        try:
            del _namedAnalyses[self.name]
        finally:
            namelock.release()

def getNamedAnalysis(name):
    return _namedAnalyses[name]

def analysisNames():
    return _namedAnalyses.keys()

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

def findNamedAnalysis(operation, data, domain, sampling):
    for name, analysis in _namedAnalyses.items():
        if (analysis.operation == operation and
            analysis.data == data and
            analysis.domain == domain and
            analysis.sampling == sampling):
            return name
    return ""

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class AnalysisNamesParameter(parameter.ListOfStringsParameter):
    pass
class AnalysisNameParameter(parameter.StringParameter):
    pass

class NamedAnalysisOutput(scheduledoutput.ScheduledOutput):
    # Performs either Bulk or Bdy analyses
    def __init__(self, analysis):
        self.analysis = analysis # just the name
        self.analysisObj = getNamedAnalysis(analysis)
        scheduledoutput.ScheduledOutput.__init__(self)
    def start(self, meshcontext, time, continuing):
        self.analysisObj.start(meshcontext, time, continuing)
        scheduledoutput.ScheduledOutput.start(self, meshcontext, time,
                                              continuing)
    def perform(self, meshcontext, time):
        self.destination.printHeadersIfNeeded(self)
        self.analysisObj.perform(self, meshcontext, time, self.destination)
    def finish(self, meshcontext):
        self.analysisObj.finish(meshcontext)
        scheduledoutput.ScheduledOutput.finish(self, meshcontext)
    def defaultName(self):
        return self.analysis
    def printHeaders(self, destination):
        self.analysisObj.printHeaders(destination)
    def save(self, datafile, meshctxt):
        # Before saving the ScheduledOutput, make sure the named
        # analysis is in the data file.
        from ooflib.engine.IO import analyzemenu
        analyzemenu.saveAnalysisDef(datafile, self.analysis)
        scheduledoutput.ScheduledOutput.save(self, datafile, meshctxt)

registeredclass.Registration(
    "Named Analysis",
    scheduledoutput.ScheduledOutput,
    NamedAnalysisOutput,
    ordering=3,
    destinationClass=outputdestination.TextOutputDestination,
    params=[
        AnalysisNameParameter(
            "analysis", 
            tip="Name of the analysis operation to perform.  Named analyses can be created on the Analysis and Boundary Analysis Pages.")
        ],
    tip="Use a predefined bulk or boundary Analysis method.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/namedanalysis.xml')
)
        
