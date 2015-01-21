# -*- python -*-
# $RCSfile: sampleregclassfactory.py,v $
# $Revision: 1.9.4.5 $
# $Author: langer $
# $Date: 2014/11/05 16:54:55 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO.GUI import regclassfactory
from ooflib.engine import analysissample
from ooflib.engine import analysisdomain
from ooflib.engine.IO import analyze

# A special registered class factory for the sampling widget.  It
# notices when the domain and operation change, which can affect which
# samplings are allowed.

# The DataOperation and AnalysisDomain registrations
# both have "sampling" lists, which contain the SampleSet subclasses
# that are allowed.  The RCF includes all SampleSet subclasses
# that are derived from a class in *both* lists.

class SampleRCF(regclassfactory.RegisteredClassFactory):
    def __init__(self, obj=None, title=None, callback=None,
                 fill=0, expand=0, scope=None, name=None, widgetdict={},
                 domainClass=None, operationClass=None, verbose=False,
                 *args, **kwargs):
        self.directness = False

        # domainSampleTypes is the tuple of SampleSet classes
        # compatible with the current AnalysisDomain.
        # operationSampleTypes contains the SampleSet classes
        # compatible with the current data operation.
        self.domainSampleTypes = ()
        self.operationSampleTypes = ()

        regclassfactory.RegisteredClassFactory.__init__(
            self,
            registry=analysissample.SampleSet.registry,
            obj=obj,
            title=title, callback=callback, fill=fill, expand=expand, 
            scope=scope, name=name, widgetdict=widgetdict, verbose=verbose,
            *args, **kwargs)

        self.sbcallbacks = []

        # If the domainClass arg is specified, then this widget will
        # only be used on a particular type of domain, and it won't be
        # necessary to synchronize with a Domain widget.  (The Mesh
        # cross section toolbox sets domainClass.)
        if domainClass is None:
            # Find widget to synch with.
            self.domainWidget = self.findWidget(
                lambda w: (isinstance(w, regclassfactory.RegisteredClassFactory)
                           and w.registry is analysisdomain.Domain.registry))
            assert self.domainWidget is not None
            self.newDomain()
            self.sbcallbacks.append(
                switchboard.requestCallbackMain(self.domainWidget,
                                                self.domainCB))
        else:                   # domainClass was specified
            # Find the registration for the class
            for reg in analysisdomain.Domain.registry:
                if reg.subclass is domainClass:
                    self.domainSampleTypes = reg.sampling
                    break

        # Ditto for the operationClass.
        if operationClass is None:
            self.operationWidget = self.findWidget(
                lambda w: (isinstance(w, regclassfactory.RegisteredClassFactory)
                           and w.registry is analyze.DataOperation.registry))
            assert self.operationWidget is not None
            self.newOperation()
            self.sbcallbacks.append(
                switchboard.requestCallbackMain(self.operationWidget,
                                                self.operationCB))
        else: # operationClass is not None, set directness accordingly
            for reg in analyze.DataOperation.registry:
                if reg.subclass is operationClass:
                    self.directness = reg is analyze.directOutput
                    self.operationSampleTypes = reg.sampling
                    break
        self.refresh(obj)

    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        regclassfactory.RegisteredClassFactory.cleanUp(self)
        
    # The "self.directness" reflects whether or not the output
    # operation requires direct output (i.e. is not statistical).
    # self.domainSampleTypes contains the sample classes that are
    # compatible with the domain, and self.operationSampleTypes
    # contains those compatible with the operation.  Choose a sampling
    # that is compatible with both, and which is direct if the
    # operation is direct.

    def includeRegistration(self, registration):
        return (issubclass(registration.subclass, self.domainSampleTypes) and
                issubclass(registration.subclass, self.operationSampleTypes) and
                registration.direct == self.directness)

    def newDomain(self):
        domain_reg = self.domainWidget.getRegistration()
        if domain_reg:
            self.domainSampleTypes = domain_reg.sampling
        else:
            self.domainSampleTypes = ()

    def domainCB(self, *args):
        # The domain has changed, so the allowed samplings may have
        # changed.
        self.newDomain()
        self.refresh()

    def newOperation(self):
        op_reg = self.operationWidget.getRegistration()
        if op_reg:
            self.operationSampleTypes = op_reg.sampling
            self.directness = op_reg is analyze.directOutput
        else:
            self.operationSampleTypes = ()
            self.directness = False

    def operationCB(self, *args):
        # The output operation has changed, so
        # the allowed samplings may have changed.
        self.newOperation()
        self.refresh()

def _SamplingParameter_makeWidget(self, scope=None, verbose=False):
    return SampleRCF(self.value, name=self.name, scope=scope, verbose=verbose)

analysissample.SamplingParameter.makeWidget = _SamplingParameter_makeWidget
