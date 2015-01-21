# -*- python -*-
# $RCSfile: destinationparamwidget.py,v $
# $Revision: 1.20.2.4 $
# $Author: langer $
# $Date: 2013/11/08 20:43:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Widget for the Destination parameter. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.SWIG.common import guitop
from ooflib.common.IO import automatic
from ooflib.common.IO import destinationparam
from ooflib.common.IO import filenameparam
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import parameterwidgets
import gtk

MSGWINDOW = "Message Window"

# _allDestinationWidgets keeps track of all destination widgets, so
# that their lists can be synchronized.  It's tempting to use a
# WeakKeyDictionary instead of a set here, but it would be wrong.  The
# reference count for the widget doesn't go to zero when the widget is
# destroyed, unless the switchboard callback is removed, so we'd need
# an explicity cleanUp() function even if we used a WeakKeyDictionary.
_allDestinationWidgets = set()

class DestinationParamWidget(parameterwidgets.ParameterWidget):
    # All instances share the same namelist.
    namelist = [MSGWINDOW]
    def __init__(self, param=None, scope=None, name=None, framed=True):
        vbox = gtk.VBox(spacing=2)
        if framed:
            parameterwidgets.ParameterWidget.__init__(self, gtk.Frame(),
                                                      scope=scope, name=name)
            self.gtk.add(vbox)
        else:
            parameterwidgets.ParameterWidget.__init__(self, vbox, scope=scope,
                                                      name=name)
            

        self.chooser = chooser.ChooserWidget(DestinationParamWidget.namelist,
                                             callback=self.chooserCB,
                                             name='Chooser')
        vbox.pack_start(self.chooser.gtk, expand=0, fill=0)

        bbox = gtk.HBox(spacing=2, homogeneous=True)
        vbox.pack_start(bbox, expand=0, fill=0)

        newbutton = gtkutils.StockButton(gtk.STOCK_NEW, "New...")
        gtklogger.setWidgetName(newbutton, "New")
        bbox.pack_start(newbutton, expand=1, fill=1)
        gtklogger.connect(newbutton, 'clicked', self.newCB)

        self.clearbutton = gtkutils.StockButton(gtk.STOCK_CLEAR, "Clear")
        gtklogger.setWidgetName(self.clearbutton, "Clear")
        bbox.pack_start(self.clearbutton, expand=1, fill=1)
        gtklogger.connect(self.clearbutton, 'clicked', self.clearCB)

        self.sbcallbacks = [
            switchboard.requestCallbackMain('destinations changed',
                                            self.rebuild)
            ]
        self.rebuild()
        if param and param.value is not None:
            self.set_value(param.value)
        self.widgetChanged(1, interactive=0)
        _allDestinationWidgets.add(self)

    def cleanUp(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        _allDestinationWidgets.remove(self)
        parameterwidgets.ParameterWidget.cleanUp(self)

    def rebuild(self):
        self.chooser.update(DestinationParamWidget.namelist)

    def newCB(self, button):
        debug.mainthreadTest()
        fileparam = filenameparam.WriteFileNameParameter("filename",
                                                         tip="Data file name")
        if parameterwidgets.getParameters(fileparam,
                                          title="Add a data destination"):
            newname = fileparam.value
            if newname not in DestinationParamWidget.namelist:
                DestinationParamWidget.namelist.append(newname)
                self.rebuild()
                self.just_set_value(newname)
                self.updateOtherWidgets()
                self.widgetChanged(True, interactive=True)

    def clearCB(self, button):
        DestinationParamWidget.namelist = [MSGWINDOW]
        self.rebuild()
        self.updateOtherWidgets()
        self.widgetChanged(1, interactive=1)

    def chooserCB(self, *args):
        self.widgetChanged(1, interactive=1)

    def just_set_value(self, value):
        if value == automatic.automatic:
            self.chooser.set_state(MSGWINDOW)
        else:
            self.chooser.set_state(value)

    def set_value(self, value):
        self.just_set_value(value)
        self.widgetChanged(1, interactive=0)        

    def get_value(self):
        val = self.chooser.get_value()
        if val == MSGWINDOW:
            return automatic.automatic
        return val

    def updateOtherWidgets(self):
        for widget in _allDestinationWidgets:
            if widget is not self:
                widget.rebuild()

def _make_DestParamWidget(self, scope=None):
    return DestinationParamWidget(self, scope=scope, name=self.name)

destinationparam.DestinationParameter.makeWidget = _make_DestParamWidget
