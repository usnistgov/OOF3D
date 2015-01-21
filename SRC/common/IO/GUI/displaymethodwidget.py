# -*- python -*-
# $RCSfile: displaymethodwidget.py,v $
# $Revision: 1.10.18.2 $
# $Author: langer $
# $Date: 2014/05/08 14:38:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO import display
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import whowidget

# The DisplayMethodParameterWidget is basically a
# RegisteredClassFactory for DisplayMethods, but it only lists those
# methods that are appropriate for the WhoClass specified in the
# associated WhoClassParameterWidget. DisplayMethod Registrations
# contain a "whoclasses" variable which lists the names of the classes
# to which the method applies.

class DisplayMethodParameterWidget(regclassfactory.RegisteredClassFactory):
    def __init__(self, value, scope, name, verbose=False):
        self.whoclasswidget = scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoClassParameterWidget))
        regclassfactory.RegisteredClassFactory.__init__(
            self, display.DisplayMethod.registry, scope=scope, name=name,
            verbose=False)
        if value is not None:
            self.set(value, interactive=0)
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.whoclasswidget,
                                            self.whoChangedCB)
            ]
    def whoChangedCB(self, interactive):
        self.update(self.registry)
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        regclassfactory.RegisteredClassFactory.cleanUp(self)
    def includeRegistration(self, registration):
        return self.whoclasswidget.get_value() in registration.whoclasses

def _DisplayMethodParameter_makeWidget(self, scope, verbose=False):
    return DisplayMethodParameterWidget(self.value, scope=scope, name=self.name,
                                        verbose=verbose)

display.DisplayMethodParameter.makeWidget = _DisplayMethodParameter_makeWidget
