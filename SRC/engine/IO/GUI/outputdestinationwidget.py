# -*- python -*-
# $RCSfile: outputdestinationwidget.py,v $
# $Revision: 1.2.4.3 $
# $Author: langer $
# $Date: 2014/06/25 21:39:30 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common.IO import filenameparam
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.common.IO.GUI import tooltips
from ooflib.engine.IO import analyzemenu
from ooflib.engine.IO import outputdestination
from ooflib.engine.IO import scheduledoutput
import gtk


class OutputDestinationWidget(regclassfactory.RegisteredClassFactory):
    def __init__(self, obj=None, title=None, callback=None,
                 fill=0, expand=0, scope=None, name=None, verbose=False):
        self.outputWidget = scope.findWidget(
            lambda w: (isinstance(w, regclassfactory.RegisteredClassFactory) and
                       w.registry is scheduledoutput.ScheduledOutput.registry))

        self.sbcallback = switchboard.requestCallbackMain(self.outputWidget,
                                                          self.outputCB)
        regclassfactory.RegisteredClassFactory.__init__(
            self, registry=outputdestination.OutputDestination.registry,
            obj=obj, title=title, callback=callback, 
            fill=fill, expand=expand, scope=scope, name=name, verbose=verbose)
    def includeRegistration(self, reg):
        return issubclass(
            reg.subclass,
            self.outputWidget.get_value().getRegistration().destinationClass)
    def outputCB(self, *args):
        self.refresh()
    def cleanUp(self):
        switchboard.removeCallback(self.sbcallback)
        regclassfactory.RegisteredClassFactory.cleanUp(self)
                
def _makeOutputDestinationWidget(self, scope, verbose=False):
    return OutputDestinationWidget(self.value, scope=scope, name=self.name,
                                   verbose=verbose)
        
outputdestination.OutputDestinationParameter.makeWidget = \
    _makeOutputDestinationWidget

#####################

# class ExistingStreamWidget(parameterwidgets.ParameterWidget):
#     def __init__(self, value, scope=None, name=None):
#         filenames = outputdestination.allTextOutputStreams()
#         self.chooser = chooser.ChooserWidget(filenames,
#                                              callback=self.chooserCB, name=name)
#         parameterwidgets.ParameterWidget.__init__(self, self.chooser.gtk,
#                                                   scope=scope)
#         if value is not None:
#             self.set_value(value)
#         self.widgetChanged(self.chooser.nChoices() > 0, interactive=False)
#     def set_value(self, val):
#         self.chooser.set_state(val)
#     def get_value(self):
#         return self.chooser.get_value()
#     def chooserCB(self, *args):
#         self.widgetChanged(self.chooser.nChoices() > 0, interactive=True)

# def _makeExistingStreamWidget(self, scope):
#     return ExistingStreamWidget(self.value, scope=scope, name=self.name)

# outputdestination.ExistingStreamParam.makeWidget = _makeExistingStreamWidget

###################

MSGWINDOW = "<Message Window>"

class TextDestinationWidget(parameterwidgets.ParameterWidget):
    def __init__(self, param=None, scope=None, name=None, framed=True, 
                 verbose=False):
        debug.mainthreadTest()
        vbox = gtk.VBox(spacing=2)
        if framed:
            parameterwidgets.ParameterWidget.__init__(
                self, gtk.Frame(), scope=scope, name=name, verbose=verbose)
            self.gtk.add(vbox)
        else:
            parameterwidgets.ParameterWidget.__init__(
                self, vbox, scope=scope, name=name, verbose=verbose)

        self.chooser = chooser.ChooserWidget([], callback=self.chooserCB,
                                             name='Chooser')
        vbox.pack_start(self.chooser.gtk, expand=False, fill=False)
        bbox = gtk.HBox(spacing=2, homogeneous=True)
        vbox.pack_start(bbox, expand=0, fill=0)

        newbutton = gtkutils.StockButton(gtk.STOCK_NEW, "New...")
        gtklogger.setWidgetName(newbutton, "New")
        bbox.pack_start(newbutton, expand=True, fill=True)
        gtklogger.connect(newbutton, 'clicked', self.newCB)
        tooltips.set_tooltip_text(newbutton,
                                  "Open a new file for output.")

        self.rewindbutton = gtkutils.StockButton(gtk.STOCK_MEDIA_REWIND,
                                                 "Rewind")
        gtklogger.setWidgetName(self.rewindbutton, "Rewind")
        bbox.pack_start(self.rewindbutton, expand=True, fill=True)
        gtklogger.connect(self.rewindbutton, 'clicked', self.rewindCB)
        tooltips.set_tooltip_text(
            self.rewindbutton,
            "Rewind the selected file.  Data will be lost.")

        self.clearbutton = gtkutils.StockButton(gtk.STOCK_CLEAR, "Clear")
        gtklogger.setWidgetName(self.clearbutton, "Clear")
        bbox.pack_start(self.clearbutton, expand=True, fill=True)
        gtklogger.connect(self.clearbutton, 'clicked', self.clearCB)
        tooltips.set_tooltip_text(
            self.clearbutton,
            "Close all files and remove them from the list.")

        self.sbcallback = switchboard.requestCallbackMain(
            'output destinations changed', self.rebuild)

        self.rebuild()
        if param and param.value is not None:
            self.set_value(param.value)
        self.widgetChanged(True, interactive=False)

    def cleanUp(self):
        switchboard.removeCallback(self.sbcallback)
        parameterwidgets.ParameterWidget.cleanUp(self)

    def filenames(self):
        return [MSGWINDOW] + outputdestination.allTextOutputStreams()
        
    def rebuild(self):
        self.chooser.update(self.filenames())

    def newCB(self, button):
        debug.mainthreadTest()
        fileparam = outputdestination.newreg.getParameter('filename')
        modeparam = outputdestination.newreg.getParameter('mode')
        if parameterwidgets.getParameters(fileparam, modeparam,
                                          title="Add a data destination"):
            newname = fileparam.value
            # Create the OutputDestination object.  This calls
            # self.rebuild via the switchboard.
            dest = outputdestination.newreg()
            self.set_value(dest)

    def rewindCB(self, button):
        name = self.chooser.get_value()
        if name != MSGWINDOW:
            menuitem = analyzemenu.ops_menu.Rewind
            menuitem.callWithDefaults(filename=name)

    def clearCB(self, button):
        outputdestination.forgetTextOutputStreams()

    def chooserCB(self, *args):
        self.widgetChanged(True, interactive=True)

    def set_value(self, value):
        if isinstance(value, outputdestination.MessageWindowStream):
            self.chooser.set_state(MSGWINDOW)
        elif isinstance(value, outputdestination.TextOutputDestination):
            self.chooser.set_state(value.filename)

    def get_value(self):
        name = self.chooser.get_value()
        if name == MSGWINDOW:
            return outputdestination.msgWindowOutputDestination
        else:
            mode = outputdestination.getLatestMode(name,
                                                   filenameparam.WriteMode("w"))
            return outputdestination.OutputStream(name, mode)
