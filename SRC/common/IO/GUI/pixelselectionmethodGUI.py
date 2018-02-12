# -*- python -*-
# $RCSfile: pixelselectionmethodGUI.py,v $
# $Revision: 1.1.2.1 $
# $Author: rdw1 $
# $Date: 2015/08/07 12:55:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import pixelselectionmethod
from ooflib.common import subthread
from ooflib.common import thread_enable
from ooflib.common.IO import voxelregionselectiondisplay
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import pixelselectparamwidgets
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
import gtk
import math

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# selmethodGUIdict is a dictionary which stores the SelectionMethodGUI
# subclasses for each type of selection method. For a given subclass
# of SelectionMethodGUI, the key in the dictionary is the associated
# subclass of pixelselectionmethod.SelectionMethod:
# RectangularPrismSelector, SphereSelector, etc.

selmethGUIdict = {}

class SelectionMethodGUIMetaClass(type):
    def __init__(cls, name, bases, dct):
        super(SelectionMethodGUIMetaClass, cls).__init__(name, bases, dct)
        try:
            targetName = dct['targetName']
        except KeyError:
            pass
        else:
            selmethGUIdict[targetName] = cls

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Subclasses of SelectionMethodGUI are in charge of managing what
# state a particular tool for selecting regions of pixels (or voxels)
# is in, and they also act as MouseHandlers for that particular tool.

# Some selection methods/tools (e.g. that to select a rectangular
# prism of voxels) require the user to perform multiple steps
# (e.g. create a new box-shaped region, edit that region using the
# mouse, finish editing the region and finally select all voxels
# within that region). Therefore, we must somehow keep track of which
# step the user is currently performing. It makes sense to have this
# tracking done by an object that is registered with (but separate
# from) the PixelSelectToolboxGUI that the user is working with, and
# to have this object's class associated with the selection
# method/tool whose GUI it is managing.  So, we let this object be an
# instance of a certain SelectionMethodGUI subclass, and we associate
# each subclass of SelectionMethodGUI
# (e.g. RectangularPrismSelectorGUI) with a subclass of
# SelectionMethod (e.g. RectangularPrismSelector) using the dictionary
# selmethGUIdict.

class SelectionMethodGUI(mousehandler.MouseHandler):
    # Base class for RectangularPrismSelectorGUI, SphereSelectorGUI,
    # etc.
    __metaclass__ = SelectionMethodGUIMetaClass
    def __init__(self, gfxwindow):
        self.gfxwindow = gfxwindow
    
    def __call__(self, params, scope=None, name=None, verbose=False):
        # This function should be redefined for derived classes.  It
        # should return a ParameterWidget of some sort.
        pass
    
    def cancel(self):
        # This function should be redefined for derived classes. It
        # should be used to notify a SelectionMethodGUI to cancel any
        # subthreads it started, and should be called when the
        # SelectionMethodGUI's toolboxGUI is being closed.
        pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# TODO: Have the done function in RectangularPrismSelectorGUI call the
# menu item to select a rectangular-prism-shaped region of
# voxels. Right now, we just have a little click-and-drag-able curio
# that does nothing useful.

# TODO: Allow the user to adjust the box by selecting edges and
# corners too (see TODOs in common/IO/canvaslayer.C for some of the
# BoxWidgetLayer functions).

class RectangularPrismSelectorGUI(SelectionMethodGUI):
    targetName = pixelselectionmethod.RectangularPrismSelector
    def __init__(self, gfxwindow):
        SelectionMethodGUI.__init__(self, gfxwindow)
        self.widget = None

        # ID of the vtk cell currently being edited.
        self.cellID = None

        # The VoxelRegionSelectionDisplay layer that's being updated.
        self.layer = None

        # Previous position, in display coordinates, of the mouse.
        self.last_x = None
        self.last_y = None

        # eventlist is a queue of events that have occurred.  datalock
        # is an EventLogSLock on the data in eventlist. The lock is
        # acquired and released from the mainthread in the down, up,
        # and move mouse callbacks using the
        # logNewEvent_acquire/release functions. The mainthread adds
        # down, up, and move events to the queue. When new events are
        # logged, the lock is acquired and released from an
        # event-processing subthread using the
        # handleNewEvents_acquire/release functions. This
        # event-processing subthread handles determining what has been
        # clicked on, making changes to the display layer, and
        # updating the graphics in time with the events being
        # processed.
        self.datalock = lock.EventLogSLock()
        self.eventlist = []

        # This flag will be True whenever the user is currently using
        # the mouse on the canvas to edit the dimensions of the box
        # enclosing the voxels to be selected. The flag will be set to
        # False again once the user has pressed the 'Done' button.
        self.region_editing_in_progress = False

        # Indicates whether the mouse has been clicked down or not.
        self.downed = False

        # Start the event-processing subthread.  See the comment in
        # viewertoolbox3dGUI.py about why execute_immortal is used
        # here.
        if thread_enable.query():
            self.eventThread = subthread.execute_immortal(
                self.processEvents_subthread)
        else:
            self.eventThread = None
        
    def __call__(self, params, scope=None, name=None, verbose=False):
        # This function creates a VoxelRegionSelectWidget and
        # returns it.
        ## TODO: Give this function a real name.
        self.widget = pixelselectparamwidgets.VoxelRegionSelectWidget(
            self, params, scope=scope, name=name, verbose=verbose)
        return self.widget

    def done(self):
        self.datalock.logNewEvent_acquire()
        try:
            self.region_editing_in_progress = False
            switchboard.notify("region editing finished", self.gfxwindow)
            self.gfxwindow.oofcanvas.render()
        finally:
            self.datalock.logNewEvent_release()

    def start(self):
        self.region_editing_in_progress = True
        switchboard.notify("region editing begun", self.gfxwindow)
        self.gfxwindow.oofcanvas.render()

    def up(self, x, y, button, shift, ctrl):
        self.downed = False
        self.datalock.logNewEvent_acquire()
        try:
            self.downed = False
            self.eventlist.append(('up', x, y, shift, ctrl))
        finally:
            self.datalock.logNewEvent_release()

    def down(self, x, y, button, shift, ctrl):
        self.datalock.logNewEvent_acquire()
        try:
            self.downed = True
            if self.region_editing_in_progress:
                self.eventlist.append(('down', x, y, shift, ctrl))
        finally:
            self.datalock.logNewEvent_release()

    def move(self, x, y, button, shift, ctrl):
        self.datalock.logNewEvent_acquire()
        try:
            if not self.eventlist:
                # All events have been processed so far. Append the
                # new move event to the list.
               self.eventlist.append(('move', x, y, shift, ctrl))
            elif self.eventlist[-1][0] == 'down':
                # Previous event was a down event. Append the new move
                # event to the list.
                self.eventlist.append(('move', x, y, shift, ctrl))
            elif self.eventlist[-1][0] == 'move':
                # Previous event was a move event. Overwrite that
                # event with the new move event.
                self.eventlist[-1] = ('move', x, y, shift, ctrl)
        finally:
            self.datalock.logNewEvent_release()
    
    def processUp(self):
        # Commands which need to be run when an 'up' event is being
        # processed.
        self.last_x = None
        self.last_y = None
        self.layer = None
        self.cellID = None
        return
        
    def processDown(self, x, y):
        # Commands which need to be run when a 'down' event is being
        # processed.
        viewobj = mainthread.runBlock(self.gfxwindow.oofcanvas.get_view)
        point = mainthread.runBlock(self.gfxwindow.oofcanvas.display2Physical,
                                    (viewobj, x, y))
        (self.cellID, click_pos, self.layer) = \
               self.gfxwindow.findClickedCellIDByLayerClass_nolock(
                   voxelregionselectiondisplay.VoxelRegionSelectionDisplay,
                   point, viewobj)
        self.last_x = x;
        self.last_y = y;

    def processMove(self, x, y):
        viewobj = mainthread.runBlock(self.gfxwindow.oofcanvas.get_view)
        last_mouse_coords = mainthread.runBlock(
            self.gfxwindow.oofcanvas.display2Physical, (viewobj, self.last_x,
                                                        self.last_y))
        mouse_coords = mainthread.runBlock(
            self.gfxwindow.oofcanvas.display2Physical, (viewobj, x, y))
        diff = mouse_coords - last_mouse_coords
        diff_size = math.sqrt(diff ** 2)
        if diff_size == 0:
            return
        diff = diff / diff_size
        normal = self.layer.canvaslayer.get_cellNormal_Coord3D(self.cellID)
        if (normal is None):
            return
        center = self.layer.canvaslayer.get_cellCenter(self.cellID)
        camera_pos = mainthread.runBlock(
            self.gfxwindow.oofcanvas.get_camera_position_v2)
        dist = math.sqrt((camera_pos - center) ** 2)
        view_angle = mainthread.runBlock(
            self.gfxwindow.oofcanvas.get_camera_view_angle)
        canvas_size = mainthread.runBlock(self.gfxwindow.oofcanvas.get_size)
        offset = (diff.dot(normal) * dist * math.tan(math.radians(view_angle))
                  * math.sqrt((x - self.last_x) ** 2 +
                              (y - self.last_y) ** 2) / canvas_size[1])
        
        # Update the canvaslayer.
        self.layer.canvaslayer.offset_cell(self.cellID, offset)
        self.layer.canvaslayer.setModified()

        self.last_x = x;
        self.last_y = y;
        mainthread.runBlock(self.gfxwindow.oofcanvas.render)

    def processEvents_subthread(self):
        while (True):
            self.datalock.handleNewEvents_acquire()
            try:
                if not self.eventlist:
                    continue
                (eventtype, x, y, shift, ctrl) = self.eventlist.pop(0)
            finally:
                self.datalock.handleNewEvents_release()
            if eventtype == "exit":
                return
            
            # Acquire the gfxlock so that we can be sure that the
            # gfxwindow is not in the middle of being changed or
            # closed at this time.
            self.gfxwindow.acquireGfxLock()
            try:
                if eventtype is 'down':
                    self.processDown(x, y)
                elif eventtype is 'move' and (self.cellID is not None):
                    self.processMove(x, y)
                elif eventtype is 'up':
                    self.processUp()
            finally:
                self.gfxwindow.releaseGfxLock()

    def cancel(self):
        if self.eventThread is not None:
            self.datalock.logNewEvent_acquire()
            try:
                ## TODO: See TODO in similar code in viewertoolbox3dGUI.py.
                self.eventlist = [('exit', None, None, None, None)]
            finally:
                self.datalock.logNewEvent_release()
            self.eventThread.join()
        
    def acceptEvent(self, eventtype):
        return (eventtype == 'down' or
                (self.region_editing_in_progress and self.downed and
                 (eventtype in ('move', 'up'))))
        
        
   
                                      
    
