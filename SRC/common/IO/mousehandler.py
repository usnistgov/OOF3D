# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.common import subthread

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# A GfxWindow always has a current MouseHandler, which knows what to
# do with mouse events on the canvas.  The window's toolboxes can
# install new MouseHandlers.  The base class defined here does
# nothing.  Toolboxes can themselves be subclasses of MouseHandler, or
# they can use one of the classes defined below.


class MouseHandler(object):
    def __init__(self, gfxwindow, toolbox):
        self.gfxwindow = gfxwindow
        self.toolbox = toolbox
    def acceptEvent(self, eventtype):
        # eventtype is either 'up', 'down', or 'move'.  Return True if it
        # can be handled.
        # Locked only the three events 
        if eventtype == 'up' or eventtype == 'down' or eventtype == 'move':
	  return True
	else:
	  return False
    def up(self, x, y, button, shift, ctrl):
        pass
    def down(self, x, y, button, shift, ctrl):
        pass
    def move(self, x, y, button, shift, ctrl):
        pass
    def start(self):
        pass
    def stop(self):
        pass

class NullMouseHandler(MouseHandler):
    def acceptEvent(self, eventtype):
        return False
    
nullHandler = NullMouseHandler()            # doesn't do anything

# SingleClickMouseHandler just uses the location of the mouse-up
# event, if a mouse-down event was detected earlier.  Subclasses must
# define doUp().

class SingleClickMouseHandler(MouseHandler):
    def __init__(self, gfxwindow, guitoolbox):
        MouseHandler.__init__(self, gfxwindow, guitoolbox)
        self.downed = False
        self.button_down = None
        self.shift_down = None
        self.ctrl_down = None
    def acceptEvent(self, event):
        return event in ("up", "down")
    def down(self, x, y, button, shift, ctrl):
        self.button_down = button
        self.shift_down = shift
        self.ctrl_down = ctrl
        self.downed = True
    def up(self, x, y, button, shift, ctrl):
        if self.downed:
            self.doUp(x, y, self.button_down, self.shift_down, self.ctrl_down,
                    self.gfxwindow)
        self.downed = False


# Threaded mouse handler stores events on a queue and processes them
# on a thread.  This give smoother handling if there's non-trivial
# drawing to be done in response.
    
class ThreadedMouseHandler(object):
    def __init__(self, guitoolbox, eventtypes):
        # guitoolbox doesn't have to be a toolbox, it can be some
        # other object that knows how to respond to mouse events.
        self.guitoolbox = guitoolbox # Toolboxes can't share a mouse handler!
        self.eventtypes = eventtypes # tuple containing "up", "down", "move"
        for event in eventtypes:
            assert event in ("up", "down", "move")
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
    def acceptEvent(self, eventtype):
        return eventtype in self.eventtypes
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
        assert self.eventThread is not None
        self.datalock.logNewEvent_acquire()
        try:
            self.eventlist = [MouseTrap()]
        finally:
            self.datalock.logNewEvent_release()
        self.eventThread.join()
        self.eventThread = None

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

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Mouse events stored in the ThreadedMouseHandlers' queue.

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

            
