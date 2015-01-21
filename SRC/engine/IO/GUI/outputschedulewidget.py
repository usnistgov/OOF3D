# -*- python -*-
# $RCSfile: outputschedulewidget.py,v $
# $Revision: 1.2.4.1 $
# $Author: langer $
# $Date: 2014/05/15 15:06:15 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Widget for the ScheduledOutputParameter.  It lets the user choose an
# Output from the ones defined in a Mesh.

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import mesh
from ooflib.engine.IO import scheduledoutput

class ScheduledOutputWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        self.chooser = chooser.ChooserWidget([], callback=self.chooserCB,
                                             name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.chooser.gtk, scope,
                                                  verbose=verbose)
        self.meshwidget = scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and w.whoclass is mesh.meshes)
        assert self.meshwidget is not None
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.meshwidget, self.update),
            switchboard.requestCallbackMain("scheduled outputs changed",
                                            self.update)
            ]
        self.update(interactive=False)

    def chooserCB(self, *args):
        self.widgetChanged(True, interactive=True)

    def update(self, *args, **kwargs):
        meshname = self.meshwidget.get_value()
        try:
            meshctxt = mesh.meshes[meshname]
        except KeyError:
            self.chooser.update([])
            self.widgetChanged(False, interactive=False)
        else:
            self.chooser.update(meshctxt.outputSchedule.names())
            self.widgetChanged(meshctxt.outputSchedule.nOutputs()>0, 
                               interactive=False)
        
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        parameterwidgets.ParameterWidget.cleanUp(self)
    def get_value(self):
        return self.chooser.get_value()
    def set_value(self, val):
        self.chooser.set_state(val)
        self.widgetChanged(True, interactive=False)


def _makeScheduledOutputWidget(self, scope, verbose=False):
    return ScheduledOutputWidget(self, scope, name=self.name, verbose=verbose)

scheduledoutput.ScheduledOutputParameter.makeWidget = _makeScheduledOutputWidget
