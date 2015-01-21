# -*- python -*-
# $RCSfile: pixelgroupwidget.py,v $
# $Revision: 1.32.10.3 $
# $Author: langer $
# $Date: 2014/05/08 14:39:00 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO import pixelgroupparam
from ooflib.common.IO import placeholder
from ooflib.common.IO import whoville
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import whowidget
import ooflib.common.microstructure
#Interface branch
from ooflib.engine.IO import interfaceparameters

# Widget for choosing a pixel group.  It *requires* a non trivial
# scope argument (WidgetScope object) so that it can find a WhoWidget
# for a microstructure.

class PixelGroupWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param, scope=None, name=None, verbose=False):
        self.groupchooser = chooser.ChooserWidget([], name=name)
        parameterwidgets.ParameterWidget.__init__(self, self.groupchooser.gtk,
                                                  scope=scope, verbose=verbose)
        self.mswidget = self.scope.findWidget(
            lambda w: isinstance(w, whowidget.WhoWidget)
            and (w.whoclass is whoville.getClass("Microstructure") or
                 w.whoclass is whoville.getClass("Image")))
        self.update()
        if param.value is not None:
            self.set_value(param.value)
        self.sbcallbacks = [
            switchboard.requestCallbackMain(self.mswidget, self.update),
            switchboard.requestCallbackMain("new pixel group", self.update),
            switchboard.requestCallbackMain("renamed pixel group",
                                            self.update),
            switchboard.requestCallbackMain("destroy pixel group",
                                            self.update),
            switchboard.requestCallbackMain(self.groupchooser, self.chooserCB)
            ]
    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.mswidget = None
        parameterwidgets.ParameterWidget.cleanUp(self)
    def update(self, *args, **kwargs):
        msname = self.mswidget.get_value(depth=1)
        if msname:
            ms = ooflib.common.microstructure.microStructures[msname]
            if ms:
                names = ms.getObject().groupNames()
                self.groupchooser.update(names)
                self.widgetChanged(len(names) > 0, interactive=0)
                return
        self.groupchooser.update([])
        self.widgetChanged(0, interactive=0)
    def chooserCB(self):
        self.widgetChanged(self.groupchooser.nChoices() > 0, interactive=1)
    def get_value(self):                # returns *name* of group
        return self.groupchooser.get_value()
    def set_value(self, groupname):
        self.groupchooser.set_state(groupname)
        

def _makePixelGroupWidget(self, scope=None, verbose=False):
    return PixelGroupWidget(self, scope=scope, name=self.name, verbose=verbose)

pixelgroupparam.PixelGroupParameter.makeWidget = _makePixelGroupWidget

############

class PixelAggregateWidget(PixelGroupWidget):
    def update(self, *args, **kwargs):
        msname = self.mswidget.get_value()
        if msname:
            ms = ooflib.common.microstructure.microStructures[msname]
            if ms:
                self.groupchooser.update(
                    [placeholder.selection.IDstring,
                     placeholder.every.IDstring] +
                    ms.getObject().groupNames())
                self.widgetChanged(1, interactive=0)
                return
        self.groupchooser.update([])
        self.widgetChanged(0, interactive=0)
    def get_value(self):
        rval = self.groupchooser.get_value()
        return placeholder.getPlaceHolderFromString(rval)

def _makePixelAggregateWidget(self, scope=None, verbose=False):
    return PixelAggregateWidget(self, scope=scope, name=self.name, 
                                verbose=verbose)

pixelgroupparam.PixelAggregateParameter.makeWidget = _makePixelAggregateWidget

#Interface branch
class PixelGroupInterfaceWidget(PixelGroupWidget):
    def update(self, *args, **kwargs):
        msname = self.mswidget.get_value()
        if msname:
            ms = ooflib.common.microstructure.microStructures[msname]
            if ms:
                names = ms.getObject().groupNames()
                names=names+[interfaceparameters.NO_PIXELGROUP_STR,
                             interfaceparameters.ANY_STR,
                             interfaceparameters.NORTH_STR,
                             interfaceparameters.SOUTH_STR,
                             interfaceparameters.EAST_STR,
                             interfaceparameters.WEST_STR]
                self.groupchooser.update(names)
                self.widgetChanged(len(names) > 0, interactive=0)
                return
        self.groupchooser.update([])
        self.widgetChanged(0, interactive=0)        

def _makePixelGroupInterfaceWidget(self, scope=None, verbose=False):
    return PixelGroupInterfaceWidget(self, scope=scope, name=self.name,
                                     verbose=verbose)

pixelgroupparam.PixelGroupInterfaceParameter.makeWidget = _makePixelGroupInterfaceWidget
