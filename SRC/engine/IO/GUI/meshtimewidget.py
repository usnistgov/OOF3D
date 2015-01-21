# -*- python -*-
# $RCSfile: meshtimewidget.py,v $
# $Revision: 1.12.4.3 $
# $Author: langer $
# $Date: 2014/05/09 02:16:19 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO import gfxmanager
from ooflib.common.IO import placeholder
from ooflib.common.IO import whoville
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.engine import mesh
from ooflib.engine.IO import animationtimes
from ooflib.engine.IO import meshparameters

import gtk

# Widget for choosing a time at which to display a Mesh.  There are
# two derived classes.  MeshTimeParamWidget uses the widget scope to
# find a Mesh widget, and allows times to be chosen from the mesh's
# data cache. GfxMeshTimeParamWidget allows times to be chosen from
# all of the animatable Mesh layers in a graphics window.

class MeshTimeWidgetBase(parameterwidgets.ParameterWidget):
    def __init__(self, scope, name=None, verbose=False):
        debug.mainthreadTest()

        parameterwidgets.ParameterWidget.__init__(
            self, gtk.HBox(), scope=scope, name=name, verbose=verbose)
        self.times = []
        self.signals = []
        self.sbcallbacks = []
        
        self.earliestButton = gtkutils.StockButton(gtk.STOCK_MEDIA_REWIND)
        gtklogger.setWidgetName(self.earliestButton, 'earliest')
        self.signals.append(gtklogger.connect(self.earliestButton, 'clicked',
                                              self.extremeCB, 
                                              placeholder.earliest))
        self.gtk.pack_start(self.earliestButton, expand=0, fill=0)
        tooltips.set_tooltip_text(self.earliestButton,
                             "Use the earliest stored time.")

        self.prevButton = gtkutils.StockButton(gtk.STOCK_GO_BACK)
        gtklogger.setWidgetName(self.prevButton, "Prev")
        self.signals.append(gtklogger.connect(self.prevButton, 'clicked', 
                                              self.prevCB))
        self.gtk.pack_start(self.prevButton, expand=0, fill=0)
        tooltips.set_tooltip_text(self.prevButton,
                             "Go to an earlier time saved in the mesh.")

        self.text = gtk.Entry()
        gtklogger.setWidgetName(self.text, 'Text')
        self.signals.append(gtklogger.connect(self.text, 'changed',
                                              self.entryCB))
        self.gtk.pack_start(self.text, expand=1, fill=1)

        self.nextButton = gtkutils.StockButton(gtk.STOCK_GO_FORWARD)
        gtklogger.setWidgetName(self.nextButton, "Next")
        gtklogger.connect(self.nextButton, 'clicked', self.nextCB)
        self.gtk.pack_start(self.nextButton, expand=0, fill=0)
        tooltips.set_tooltip_text(self.nextButton,
                             "Go to a later time saved in the mesh.")

        self.latestButton = gtkutils.StockButton(gtk.STOCK_MEDIA_FORWARD)
        gtklogger.setWidgetName(self.latestButton, 'latest')
        self.signals.append(gtklogger.connect(self.latestButton, 'clicked',
                                              self.extremeCB,
                                              placeholder.latest))
        self.gtk.pack_start(self.latestButton, expand=0, fill=0)
        tooltips.set_tooltip_text(self.latestButton,
                             "Use the latest stored time.")
        
        self.mode = placeholder.latest # 'earliest', 'latest', or None

    def blockSignals(self):
        debug.mainthreadTest()
        for signal in self.signals:
            signal.block()
    def unblockSignals(self):
        debug.mainthreadTest()
        for signal in self.signals:
            signal.unblock()

    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        parameterwidgets.ParameterWidget.cleanUp(self)
                
    def sensitize(self):
        debug.mainthreadTest()
        self.getTimes()
        if self.times:
            if self.mode is placeholder.latest:
                time = self.times[-1]
            elif self.mode is placeholder.earliest:
                time = self.times[0]
            else:
                time = self.get_value()
        self.latestButton.set_sensitive(
            bool(self.times and self.mode is not placeholder.latest))
        self.earliestButton.set_sensitive(
            bool(self.times and self.mode is not placeholder.earliest))
        self.text.set_sensitive(bool(self.times))
        self.nextButton.set_sensitive(bool(self.times and
                                           time is not None and
                                           time < self.times[-1]))
        self.prevButton.set_sensitive(bool(self.times and
                                           time is not None and
                                           time > self.times[0]))

    def set_value(self, value):
        debug.mainthreadTest()
        self.blockSignals()
        if not self.times:
            self.text.set_text("---")
            ok = False
        elif value is placeholder.latest or value is None:
            self.text.set_text(placeholder.latest.IDstring)
            self.mode = placeholder.latest
            ok = True
        elif value is placeholder.earliest:
            self.text.set_text(placeholder.earliest.IDstring)
            self.mode = placeholder.earliest
            ok = True
        else:
            self.text.set_text(`value`)
            self.mode = None
            ok = True
        self.sensitize()
        self.unblockSignals()
        self.widgetChanged(ok, interactive=False)
            
    def get_value(self):
        debug.mainthreadTest()
        if self.mode is not None:
            return self.mode
        try:
            return float(eval(self.text.get_text()))
        except:
            return None

    def extremeCB(self, gtkobj, mode):
        debug.mainthreadTest()
        self.mode = mode
        self.blockSignals()
        self.text.set_text(mode.IDstring)
        self.unblockSignals()
        self.sensitize()

    def entryCB(self, *gtkobj):
        debug.mainthreadTest()
        # If we can convert the text to a float, or if it's the
        # IDstring for the earliest or latest placeholders, it's ok.
        txt = self.text.get_text()
        if txt == placeholder.earliest.IDstring:
            self.mode = placeholder.earliest
            self.widgetChanged(True, interactive=True)
        elif txt == placeholder.latest.IDstring:
            self.mode = placeholder.latest
            self.widgetChanged(True, interactive=True)
        else:
            try:
                time = float(eval(self.text.get_text()))
            except:
                self.widgetChanged(False, interactive=True)
            else:
                ok = self.times and (self.times[0] <= time <= self.times[-1])
                self.widgetChanged(ok, interactive=True)
            self.mode = None
        self.sensitize()

    def prevCB(self, gtkobj):
        debug.mainthreadTest()
        time = self.get_value()
        if time is placeholder.latest:
            time = self.times[-2]
        elif time is None:
            time = self.times[0]
        else:
            # Find the first time in the cached times that is greater
            # than or equal to the current value, and choose the
            # previous one.
            for i,t in enumerate(self.times[1:]):
                if t >= time:
                    # i indexes times[1:], not times, so the previous
                    # time is times[i], not times[i-1]
                    time = self.times[i]
                    break
        self.mode = None
        self.blockSignals()
        self.text.set_text(`time`)
        self.unblockSignals()
        self.sensitize()
        self.widgetChanged(True, interactive=True)

    def nextCB(self, gtkobj):
        debug.mainthreadTest()
        time = self.get_value()
        ## time should never be 'latest' when nextButton is sensitized
        if time is None:
            time = self.times[-1]
        elif time is placeholder.earliest:
            time = self.times[1]
        else:
            for t in self.times:
                if t > time:
                    time = t
                    break
        self.mode = None
        self.blockSignals()
        self.text.set_text(`time`)
        self.unblockSignals()
        self.sensitize()
        self.widgetChanged(True, interactive=True)

##################

class MeshTimeWidget(MeshTimeWidgetBase):
    def __init__(self, scope, name=None, verbose=False):
        # Find the associated mesh widget
        self.meshwidget = scope.findWidget(
            lambda x: isinstance(x, whowidget.WhoWidget)
            and x.whoclass is mesh.meshes)

        MeshTimeWidgetBase.__init__(self, scope, name, verbose=verbose)
        self.getTimes()

        self.widgetChanged(self.currentMeshContext() is not None,
                           interactive=False)
        self.sbcallbacks.extend([
            switchboard.requestCallbackMain(self.meshwidget, self.meshwidgetCB),
            switchboard.requestCallbackMain("mesh changed", self.meshwidgetCB),
            switchboard.requestCallbackMain("mesh data changed",
                                            self.meshwidgetCB)
            ])

    def meshwidgetCB(self, *args, **kwargs):
        oldvalue = self.get_value()
        self.getTimes()         # sets self.times
        if oldvalue in self.times:
            self.set_value(oldvalue)
        else:
            self.set_value(placeholder.latest)
    def currentMeshContext(self):
        meshname = self.meshwidget.get_value()
        try:
            return mesh.meshes[meshname]
        except KeyError:
            pass
    def getTimes(self):
        meshctxt = self.currentMeshContext()
        # If meshctxt is None or is a WhoProxy object, it won't have a
        # cachedTimes method.  In either case, the right thing to do
        # is to ignore the error and set self.times to an empty list.
        try:
            self.times = meshctxt.cachedTimes()
            currenttime = meshctxt.getCurrentTime()
            if currenttime not in self.times:
                self.times += [currenttime]
                self.times.sort()
        except AttributeError:
            self.times = []

class MeshTimeParamWidget(MeshTimeWidget):
    def __init__(self, param, scope, name=None, verbose=False):
        MeshTimeWidget.__init__(self, scope, name, verbose=verbose)
        self.set_value(param.value)

def _MeshTimeParam_makeWidget(self, scope=None, verbose=False):
    return MeshTimeParamWidget(self, scope=scope, name=self.name, 
                               verbose=verbose)

placeholder.TimeParameter.makeWidget = _MeshTimeParam_makeWidget

##############

class GfxMeshTimeParamWidget(MeshTimeWidgetBase):
    def __init__(self, param, scope, name=None, verbose=False):
        self.gfxwindow = None
        MeshTimeWidgetBase.__init__(self, scope, name, verbose=verbose)
        menuitem = scope.findData('menuitem')
        gfxwindowname = menuitem.path().split('.')[1]
        self.gfxwindow = gfxmanager.gfxManager.getWindow(gfxwindowname)
        self.getTimes()
        self.set_value(param.value)

    def getTimes(self):
        if self.gfxwindow is None:
            self.times = []
        self.times = self.gfxwindow.findAnimationTimes()

def _GfxMeshTimeParam_makeWidget(self, scope=None, verbose=False):
    return GfxMeshTimeParamWidget(self, scope=scope, name=self.name,
                                  verbose=verbose)

placeholder.GfxTimeParameter.makeWidget = _GfxMeshTimeParam_makeWidget
        



