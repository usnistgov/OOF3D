# -*- python -*-
# $RCSfile: refinementcriterionparamwidget.py,v $
# $Revision: 1.1.2.4 $
# $Author: langer $
# $Date: 2014/05/08 14:39:07 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Special widget for refinement criterions -- has some
# intelligence to know whether its result should be a
# minimumVolume, an Unconditional, a minimumArea or a minimumLength .

from ooflib.common.IO.GUI import regclassfactory
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO.GUI import whowidget
from ooflib.SWIG.engine import crefinementcriterion

class RefinementCriterionParamWidget(regclassfactory.RegisteredClassFactory):
    def __init__(self, value, scope, name, verbose=False):
        self.targetwidget = scope.findWidget(
	    lambda w: isinstance(w, regclassfactory.RegisteredClassFactory) and
	      w.registry is crefinementcriterion.RefinementTargetsPtr.registry)
        regclassfactory.RegisteredClassFactory.__init__(
            self, crefinementcriterion.RefinementCriterion.registry,
            scope=scope, name=name, verbose=verbose)
        if value is not None:
            self.set(value, interactive=0)
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.targetwidget,
                                            self.whoChangedCB)
            ]
    def whoChangedCB(self, interactive):
        self.update(self.registry)
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        regclassfactory.RegisteredClassFactory.cleanUp(self)

    def includeRegistration(self, registration):
	for component in self.targetwidget.getRegistration().components:
	  if component in registration.targets:
	    return True
        return False


def _makeRCWidget(self, scope, verbose=False):
    return RefinementCriterionParamWidget(self.value, scope=scope,
                                          name=self.name, verbose=verbose)

crefinementcriterion.RefinementCriterionParameter.makeWidget = _makeRCWidget
