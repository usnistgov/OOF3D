# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import toolbox
from ooflib.common import primitives
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import widgetscope
import gtk
import sys

class GfxToolbox(widgetscope.WidgetScope):
    def __init__(self, toolbox):
        debug.mainthreadTest()
        self.toolbox = toolbox          # non-GUI toolbox
        self.gtk = gtk.Frame()          # root of toolbox's gtk widget tree
        gtklogger.setWidgetName(self.gtk, self.toolbox.displayName())
        self.gtk.set_shadow_type(gtk.SHADOW_NONE)
        self.active = 0
        widgetscope.WidgetScope.__init__(self, parent=None)
    def name(self):
        return self.toolbox.name()
    def displayName(self):
        return self.toolbox.displayName()
    def close(self):
        pass

    def activate(self):
        ## TODO: active should only be in the Toolbox class.  No need
        ## to store it in GfxToolbox as well.  There may be places in
        ## the code that assume it's in GfxToolbox, which should be
        ## changed.
        self.active = True
        self.toolbox.active = True
        switchboard.notify("toolbox activated " + self.name(),
                           self.toolbox.gfxwindow())
    def deactivate(self):
        self.active = False
        self.toolbox.active = False
        switchboard.notify("toolbox deactivated " + self.name(),
                           self.toolbox.gfxwindow())
    def gfxwindow(self):
        return self.toolbox.gfxwindow()
    def installMouseHandler(self):
        # The default mouse handler is no mouse handler.  Subclasses
        # should override this if they need to handle mouse clicks on
        # the canvas when the window is in "select" mode.
        self.gfxwindow().removeMouseHandler()
        
    def __cmp__(self, other):           # for sorting in gfxwindow's list
        return cmp(self.toolbox.ordering, other.toolbox.ordering)

    # # convenience function to get a point object from mouseclick coordinates
    # def getPoint(self, x, y):
    #     if config.dimension() == 2:
    #         return primitives.Point(x,y)
    #     elif config.dimension() == 3:
    #         p = self.gfxwindow().oofcanvas.screen_coords_to_3D_coords(x,y) 
    #         if p:
    #             return primitives.Point(p[0],p[1],p[2])
    #         else:
    #             return None

# The base Toolbox class doesn't make a GUI, but it provides a trivial
# makeGUI function so that derived toolboxes that don't create a GUI
# don't have to define makeGUI themselves.

def _makeGUI(self):
    pass

toolbox.Toolbox.makeGUI = _makeGUI

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Toolboxes can use these classes for mouse handling.  They set up a
# mouse handling queue, which provides smoother processing than just
# calling the mouse callbacks directly, if the graphics window needs
# to do some computation.

class MouseEvent(object):
    def __init__(self, x, y, button, shift, ctrl):
        self.x = x
        self.y = y
        self.button = button
        self.shift = shift
        self.ctrl = ctrl

class MouseDown(MouseEvent):
    def process(self, guitoolbox):
        guitoolbox.down(self.x, self.y, self.button, self.shift, self.ctrl)
        return True

class MouseUp(MouseEvent):
    def process(self, guitoolbox):
        guitoolbox.up(self.x, self.y, self.button, self.shift, self.ctrl)
        return True

class MouseMove(MouseEvent):
    def process(self, guitoolbox):
        guitoolbox.move(self.x, self.y, self.button, self.shift, self.ctrl)
        return True

class MouseTrap(MouseEvent):
    def __init__(self):
        pass
    def process(self, guitoolbox):
        return False

# Threaded mouse handler stores events on a queue and processes them
# on a thread.  This give smoother handling if there's non-trivial
# drawing to be done in response.
    
class ThreadedMouseHandler(object):
    def __init__(self, guitoolbox):
        self.guitoolbox = guitoolbox # Toolboxes can't share a mouse handler!
        self.eventlist = []
        self.datalock = lock.EventLogSLock()
        self.downed = False
        self.eventThread = None
        # The modifier keys are detected when the mouse button is
        # pressed, but are stored here so that the toolboxes don't
        # have to remember them for processing when the mouse is
        # released.
        self.button_down = None
        self.shift_down = None
        self.ctrl_down = None
    def clear(self):
        self.datalock.logNewEvent_acquire()
        try:
            self.eventlist = []
            self.downed = False
        finally:
            self.datalock.logNewEvent_release()
    def down(self, x, y, button, shift, ctrl):
        self.datalock.logNewEvent_acquire()
        try:
            self.downed = True
            self.button_down = button
            self.shift_down = shift
            self.ctrl_down = ctrl
            self.eventlist.append(MouseDown(x, y, button, shift, ctrl))
        finally:
            self.datalock.logNewEvent_release()
    def up(self, x, y, button, shift, ctrl):
        self.datalock.logNewEvent_acquire()
        try:
            self.downed = False
            self.eventlist.append(MouseUp(x, y, self.button_down,
                                          self.shift_down, self.ctrl_down))
        finally:
            self.datalock.logNewEvent_release()
    def move(self, x, y, button, shift, ctrl):
        self.datalock.logNewEvent_acquire()
        try:
            self.eventlist.append(MouseMove(x, y, self.button_down,
                                            self.shift_down, self.ctrl_down))
        finally:
            self.datalock.logNewEvent_release()

    def start(self):
        assert self.eventThread is None
        # This thread is shut down when cancel method is called which
        # happens when the toolbox is closed or switched to a
        # different mode.  It's started with execute_immortal instead
        # of just execute to avoid a race condition at shutdown time,
        # in which the window can be closing at the same time as the
        # miniThreadManager is shutting down threads.  Threads started
        # with execute_immortal aren't shut down by the
        # miniThreadManager.
        self.eventThread = subthread.execute_immortal(
            self.processEvents_subthread)

    def stop(self):
        self.datalock.logNewEvent_acquire()
        try:
            self.eventlist = [MouseTrap()]
        finally:
            self.datalock.logNewEvent_release()
        self.eventThread.join()

    def processEvents_subthread(self):
        while True:
            self.datalock.handleNewEvents_acquire()
            try:
                event = self.eventlist.pop(0)
            finally:
                self.datalock.handleNewEvents_release()
            # process returns False if the thread should exit
            if not event.process(self.guitoolbox):
                return


# KangarooMouseHandler is just like ThreadedMouseHandler but if move
# events accumulate in the queue, the mouse jumps to the latest
# position.  It should be used in cases where the intermediate points
# will be used to update the display but otherwise aren't important.

class KangarooMouseHandler(ThreadedMouseHandler):
    def move(self, x, y, button, shift, ctrl):
        self.datalock.logNewEvent_acquire()
        try:
            if self.eventlist and isinstance(self.eventlist[-1], MouseMove):
                self.eventlist[-1] = MouseMove(x, y)
            else:
                self.eventlist.append(MouseMove(x, y))
        finally:
            self.datalock.logNewEvent_release()
