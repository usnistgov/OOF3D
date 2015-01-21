# -*- python -*-
# $RCSfile: pbcparamwidget.py,v $
# $Revision: 1.3.18.3 $
# $Author: langer $
# $Date: 2014/05/15 15:06:15 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import skeletoncontext
from ooflib.engine.IO import pbcparams

# The PBCBooleanWidget is just like a regular BooleanWidget except
# that it's desensitized when the current Skeleton has no periodic
# boundaries.  Its value is False in that case.  It's always in a
# valid state, though.

class PBCBooleanWidget(parameterwidgets.BooleanWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        parameterwidgets.BooleanWidget.__init__(self, param, scope, name,
                                                verbose=verbose)
        self.skelwidget = scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and w.whoclass is skeletoncontext.skeletonContexts)
        if self.skelwidget is None:
            raise ooferror.ErrPyProgrammingError(
                "Can't find WhoWidget for Skeleton")
        self.sbcallback = switchboard.requestCallbackMain(self.skelwidget,
                                                          self.sensitize)
        self.sensitize()
    def cleanUp(self):
        switchboard.removeCallback(self.sbcallback)
        parameterwidgets.BooleanWidget.cleanUp(self)
    def isSkeletonPeriodic(self):
        skelname =  self.skelwidget.get_value()
        try:
            skel = skeletoncontext.skeletonContexts[skelname].getObject()
        except KeyError:
            return False
        if config.dimension() == 2:
            return skel.getPeriodicity(0) or skel.getPeriodicity(1)
        return (skel.getPeriodicity(0) or skel.getPeriodicity(1)
                or skel.getPeriodicity(2))
    def sensitize(self, *args, **kwargs):
        self.gtk.set_sensitive(self.isSkeletonPeriodic())
    def get_value(self):
        debug.mainthreadTest()
        if not self.isSkeletonPeriodic():
            return False
        return parameterwidgets.BooleanWidget.get_value(self)
                
def _makePBCBooleanWidget(param, scope, verbose=False):
    return PBCBooleanWidget(param, scope, name=param.name, verbose=verbose)
            
pbcparams.PBCBooleanParameter.makeWidget = _makePBCBooleanWidget
