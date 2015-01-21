# -*- python -*-
# $RCSfile: invariantwidget.py,v $
# $Revision: 1.11.18.5 $
# $Author: langer $
# $Date: 2014/07/15 00:55:54 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.engine import invariant
from ooflib.common import debug
from ooflib.common.IO.GUI import regclassfactory
from ooflib.engine.IO import outputClones
from ooflib.engine.IO.GUI import meshparamwidgets

class InvariantParameterWidgetBase(regclassfactory.RegisteredClassFactory):
    def __init__(self, value, scope, name, verbose=False):
        self.sbcallbacks = []
        regclassfactory.RegisteredClassFactory.__init__(
            self, invariant.InvariantPtr.registry, scope=scope, name=name,
            verbose=verbose)
        if value is not None:
            self.set(value, interactive=0)
    def includeRegistration(self, registration):
        return (self.invariandclass is not None and
                invariant.okInvariant(registration, self.invariandclass))
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        regclassfactory.RegisteredClassFactory.cleanUp(self)
        self.table = None


class InvariantParameterWidget(InvariantParameterWidgetBase):
    def __init__(self, value, scope, name, verbose=False):
        self.invariandwidget = scope.findWidget(
            lambda w: isinstance(w, meshparamwidgets.InvariandWidget))
        self.findInvariand()
        InvariantParameterWidgetBase.__init__(self, value, scope, name,
                                              verbose=verbose)
        self.sbcallbacks.append(switchboard.requestCallbackMain(
            self.invariandwidget, self.invWidgetChanged))
    def findInvariand(self):
        invariand = self.invariandwidget.get_value()
        if invariand is not None:
            self.invariandclass = \
                                invariand.newOutputValue().valuePtr().__class__
        else:
            self.invariandclass = None
    # This function can get an "interactive" argument -- discard it.
    def invWidgetChanged(self, *args):
        self.findInvariand()
        self.update(self.registry)

# When used in an Output, the kind of Invariant to use depends on the
# Output's input, which might not be the scope's invariand.

class InvariantOutputWidget(InvariantParameterWidgetBase):
    def __init__(self, value, scope, name, output, verbose=False):
        self.output = output
        self.invariandclass = None
        self.table = None
        InvariantParameterWidgetBase.__init__(self, value, scope, name,
                                              verbose=verbose)
    def findInvariandClass(self):
        # First, copy the widget values into the params in the output,
        # so that getInvariandClass can use them.
        self.table.get_values()
        self.invariandclass = outputClones.getInvariandClass(self.output)
    def parameterTableXRef(self, table, widgets):
        # Find the widgets that control the Outputs that precede our
        # Output in the pipeline, and request notification when any of
        # them change.
        self.table = table
        inputs = self.output.allInputs()
        for param, widget in zip(table.params, widgets):
            if param.get_data("Output") in inputs:
                self.sbcallbacks.append(switchboard.requestCallbackMain(
                    widget, self.inputsChangedCB))
        self.inputsChangedCB()
    def inputsChangedCB(self, *args):
        self.findInvariandClass()
        self.update(self.registry)


def _InvariantParameter_makeWidget(self, scope, verbose=False):
    if self.get_data("Output"):
        return InvariantOutputWidget(self.value, scope=scope, name=self.name,
                                     output=self.get_data("Output"),
                                     verbose=verbose)
    return InvariantParameterWidget(self.value, scope=scope, name=self.name,
                                    verbose=verbose)

invariant.InvariantParameter.makeWidget = _InvariantParameter_makeWidget
