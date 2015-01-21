# -*- python -*-
# $RCSfile: gfxwindowbase.py,v $
# $Revision: 1.13.2.25 $
# $Author: langer $
# $Date: 2014/09/10 21:28:41 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import progress
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import subthread
from ooflib.common.IO import ghostgfxwindow
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import subWindow
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import labelledslider

import gobject
import gtk 
import threading

class GfxWindowBase(subWindow.SubWindow, ghostgfxwindow.GhostGfxWindow):
    def __init__(self, name, gfxmgr, clone=0):
        debug.subthreadTest()
        # self.name is also assigned by GhostGfxWindow, but it's
        # helpful for debugging for it to be assigned as soon as
        # possible in all execution paths.
        self.name = name
        self.gfxlock = lock.Lock()
        self.acquireGfxLock()

        # This whole initialization sequence is complicated.  The
        # reason is that the order of operations is important -- the
        # ghostgfxwindow makes function calls which need to be
        # redefined in the GUI before they occur -- and there is a
        # requirement that the main thread never be locked.
        # Furthermore, the ghostgfxwindow has to create the menu
        # before the SubWindow init gets called.  It could probably be
        # rationalized, but it's not urgent.

        # preinitialize and postinitialize are defined in gfxwindow.py
        # for 2D and gfxwindow3d.py for 3D.
        mainthread.runBlock(self.preinitialize, (name, gfxmgr, clone))
        # GhostGfxWindow.__init__ creates the canvas, among other things.
        ghostgfxwindow.GhostGfxWindow.__init__(self, name, gfxmgr,
                                               clone=clone)
        mainthread.runBlock(self.postinitialize, (name, gfxmgr, clone))
        self.releaseGfxLock()

        self.switchboardCallbacks.append(
            switchboard.requestCallback("shutdown", self.shutdownCB))

    ################################################

    def get_oofcanvas(self):
        return self.oofcanvas


    # Zoom Fill Window
    ################################################

    def zoomFillWindow(self, *args, **kwargs):
        # This has args because it's used as a menuitem callback.  The
        # 'lock' argument is not a menu argument, though.  It's only
        # used when zoomFillWindow is called explicitly from within
        # another drawing routine, to indicate that the gfxLock has
        # already been acquired.
        lock = kwargs.get('lock', True) # default is to acquire the lock
        if lock:
            self.acquireGfxLock()
        try:
            mainthread.runBlock(self.zoomFillWindow_thread)
        finally:
            if lock:
                self.releaseGfxLock()    


    # Functions that manipulate the LayerList
    ################################################

    def newLayerMembers(self):
        self.fillLayerList()
        ghostgfxwindow.GhostGfxWindow.newLayerMembers(self)

    ## Only call fillLayerList if the whole list needs to be rebuilt.
    def fillLayerList(self):
        mainthread.runBlock(self.fillLayerList_thread)

    def fillLayerList_thread(self):
        debug.mainthreadTest()
        self.suppressRowOpSignals()
        self.suppressSelectionSignals()
        try:
            self.layerList.clear()
            for layer in self.layers:
                self.layerList.prepend([layer])
                if layer is self.selectedLayer:
                    self.layerListView.get_selection().select_path('0')
        finally:
            self.allowRowOpSignals()
            self.allowSelectionSignals()
            
    def toggleLongLayerNames(self, menuitem, longlayernames):
        self.acquireGfxLock()
        try:
            self.settings.longlayernames = longlayernames
            self.fillLayerList()
        finally:
            self.releaseGfxLock()
        
    # Callbacks for the TreeView for the Layer List.
    ##################################################

    # TreeView callback for setting the state of the "Show" button 
    def renderShowCell(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        layer = model[iter][0]
        cell_renderer.set_active(not layer.hidden)

    def showcellCB(self, cell_renderer, path):
        layer = self.layerList[path][0]
        if layer.hidden:
            self.menu.Layer.Show(n=self.layerID(layer))
        else:
            self.menu.Layer.Hide(n=self.layerID(layer))

    def renderFreezeCell(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        layer = model[iter][0]
        cell_renderer.set_active(layer.frozen)

    def freezeCellCB(self, cell_renderer, path):
        layer = self.layerList[path][0]
        if layer.frozen:
            self.menu.Layer.Unfreeze(n=self.layerID(layer))
        else:
            self.menu.Layer.Freeze(n=self.layerID(layer))

    def renderLayerCell(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        layer = model[iter][0]
        who = layer.who()
        if who is not None:
            txt = "%s(%s)" % (who.getClassName(), who.name())
        else:
            # who is None.  This probably can't happen, but there was
            # comment here wondering if it could, and it's harmless to
            # check for it.
            txt = "???"
        cell_renderer.set_property('text', txt)

    def renderMethodCell(self, column, cell_renderer, model, iter):
        debug.mainthreadTest()
        layer = model[iter][0]
        if self.settings.longlayernames:
            cell_renderer.set_property('text', `layer`)
        else:
            cell_renderer.set_property('text', layer.short_name())
                                   
    def selectionChangedCB(self, selection): # self.layerListView callback
        debug.mainthreadTest()
        model, iter = selection.get_selected()
        self.suppressSelectionSignals()
        try:
            if iter is not None:
                layer = model[iter][0]
                self.menu.Layer.Select(n=self.layerID(layer))
            else:
                self.menu.Layer.Deselect(n=self.layerID(self.selectedLayer))
        finally:
            self.allowSelectionSignals()

    def layerDoubleClickCB(self, treeview, path, col):
        self.editLayer_gui(self.menu.Layer.Edit)

    # TreeView callback that determines if a row is displayed as a
    # separator.
    def layerRowSepFunc(self, model, iter):
        layer = model[iter][0]
        return not (layer.listed or self.settings.listall)

    # Callbacks for the layerList's "row-inserted" and "row-deleted"
    # signals, sent when the user reorders layers by dragging them in
    # the layer list.  "row-inserted" is sent first.
    
    def listRowInsertedCB(self, model, path, iter):
        # "row-inserted" is sent before the row is built, so we can't
        # get the actual layer here, just where it's going to be.
        self.destination_path = path
        self.suppressSelectionSignals()

    def listRowDeletedCB(self, model, path):
        self.allowSelectionSignals()
        if self.destination_path is not None:
            source_row = path[0]
            dest_row = self.destination_path[0]
            if source_row > dest_row:
                # The layer has been raised.  Remember that indices in the
                # gtk ListStore run in the opposite direction from indices
                # in the Display's layer list.
                layer = model[self.destination_path][0]
                # How far has the row moved? The -1 is because the path
                # was computed *before* the row was deleted.
                delta = source_row - dest_row - 1
                if delta > 0:
                    self.menu.Layer.Raise.By(n=self.layerID(layer),
                                             howfar=delta)
            else:                           # source_row < dest_row
                # The layer has been lowered.
                # After the source row is deleted, the destination row
                # number decreases by 1.
                layer = model[(dest_row-1,)][0]
                delta = dest_row - source_row - 1
                if delta > 0:
                    self.menu.Layer.Lower.By(n=self.layerID(layer),
                                             howfar=delta)
            self.destination_path = None

    # suppressRowOpSignals and allowRowOpSignals are used to make sure
    # that the row rearrangement callbacks aren't invoked when rows
    # are manipulated from the program, instead of by the user.
    def suppressRowOpSignals(self):
        debug.mainthreadTest()
        for signal in self.rowOpSignals:
            signal.block()

    def allowRowOpSignals(self):
        debug.mainthreadTest()
        for signal in self.rowOpSignals:
            signal.unblock()

    def suppressSelectionSignals(self):
        debug.mainthreadTest()
        self.selsignal.block()

    def allowSelectionSignals(self):
        debug.mainthreadTest()
        self.selsignal.unblock()
        
    # Call layerListRowChanged to notify the TreeView that the data it
    # displays has changed.
    def layerListRowChanged(self, n):
        rowno = len(self.layerList) - 1 - n
        self.layerList.row_changed(rowno, self.layerList.get_iter(rowno))

    def updateLayerList(self, layer):
        self.layerListRowChanged(self.layerID(layer))

    # def replaceLayer(self, count, oldlayer, newlayer):
    #     self.acquireGfxLock()
    #     try:
    #         ghostgfxwindow.GhostGfxWindow.replaceLayer(self, count,
    #                                                    oldlayer, newlayer)
    #         for row in self.layerList:
    #             if row[0] is oldlayer:
    #                 row[0] = newlayer
    #                 break
    #     finally:
    #         self.releaseGfxLock()


    # General callbacks
    #######################################################

    # gtk callback 
    def realizeCB(self, *args):         
        if not self.realized:
            self.realized = True
            subthread.execute(self.drawAtTime, (self.displayTime,))
        return False

    # OOFMenu callback
    def close(self, *args): 
        # The subwindow menu-removal can't depend on the existence of
        # .gtk, and it's done in the non-GUI parent, so call it
        # if this is the first time through.
        if not self.closed:
            ghostgfxwindow.GhostGfxWindow.close(self, *args)
            self.closed = True
        if self.gtk:
            mainthread.runBlock(self.gtk.destroy) # calls destroyCB via gtk

    # gtk callback
    def destroyCB(self, *args):
        # See comment in GhostGfxWindow.close about the order of operations.
        if self.gtk:
            ## tell all the miniThreads to stop and go home.
#             self.device.destroy()
#             if config.dimension() == 2:
#                 self.contourmapdata.device.destroy()
            
            for tbgui in self.toolboxGUIs:
                if tbgui.active:
                    tbgui.deactivate()
                tbgui.close()
            del self.toolboxGUIs
            del self.mouseHandler
            if self.menu:
                self.menu.gui_callback=None

            self.gtk = None             # make sure this isn't repeated

            # self.menu.File.Close() will call its callback on a
            # subthread without blocking, which means that the caller
            # of this function will continue as soon as this function
            # finishes.  Since the caller of this function may be
            # destroying other gtk objects in the gfx window, there
            # may be race conditions.  Setting a flag here, before
            # calling Close() allows other callbacks to know that the
            # window is already in the process of being closed.
            self.gtk_destruction_in_progress = True

            if self.menu:
                self.menu.File.Close()    # calls self.close()


    # Toolbox callbacks
    ##################################################

    def switchToolbox(self, chooser, tbname): # toolboxchooser callback
        self.selectToolbox(tbname)

    def selectToolbox(self, tbname):
        debug.mainthreadTest()
        if not (self.current_toolbox and (self.current_toolbox.name()==tbname)):
            if config.dimension() == 2:
                self.removeMouseHandler()
            if self.current_toolbox:
                self.current_toolbox.deactivate()
            self.current_toolbox = self.getToolboxGUIByName(tbname)
            self.current_toolbox.activate()
            self.toolboxbody.foreach(self.toolboxbody.remove)
            self.toolboxbody.add(self.current_toolbox.gtk)
            self.toolboxbody.show_all()

    def getToolboxGUIByName(self, name):
        for tbgui in self.toolboxGUIs:
            if tbgui.name() == name:
                return tbgui

    def makeToolboxGUI(self, tb):
        tbgui = mainthread.runBlock(tb.makeGUI)
        if tbgui:
            self.toolboxGUIs.append(tbgui)
            self.toolboxGUIs.sort()
            self.updateToolboxChooser()
               
    def updateToolboxChooser(self):
        self.toolboxGUIs.sort()
        self.toolboxchooser.update([tb.name() for tb in self.toolboxGUIs])


    # Layer callbacks
    ######################################################
                
    # def newLayer_gui(self, menuitem):
    #     layereditor.menu.LayerSet.New(window=self.name)

    def editLayer_gui(self, menuitem):
        if self.selectedLayer is not None:
            category = menuitem.get_arg("category")
            what = menuitem.get_arg("what")
            how = menuitem.get_arg("how")
            category.value = self.selectedLayer.who().getClassName()
            what.value = self.selectedLayer.who().path()
            how.value = self.selectedLayer
            if parameterwidgets.getParameters(category, what, how,
                                              title="Edit Graphics Layer"):
                menuitem.callWithDefaults(n=self.layerID(self.selectedLayer))
        
    def newLayer(self, displaylayer):
        self.fillLayerList()
        
    def deleteLayer_gui(self, menuitem):
        if self.selectedLayer is None:
            guitop.top().message_out('No layer is selected!\n')
        else:
            self.suppressSelectionSignals()
            try:
                self.menu.Layer.Delete(n=self.layerID(self.selectedLayer))
            finally:
                self.allowSelectionSignals()

    def freezeLayer_gui(self, menuitem):
        if self.selectedLayer is not None:
            self.menu.Layer.Freeze(n=self.layerID(self.selectedLayer))

    def unfreezeLayer_gui(self, menuitem):
        if self.selectedLayer is not None:
            self.menu.Layer.Unfreeze(n=self.layerID(self.selectedLayer))

    # This is an override of the command-line menu callback in
    # ghostgfxwindow.  It exists in addition to the GUI callback
    # below, which is also required because it operates on the
    # current layer.
    def hideLayer(self, menuitem, n):   # OOFMenu callback
        ghostgfxwindow.GhostGfxWindow.hideLayer(self, menuitem, n)
        mainthread.runBlock(self.hideLayer_thread, (menuitem, n))

    def hideLayer_thread(self, menuitem, n):
        self.layerListRowChanged(n)
        # Update the contourmap.
        if config.dimension() == 2:
            self.contourmap_newlayers()
            subthread.execute(self.show_contourmap_info)

        
    def hideLayer_gui(self, menuitem):  # OOFMenu GUI callback.
        if self.selectedLayer is None:
            reporter.report('No layer is selected!')
        else:
            self.menu.Layer.Hide(n=self.layerID(self.selectedLayer))

        
    def showLayer(self, menuitem, n):   # OOFMenu callback.
        ghostgfxwindow.GhostGfxWindow.showLayer(self, menuitem, n)
        mainthread.runBlock(self.showLayer_thread, (menuitem, n))

    def showLayer_thread(self, menuitem, n):
        self.layerListRowChanged(n)
        # Update the contourmap.
        if config.dimension() == 2:
            self.contourmap_newlayers()
            subthread.execute(self.show_contourmap_info)

    def showLayer_gui(self, menuitem):  # OOFMenu GUI callback
        if self.selectedLayer is None:\
            reporter.report('No layer is selected!')
        else:
            self.menu.Layer.Show(n=self.layerID(self.selectedLayer))

    def selectLayer(self, n):
        if self.selectedLayer is not None:
            self.deselectLayer(self.layerID(self.selectedLayer))
        ghostgfxwindow.GhostGfxWindow.selectLayer(self, n)
        mainthread.runBlock(self.selectLayer_thread, (n,))

    def selectLayer_thread(self, n):
        self.suppressSelectionSignals()
        self.layerListView.get_selection().select_path(self.nlayers()-n-1)
        self.allowSelectionSignals()

    def deselectLayer(self, n):
        if self.selectedLayer is not None:
            mainthread.runBlock(self.deselectLayer_thread, (n,))
            ghostgfxwindow.GhostGfxWindow.deselectLayer(self, n)

    def deselectLayer_thread(self, n):
        self.suppressSelectionSignals()
        self.layerListView.get_selection().unselect_all()
        self.allowSelectionSignals()

    def deselectAll(self):
        # called by createDefaultLayers and sb 'deselect all gfxlayers'
        if self.selectedLayer is not None:
            mainthread.runBlock(self.deselectAll_thread)

    def deselectAll_thread(self):
        self.suppressSelectionSignals()
        self.layerListView.get_selection().unselect_all()
        ghostgfxwindow.GhostGfxWindow.deselectAll(self)
        self.allowSelectionSignals()
        
    # At layer-removal time, it's necessary to explicitly redraw the
    # contourmap, because the main canvas layers have not been redrawn,
    # so the usual automatic redraw has not taken place.
    def removeLayer(self, layer):
        ghostgfxwindow.GhostGfxWindow.removeLayer(self, layer)
        if config.dimension() == 2:
            self.show_contourmap_info()
    
    def raiseLayer_gui(self, menuitem):
        if self.selectedLayer is None:
            guitop.top().message_out('No layer is selected!\n')
        else:
            self.menu.Layer.Raise.One_Level(
                n=self.layerID(self.selectedLayer))

    def raiseToTop_gui(self, menuitem):
        if self.selectedLayer is None:
            guitop.top().message_out('No layer is selected!\n')
        else:
            self.menu.Layer.Raise.To_Top(
                n=self.layerID(self.selectedLayer))

    def lowerLayer_gui(self, menuitem):
        if self.selectedLayer is None:
            guitop.top().message_out('No layer is selected!\n')
        else:
            self.menu.Layer.Lower.One_Level(
                n=self.layerID(self.selectedLayer))

    def lowerToBottom_gui(self, menuitem):
        if self.selectedLayer is None:
            guitop.top().message_out('No layer is selected!\n')
        else:
            self.menu.Layer.Lower.To_Bottom(
                n=self.layerID(self.selectedLayer))

    def raiseLayerByGUI(self, layer):
        self.menu.Layer.Raise.One_Level(n=self.layerID(layer))

    def lowerLayerByGUI(self, layer):
        self.menu.Layer.Lower.One_Level(n=self.layerID(layer))


    #### Mouse clicks ############

    def setMouseHandler(self, handler):
        self.mouseHandler = handler

    def removeMouseHandler(self):
        self.mouseHandler = mousehandler.nullHandler

    def mouseCB(self, eventtype, x, y, shift, ctrl):
        debug.mainthreadTest()
        global _during_callback
        _during_callback = 1
        if self.mouseHandler.acceptEvent(eventtype):
            if eventtype == 'up':
                self.mouseHandler.up(x,y, shift, ctrl)
            elif eventtype == 'down':
                self.mouseHandler.down(x,y, shift, ctrl)
            elif eventtype == 'move':
                self.mouseHandler.move(x,y, shift, ctrl)
        _during_callback = 0

    #############################################

    # Time Controls

    def makeTimeBox(self):
        # Construct and return, but don't install, a box containing
        # the time slider and other widgets.
        timebox = gtk.HBox(spacing=2)
        gtklogger.setWidgetName(timebox, 'time')
        timebox.pack_start(gtk.Label("time:"), expand=False, fill=False, 
                           padding=2)

        self.prevtimeButton = gtkutils.StockButton(gtk.STOCK_GO_BACK)
        gtklogger.setWidgetName(self.prevtimeButton, "prev")
        gtklogger.connect(self.prevtimeButton, 'clicked', self.prevtimeCB)
        timebox.pack_start(self.prevtimeButton, expand=False, fill=False)
        tooltips.set_tooltip_text(self.prevtimeButton, 
                                  "Go to the previous stored time.")
        
        self.nexttimeButton = gtkutils.StockButton(gtk.STOCK_GO_FORWARD)
        gtklogger.setWidgetName(self.nexttimeButton, "next")
        gtklogger.connect(self.nexttimeButton, 'clicked', self.nexttimeCB)
        timebox.pack_start(self.nexttimeButton, expand=False, fill=False)
        tooltips.set_tooltip_text(self.nexttimeButton,
                                  "Go to the next stored time.")

        # The slider/entry combo has immediate==False because we don't
        # want to update until the user is done typing a time.
        self.timeslider = labelledslider.FloatLabelledSlider(
            value=0.0, vmin=0, vmax=0, step=0.01,
            callback=self.timeSliderCB,
            name='timeslider',
            immediate=False)
        self.timeslider.set_policy(gtk.UPDATE_DISCONTINUOUS)
        timebox.pack_start(self.timeslider.gtk, expand=True, fill=True)
        self.timeslider.set_tooltips(
            slider="Select an interpolation time.",
            entry="Enter an interpolation time.")

        return timebox
        
    def timeSliderCB(self, slider, val):
        # If the time is outside of the range of times stored in the
        # Mesh, it will be automatically changed to the earliest or
        # latest time.
        self.menu.Settings.Time.callWithDefaults(time=val)

    def prevtimeCB(self, gtkbutton):
        times = self.findAnimationTimes()
        for i,t in enumerate(times[1:]):
            if t >= self.displayTime:
                # i indexes times[1:] so the previous time is
                # times[i], not times[i-1].
                self.menu.Settings.Time.callWithDefaults(time=times[i])
                return

    def nexttimeCB(self, gtkbutton):
        times = self.findAnimationTimes()
        for t in times:
            if t > self.displayTime:
                self.menu.Settings.Time.callWithDefaults(time=t)
                return

    def updateTimeControls(self):
        mainthread.runBlock(self._updateTimeControls)
    def _updateTimeControls(self):
        debug.mainthreadTest()
        times = self.findAnimationTimes()
        if times:
            self.timeslider.set_sensitive(True)
            mintime = min(times)
            maxtime = max(times)
            self.timeslider.setBounds(mintime, maxtime)
        else:
            self.timeslider.set_sensitive(False)
        self.sensitizeTimeButtons(times)

    def sensitizeTimeButtons(self, times=None):
        debug.mainthreadTest()
        if times is None:       # distinguish from []!
            times = self.findAnimationTimes()
        notlast = bool(times and self.displayTime != times[-1])
        notfirst = bool(times and self.displayTime != times[0])
        self.nexttimeButton.set_sensitive(notlast)
        self.prevtimeButton.set_sensitive(notfirst)

    def setTimeCB(self, menuitem, time):
        self.drawAtTime(time)

    def drawAtTime(self, time):
        debug.subthreadTest()
        if time is not None:
            self.setDisplayTime(time)
            mainthread.runBlock(self.timeslider.set_value, (self.displayTime,))
            # Ensure that animatable layers will be redrawn by backdating
            # them, and then calling "draw".  All time-dependent layers
            # are animatable, and they get their time from the GfxWindow's
            # displayTime.

            for layer in self.layers:
                layer.timeChanged() 

        self.draw()

        mainthread.runBlock(self.sensitizeTimeButtons)

    #=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

    def animate(self, menuitem, start, finish, times, frame_rate, style):
        menuitem.disable()
        prog = progress.getProgress("Animation", style.getProgressStyle())

        # Construct a generator that produces the times of the
        # animation frames.  

        ## OLD COMMENT WHICH SEEMS NOT TO BE TRUE ANYMORE: Python
        ## generators aren't thread safe in some mysterious way, so
        ## the generator has to be constructed on the main thread.  If
        ## this isn't done, then interrupting an animation can lead to
        ## an internal python error or seg fault.
        # timegen = mainthread.runBlock(self._timegenerator,
        #                               (style, times, start, finish))
        timegen = self._timegenerator(style, times, start, finish)

        # Get the full list of times from the animation layers so we
        # can find the start and finish times.  This is just to
        # calibrate the progress bar.  timegen is what actually
        # produces the frame times.
        times = self.findAnimationTimes()
        
        if times and times[-1] > times[0]:
            time0 = times[0]
            time1 = times[-1]
            # Animation timing is controlled by a timeout callback
            # which periodically sets an "escapement" Event.  Every
            # time the Event is set, it allows one frame to be drawn.
            self._escapement = threading.Event()

            # This menuitem shouldn't finish until the escapement
            # timeout callback has been cleared, which is indicated by
            # another event.
            escapementDone = threading.Event()

            # _stopAnimation indicates that the animation is complete,
            # either because it ran to the end, the user interrupted
            # it, or the program is quitting.
            self._stopAnimation = False

            # Start the escapement.
            gobject.timeout_add(
                int(1000./frame_rate), # time between frames, in milliseconds
                self._escapementCB,
                prog,
                escapementDone,
                priority=gobject.PRIORITY_LOW)

            # Draw frames, after waiting for an escapement event.
            while not self._stopAnimation:
                self._escapement.wait()
                if prog.stopped() or self._stopAnimation:
                    self._stopAnimation = True
                    break
                # Clear the event, so that we have to wait for the
                # escapement to set it again before drawing the
                # next frame. This is done *before* drawing the
                # current frame, because if drawing a frame takes
                # longer than the time between escapement events,
                # we'll want to start on the next frame as soon as
                # possible.
                self._escapement.clear()

                try:
                    time = timegen.next()
                except StopIteration:
                    self._stopAnimation = True
                else:
                    # Update the progress bar and actually do the drawing.
                    prog.setMessage(`time`)
                    prog.setFraction((time-time0)/(time1-time0))
                    self.drawAtTime(time)

            ## TODO 3.1: Use some other scheme for unthreaded mode.

            escapementDone.wait()
            prog.finish()
            menuitem.enable()

    def _escapementCB(self, prog, escapementDone):
        # Timeout callback that calls self._escapement.set()
        # periodically.  This is called on the main thread.
        self._escapement.set()
        if prog.stopped() or self._stopAnimation:
            self._stopAnimation = True
            escapementDone.set()
            return False        # don't reinstall time out callback
        return True             # do reinstall timeout callback

    def _timegenerator(self, style, times, start, finish):
        return iter(style.getTimes(times.times(start, finish, self)))

    def shutdownCB(self):
        self._stopAnimation = True
        # self._escapement won't exist if the window hasn't been
        # animated, so use try/except.
        try:
            self._escapement.set()
        except:
            pass
