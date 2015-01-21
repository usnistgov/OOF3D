# -*- python -*-
# $RCSfile: meshdataGUI.py,v $
# $Revision: 1.43.4.4 $
# $Author: fyc $
# $Date: 2014/07/28 22:18:33 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Window for displaying mesh data.

## TODO 3.1: The window needs to be updated when the Microstructure,
## Skeleton, or Mesh is renamed.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import primitives
from ooflib.common import subthread
from ooflib.common import utils
from ooflib.common.IO import gfxmanager
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import quit
from ooflib.common.IO.GUI import subWindow
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import whowidget
from ooflib.common.IO.GUI import widgetscope
from ooflib.engine import mesh
from ooflib.engine.IO.GUI import outputvalwidgets
import gtk
import ooflib.engine.IO.output

import sys

allMeshDataWindows = []

mdWindowMenu = mainmenu.OOF.Windows.addItem(oofmenu.OOFMenuItem("Mesh_Data"))

class MeshDataGUI(widgetscope.WidgetScope):
    count = 1
    def __init__(self, gfxwindow, time, position, output=None):
        mainthread.runBlock(self.__init__thread,
                            (gfxwindow, time, position, output))

    def __init__thread(self, gfxwindow, time, position, output):
        debug.mainthreadTest()
        allMeshDataWindows.append(self)
        widgetscope.WidgetScope.__init__(self, None)

        current_count = MeshDataGUI.count
        MeshDataGUI.count += 1
        self._name = "Mesh_Data_%d" % current_count
        self.output = output
        self.time = time
        self.position = position
        self.sbcallbacks = []
        self.gsbcallbacks = []          # callbacks from a specific gfx window
        self.updateLock = lock.Lock()

        self.outputparam = \
                     ooflib.engine.IO.output.ValueOutputParameter('output')

        # Although it's not displayed, we need a mesh widget in the
        # widgetscope, or the OutputParameterWidget won't work.
        # TODO 3.1: Is this ugly, or what?
        self.meshWidget = whowidget.WhoWidget(mesh.meshes, scope=self,
                                              name="Godot")

        self.gtk = gtk.Window(gtk.WINDOW_TOPLEVEL)
        title = utils.underscore2space(self._name)
        self.gtk.set_title(title)
        gtklogger.newTopLevelWidget(self.gtk, title)
        gtklogger.connect_passive(self.gtk, 'delete-event')
        gtklogger.connect_passive(self.gtk, 'configure-event')
        self.mainbox = gtk.VBox()
        self.gtk.add(self.mainbox)

        # Put this window into the Windows menu.  The menu item can't
        # be logged, since the creation and operation of the window
        # aren't logged, so scripts shouldn't refer to it at all.
        mainmenu.OOF.Windows.Mesh_Data.addItem(oofmenu.OOFMenuItem(
            self._name,
            no_log=1,
            help="Raise Mesh Data window %d." % current_count,
            threadable=oofmenu.UNTHREADABLE,
            callback=self.raiseWindow))

        expander = gtk.Expander("Source")
        gtklogger.setWidgetName(expander, 'ViewSource')
        gtklogger.connect_passive_after(expander, 'activate')
        self.mainbox.pack_start(expander)
        expander.set_expanded(1)
        
        self.table = gtk.Table(rows=config.dimension()+4, columns=2)
        expander.add(self.table)

        label = gtk.Label("Source Window:")
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, 0,1, xpadding=3, xoptions=gtk.FILL)
        tooltips.set_tooltip_text(label,
            "Display data for mouse clicks in this Graphics window.")

        self.gfxWindowChooser = chooser.ChooserWidget([],
                                                      callback=self.chooserCB,
                                                      name='GfxWindow')
        self.table.attach(self.gfxWindowChooser.gtk, 1,2, 0,1,
                     xpadding=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)


        label = gtk.Label("Mesh:")
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, 1,2,
                          xpadding=3, xoptions=gtk.FILL, yoptions=0)
        tooltips.set_tooltip_text(label,
                                  "Data is displayed for values on this mesh.")

        self.meshText = gtk.Entry()
        gtklogger.setWidgetName(self.meshText, "meshname")
        self.meshText.set_editable(False)
        self.meshText.set_size_request(12*guitop.top().charsize, -1)
        self.table.attach(self.meshText, 1,2, 1,2,
                          xpadding=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)

        # Position controls
        label = gtk.Label("position x:")
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, 2,3,
                          xpadding=3, xoptions=gtk.FILL, yoptions=0)
        self.xText = gtk.Entry()
        gtklogger.setWidgetName(self.xText, 'x')
        self.xText.set_size_request(12*guitop.top().digitsize, -1)
        self.table.attach(self.xText, 1,2, 2,3,
                          xpadding=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)
        self.xsignal = gtklogger.connect(self.xText, 'changed',
                                         self.posChangedCB)

        label = gtk.Label("position y:")
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, 3,4,
                          xpadding=3, xoptions=gtk.FILL, yoptions=0)
        self.yText = gtk.Entry()
        gtklogger.setWidgetName(self.yText, 'y')
        self.yText.set_size_request(12*guitop.top().digitsize, -1)
        self.table.attach(self.yText, 1,2, 3,4,
                          xpadding=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)
        self.ysignal = gtklogger.connect(self.yText, 'changed',
                                         self.posChangedCB)

        if config.dimension() == 3:
            label = gtk.Label("position z:")
            label.set_alignment(1.0, 0.5)
            self.table.attach(label, 0,1, 4,5,
                              xpadding=3, xoptions=gtk.FILL, yoptions=0)
            self.zText = gtk.Entry()
            gtklogger.setWidgetName(self.zText, 'z')
            self.zText.set_size_request(12*guitop.top().digitsize, -1)
            self.table.attach(self.zText, 1,2, 4,5, xpadding=3, 
                              xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)
            self.zsignal = gtklogger.connect(self.zText, 'changed', 
                                             self.posChangedCB)
            timerow = 5
        else:
            timerow = 6

        # Time controls.  Typing in the time widget does not
        # immediately update the displayed data, because interpolating
        # to a new time is an expensive computation, and shouldn't be
        # done while the user is in the middle of typing.  Instead,
        # the time widget is normally desensitized and uneditable.
        # When the user clicks the "Edit" button, the widget becomes
        # editable, the rest of the window is desensitized, and the
        # "Edit" button changes do a "Done" button.  When the user
        # clicks "Done" the data is updated and the time widget
        # becomes uneditable again.
        label = gtk.Label("time:")
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, timerow,timerow+1,
                          xpadding=3, xoptions=gtk.FILL, yoptions=0)
        tBox = gtk.HBox(spacing=3)
        self.table.attach(tBox, 1,2, timerow,timerow+1,
                          xpadding=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)
        self.tText = gtk.Entry()
        self.tText.set_editable(False)
        self.tText.set_sensitive(False)
        tBox.pack_start(self.tText, expand=1, fill=1)
        gtklogger.setWidgetName(self.tText, 't')
        self.tText.set_size_request(12*guitop.top().digitsize, -1)
        self.tEditButton = gtk.Button("Edit")
        tBox.pack_start(self.tEditButton, expand=0, fill=0)
        gtklogger.setWidgetName(self.tEditButton, "tEdit")
        gtklogger.connect(self.tEditButton, 'clicked', self.tEditCB)
        self.tEditMode = False
 
        # Output selection
        label = gtk.Label("Output:")
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, timerow+2,timerow+3,
                          xpadding=3, xoptions=gtk.FILL, yoptions=0)
        tooltips.set_tooltip_text(label,"Choose which data is displayed.")
        
        self.outputwidget = self.outputparam.makeWidget(scope=self)
        self.table.attach(self.outputwidget.gtk, 1,2, timerow+2,timerow+3,
                          xpadding=3, xoptions=gtk.EXPAND|gtk.FILL, yoptions=0)
        switchboard.requestCallback(self.outputwidget, self.outputwidgetCB)

        # Data display panel
        hbox = gtk.HBox()
        self.mainbox.pack_start(hbox, expand=1, fill=1, padding=5)
        frame = gtk.Frame("Data")
        gtklogger.setWidgetName(frame, 'Data')
        frame.set_shadow_type(gtk.SHADOW_IN)
        hbox.pack_start(frame, expand=1, fill=1, padding=5)
        vbox = gtk.VBox()
        frame.add(vbox)
        self.databox = gtk.HBox()
        vbox.pack_start(self.databox, expand=1, fill=1, padding=3)
        self.datawidget = None       # set by updateData

        # Buttons at the bottom of the window
        buttonbox = gtk.HBox()
        self.mainbox.pack_start(buttonbox, expand=0, fill=0, padding=3)
        # Freeze buttons 
        freezeframe = gtk.Frame("Freeze")
        gtklogger.setWidgetName(freezeframe, "Freeze")
        buttonbox.pack_start(freezeframe, expand=1, fill=1, padding=3)
        hbox = gtk.HBox()
        freezeframe.add(hbox)
        # Freeze Space button
        self.freezeSpaceFlag = False
        self.freezeSpaceButton = gtk.CheckButton('Space')
        gtklogger.setWidgetName(self.freezeSpaceButton, 'Space')
        hbox.pack_start(self.freezeSpaceButton, expand=1, fill=0, padding=0)
        self.freezeSpaceButton.set_active(self.freezeSpaceFlag)
        gtklogger.connect(self.freezeSpaceButton, 'clicked', 
                          self.freezeSpaceButtonCB)
        tooltips.set_tooltip_text(self.freezeSpaceButton,
                        "Prevent the data in this window from being updated when the sample position changes.")
        # Freeze Time button
        self.freezeTimeFlag = False
        self.freezeTimeButton = gtk.CheckButton('Time')
        gtklogger.setWidgetName(self.freezeTimeButton, "Time")
        hbox.pack_start(self.freezeTimeButton, expand=1, fill=0, padding=0)
        self.freezeTimeButton.set_active(self.freezeTimeFlag)
        gtklogger.connect(self.freezeTimeButton,'clicked',
                          self.freezeTimeButtonCB)
        tooltips.set_tooltip_text(self.freezeTimeButton,
            "Prevent the data in this window from being updated when the Mesh's time changes.")

        # Clone button
        self.cloneButton = gtkutils.StockButton(gtk.STOCK_COPY, 'Clone')
        gtklogger.setWidgetName(self.cloneButton, 'Clone')
        gtklogger.connect(self.cloneButton, 'clicked', self.cloneButtonCB)
        buttonbox.pack_start(self.cloneButton, expand=0, fill=0, padding=3)
        tooltips.set_tooltip_text(self.cloneButton,
            "Make a copy of this window with its current settings.")

        # Close button
        self.closeButton = gtk.Button(stock=gtk.STOCK_CLOSE)
        gtklogger.setWidgetName(self.closeButton, 'Close')
        gtklogger.connect(self.closeButton, 'clicked', self.closeButtonCB)
        buttonbox.pack_end(self.closeButton, expand=0, fill=0, padding=3)

        self.gtk.connect('destroy', self.destroyCB)

        self.updateGfxWindowChooser()
        if gfxwindow:
            self.gfxWindowChooser.set_state(gfxwindow.name)
        if position is not None:
            self.updatePosition(position)
        self.currentMesh = None
        self.updateMesh()

        self.setupSwitchboard()         # gfx window dependent callbacks
        self.sbcallbacks += [
            switchboard.requestCallbackMain('open graphics window',
                                            self.gfxwindowChanged),
            switchboard.requestCallbackMain('close graphics window',
                                            self.gfxwindowChanged),
            switchboard.requestCallbackMain('mesh data changed',
                                            self.meshDataChanged),
            switchboard.requestCallbackMain((gfxwindow, "time changed"),
                                            self.timeChanged)
            ]

        
        self.gtk.show_all()

    def raiseWindow(self, menuitem):
        debug.mainthreadTest()
        self.gtk.window.raise_()

    def sensitize(self):
        self.xText.set_sensitive(not self.tEditMode)
        self.yText.set_sensitive(not self.tEditMode)
        self.tText.set_sensitive(self.tEditMode)
        self.meshWidget.set_sensitive(not self.tEditMode)
        self.databox.set_sensitive(not self.tEditMode)
        self.freezeTimeButton.set_sensitive(not self.tEditMode)
        self.freezeSpaceButton.set_sensitive(not self.tEditMode)
        self.gfxWindowChooser.gtk.set_sensitive(not self.tEditMode)
        self.meshText.set_sensitive(not self.tEditMode)
        self.outputwidget.gtk.set_sensitive(not self.tEditMode)
        gtklogger.checkpoint(self._name+" sensitized")

    ###################

    # Gfx window management

    def gfxwindowChanged(self, window): # sb callback, window opened or closed
        self.updateGfxWindowChooser()

    def updateGfxWindowChooser(self):
        self.gfxWindowChooser.update(
            [w.name for w in gfxmanager.gfxManager.windows])

    def chooserCB(self, chsr, gfxwindowname):
        self.setupSwitchboard()
        self.updateMesh()               # calls updateData if needed

    def setupSwitchboard(self):
        map(switchboard.removeCallback, self.gsbcallbacks)
        window = self.currentGfxWindow()
        if window is not None:
            self.gsbcallbacks = [
                switchboard.requestCallback((window, "layers changed"),
                                            self.layersChangedCB),
                switchboard.requestCallbackMain((window, "meshinfo click"),
                                                self.updatePosition)
            ]
        else:
            self.gsbcallbacks = []

    def currentGfxWindow(self):
        name = self.gfxWindowChooser.get_value()
        if name:
            return gfxmanager.gfxManager.getWindow(name)

    ##############

    def closeButtonCB(self, button):
        self.gtk.destroy()

    def destroyCB(self, *args):         # gtk callback
        mainmenu.OOF.Windows.Mesh_Data.removeItem(self._name)
        map(switchboard.removeCallback, self.sbcallbacks)
        map(switchboard.removeCallback, self.gsbcallbacks)
        allMeshDataWindows.remove(self)

    ##############
        
    def cloneButtonCB(self, button):
        newviewer = openMeshData(self.currentGfxWindow(), self.time,
                                 self.position, self.output)
        if self.freezeTimeFlag:
            newviewer.freezeTimeButton.clicked()
        if self.freezeSpaceFlag:
            newviewer.freezeSpaceButton.clicked()

    ##############

    def freezeSpaceButtonCB(self, button):
        debug.mainthreadTest()
        self.freezeSpaceFlag = button.get_active()
        if not self.freezeSpaceFlag:
            self.updatePosition(self.position)
            subthread.execute(self.updateData)

    def freezeTimeButtonCB(self, button):
        debug.mainthreadTest()
        self.freezeTimeFlag = button.get_active()
        if not self.freezeTimeFlag:
            self.updateTime(self.currentGfxWindow().displayTime)

    ##############

    def meshDataChanged(self, meshctxt): # sb "mesh data changed"
        debug.mainthreadTest()
        if (meshctxt is self.currentMesh and
            (not self.freezeTimeFlag or
             self.time == self.currentMesh.getCurrentTime())):
            subthread.execute(self.updateData)

    def layersChangedCB(self):
        debug.subthreadTest()
        mainthread.runBlock(self.updateMesh)
        self.updateData()

    def outputwidgetCB(self, interactive): # chosen output has changed
        debug.subthreadTest()
        self.updateData()

    def posChangedCB(self, gtkobj): # text edited in x & y gtk.Entries
        debug.mainthreadTest()
        try:
            if config.dimension() == 2:
                self.position = primitives.Point(_getval(self.xText),
                                                 _getval(self.yText))
            elif config.dimension() == 3:
                self.position = primitives.Point(_getval(self.xText),
                                                 _getval(self.yText),
                                                 _getval(self.zText))
        except:
            # The user has typed something that can't be evaluated,
            # but maybe there's more typing to come. Ignore the error.
            if self.datawidget:
                self.datawidget.gtk.set_sensitive(0)
        else:
            subthread.execute(self.updateData)
            # Since the user has typed a new position, assume that
            # s/he really wants it, and don't overwrite it when the
            # mouse is clicked on the Mesh.
            self.freezeSpaceFlag = True
            self.freezeSpaceButton.set_active(True)

    def timeChanged(self): # sb callback. Time changed in gfx window.
        debug.mainthreadTest()
        if not self.freezeTimeFlag and not self.tEditMode:
            self.updateTime(self.currentGfxWindow().displayTime)
            
    def tEditCB(self, button):
        if not self.tEditMode:
            # Switch to time editing mode
            self.tEditMode = True
            self.tEditButton.set_label("Done")
            self.tText.set_editable(True)
        else:
            # Switch out of time editing mode
            self.tEditMode = False
            self.tText.set_editable(False)
            self.tEditButton.set_label("Edit")
            try:
                t = utils.OOFeval(self.tText.get_text().lstrip())
            except:
                pass
            else:
                self.time = t
                subthread.execute(self.updateData)
                # Since the user has entered a new time, don't
                # overwrite it when the graphics window's display time
                # changes.
                self.freezeTimeFlag = True
                self.freezeTimeButton.set_active(True)
        self.sensitize()

    ##############

    def updateMesh(self):
        debug.mainthreadTest()
        window = self.currentGfxWindow()
        newmesh = None
        if window:
            newmesh = window.topwho('Mesh')
            if newmesh:
                self.meshText.set_text(newmesh.path())
            else:
                self.meshText.set_text('<No Mesh in window!>')
        else:
            self.meshText.set_text('---')
        if not self.freezeTimeFlag:
            self.updateTime(window.displayTime)
        if newmesh is not self.currentMesh:
            self.currentMesh = newmesh
            subthread.execute(self.updateData)
        if newmesh is not None:
            self.meshWidget.set_value(newmesh.path())
        else:
            self.meshWidget.set_value(None)
        gtklogger.checkpoint(self._name+" mesh updated")

    def updatePosition(self, position):
        # Switchboard callback for (gfxwindow, "meshinfo click").
        # Also called when freezeSpaceFlag is unset, and during window
        # construction.
        debug.mainthreadTest()
        if not self.freezeSpaceFlag:
            if position != self.position:
                self.position = position
                subthread.execute(self.updateData)
            self.xsignal.block()
            self.ysignal.block()
            if config.dimension() == 3:
                self.zsignal.block()
            try:
                if position is not None:
                    # Strip blanks to the right of the number so that they
                    # don't get in the way when the user edits the
                    # position.
                    self.xText.set_text(("%-13.6g" % position.x).rstrip())
                    self.yText.set_text(("%-13.6g" % position.y).rstrip())
                    if config.dimension() == 3:
                        self.zText.set_text(("%-13.6g" % position.z).rstrip())
                else:
                    # Probably not required -- position is initially None,
                    # and having once been set, probably can't become
                    # None.
                    self.xText.set_text("")
                    self.yText.set_text("")
                    if config.dimension() == 3:
                        self.zText.set_text("")
            finally:
                self.xsignal.unblock()
                self.ysignal.unblock()
                if config.dimension() == 3:
                    self.zsignal.unblock()
            gtklogger.checkpoint(self._name+" position updated")

    def updateTime(self, time):
        if not self.freezeTimeFlag and not self.tEditMode:
            if time != self.time:
                self.time = time
                subthread.execute(self.updateData)
            if time is None:
                self.tText.set_text("")
            else:
                # Strip blanks to the right of the number so that they
                # don't get in the way when the user edits the
                # position.
                self.tText.set_text(("%-13.6g" % self.time).rstrip())
            gtklogger.checkpoint(self._name+" time updated")

    def updateData(self):
        debug.subthreadTest()
        self.updateLock.acquire()
        try:
            if self.datawidget:
                mainthread.runBlock(self.datawidget.destroy)
                self.datawidget = None

            op = mainthread.runBlock(self.outputwidget.get_value)

            if (self.currentMesh is not None and
                self.position is not None and op is not None):
                #self.currentMesh.begin_reading()

                self.currentMesh.restoreCachedData(self.time)
                val = None
                try:
                    # precompute *must* be called on a subthread
                    self.currentMesh.precompute_all_subproblems()
                    if (op is not None and 
                        not op.incomputable(self.currentMesh)):
                        element = self.currentMesh.enclosingElement(
                            self.position)
                        # op.evaluate eventually calls mesh precompute
                        # for the "Energy" or "Strain" selections in
                        # the Data Viewer, so we can't put these in
                        # updateDataMain below (running it with
                        # mainthread.runBlock), otherwise we get a
                        # lock error.
                        if element is not None:
                            masterpos = element.to_master(self.position)
                            val = op.evaluate(self.currentMesh.getObject(),
                                              [element], [[masterpos]])[0]
                finally:
                    self.currentMesh.releaseCachedData()
                    #self.currentMesh.end_reading()
                mainthread.runBlock(self.updateDataMain, (val,))
            gtklogger.checkpoint(self._name+" data updated")
        finally:
            self.updateLock.release()

    def updateDataMain(self, val):
        debug.mainthreadTest()
        self.datawidget = outputvalwidgets.makeWidget(val)
        self.databox.pack_start(self.datawidget.gtk,
                                expand=1, fill=1, padding=3)
        self.datawidget.show()


def _getval(widget):
    text = widget.get_text().lstrip()
    if text:
        return utils.OOFeval(text)
    return 0.0

###############################
        
def openMeshData(gfxwindow, time, position, output=None):
    return MeshDataGUI(gfxwindow, time, position, output)

