# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import lock
from ooflib.common import debug
from ooflib.common import subthread

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# MouseButtons stores which mouse button was pressed and the state of
# the modifier keys at the time.  For each event, GfxWindow3D.mouseCB
# creates a MouseButtons object and passes it to the MouseHandler's
# up, down, or move method.

class MouseButtons(object):
    def __init__(self, button=None, shift=None, ctrl=None):
        self.button = button
        self.shift = shift
        self.ctrl = ctrl

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# A GfxWindow always has a current MouseHandler, which knows what to
# do with mouse events on the canvas.  The window's toolboxes can
# install new MouseHandlers.  The base class defined here does
# nothing.  Toolboxes can themselves be subclasses of MouseHandler, or
# they can use one of the classes defined below.

class MouseHandler(object):
    def __init__(self, nextHandler):
        self.nextHandler = nextHandler
        self.buttons = MouseButtons()
    def acceptEvent(self, eventtype):
        # eventtype is either 'up', 'down', or 'move'.  Return True if it
        # can be handled.
        return eventtype in ('up', 'down','move', 'modkeys')
    def up(self, x, y, buttons):
        pass
    def down(self, x, y, buttons):
        pass
    def move(self, x, y, buttons):
        pass
    def modkeys(self, buttons):
        pass
    # start() is called just after the handler is installed
    def start(self):
        pass
    # stop() is called when the handler is about to be uninstalled
    def stop(self):
        pass

class NullMouseHandler(MouseHandler):
    def __init__(self):
        pass
    def acceptEvent(self, eventtype):
        return False
    
nullHandler = NullMouseHandler()            # doesn't do anything

# SingleClickMouseHandler just uses the location of the mouse-up
# event, if a mouse-down event was detected earlier. 

class SingleClickMouseHandler(MouseHandler):
    def __init__(self, nextHandler):
        MouseHandler.__init__(self, nextHandler)
        self._downed = False
    def acceptEvent(self, event):
        return event in ("up", "down", "modkeys")
    def down(self, x, y, buttons):
        self.buttons = buttons
        self._downed = True
        subthread.execute(self.nextHandler.down, (x, y, buttons))
    def up(self, x, y, buttons):
        if self._downed:
            self._downed = False
            subthread.execute(self.nextHandler.up, (x, y, self.buttons))
    def modkeys(self, buttons):
        self.buttons = buttons
        subthread.execute(self.nextHandler.modkeys, (buttons,))

# Threaded mouse handler stores events on a queue and processes them
# on a thread.  This give smoother handling if there's non-trivial
# drawing to be done in response.
    
class ThreadedMouseHandler(MouseHandler):
    def __init__(self, nextHandler, eventtypes):
        # nextHandler doesn't have to be a toolbox, it can be some
        # other object that knows how to respond to mouse events.
        # eventtypes are the events that this reports to its caller.
        # It always gets all events from the canvas.
        MouseHandler.__init__(self, nextHandler)
        # eventtypes is a tuple containing some or all of "up",
        # "down", "move", and "modkeys".
        self.eventtypes = eventtypes
        for event in eventtypes:
            assert event in ("up", "down", "move", "modkeys")
        self.eventlist = []
        self.datalock = lock.EventLogSLock()
        self._downed = False
        self.eventThread = None
        # The modifier keys are detected when the mouse button is
        # pressed, but are stored here so that the toolboxes don't
        # have to remember them for processing when the mouse is
        # released.
        self.buttons = MouseButtons()

    def clear(self):
        self.datalock.logNewEvent_acquire()
        try:
            self.eventlist = []
            self._downed = False
        finally:
            self.datalock.logNewEvent_release()
    def acceptEvent(self, eventtype):
        return True
    def down(self, x, y, buttons):
        self.datalock.logNewEvent_acquire()
        try:
            self._downed = True
            self.buttons = buttons
            if 'down' in self.eventtypes:
                self.eventlist.append(MouseDown(x, y, self.buttons))
        finally:
            self.datalock.logNewEvent_release()
    def up(self, x, y, buttons):
        self.datalock.logNewEvent_acquire()
        try:
            self._downed = False
            if 'up' in self.eventtypes:
                self.eventlist.append(MouseUp(x, y, self.buttons))
        finally:
            self.datalock.logNewEvent_release()
    def move(self, x, y, buttons):
        if self._downed and 'move' in self.eventtypes:
            self.datalock.logNewEvent_acquire()
            try:
                self.eventlist.append(MouseMove(x, y, self.buttons))
            finally:
                self.datalock.logNewEvent_release()
    def modkeys(self, buttons):
        self.datalock.logNewEvent_acquire()
        try:
            self.eventlist.append(ModKeys(buttons))
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
        if self.eventThread is not None:
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
            # process returns False if the thread should exit.
            if not event.process(self.nextHandler):
                return

# KangarooMouseHandler is just like ThreadedMouseHandler but if move
# events accumulate in the queue, the mouse *jumps* to the latest
# position.  It should be used in cases where the intermediate points
# will be used to update the display but otherwise aren't important.

class KangarooMouseHandler(ThreadedMouseHandler):
    def move(self, x, y, buttons):
        if self._downed and 'move' in self.eventtypes:
            self.datalock.logNewEvent_acquire()
            try:
                mevent = MouseMove(x, y, self.buttons)
                if self.eventlist and isinstance(self.eventlist[-1], MouseMove):
                    self.eventlist[-1] = mevent
                else:
                    self.eventlist.append(mevent)
            finally:
                self.datalock.logNewEvent_release()


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Mouse events stored in the ThreadedMouseHandlers' queue.

class MouseEvent(object):
    def __init__(self, x, y, buttons):
        self.x = x
        self.y = y
        self.buttons = buttons
    def __repr__(self):
        return "%s(%d, %d)" % (self.__class__.__name__, self.x, self.y)

class MouseDown(MouseEvent):
    def process(self, nextHandler):
        nextHandler.down(self.x, self.y, self.buttons)
        return True

class MouseUp(MouseEvent):
    def process(self, nextHandler):
        nextHandler.up(self.x, self.y, self.buttons)
        return True

class MouseMove(MouseEvent):
    def process(self, nextHandler):
        nextHandler.move(self.x, self.y, self.buttons)
        return True

class ModKeys(MouseEvent):
    def __init__(self, buttons):
        self.buttons = buttons
    def process(self, nextHandler):
        nextHandler.modkeys(self.buttons)
        return True

class MouseTrap(MouseEvent):
    def __init__(self):
        pass
    def process(self, *args):
        return False
    def __repr__(self):
        return "MouseTrap()"
            
