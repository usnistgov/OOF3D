# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# TODO 3.1: The GfxWindowManager maybe should be replaced with a set of
# switchboard callbacks.  There's not really any need for it any more,
# except for naming the windows.

from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import subthread
from ooflib.common import utils
from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import lock
import sys

class GfxWindowManager:
    def __init__(self):
        # Lock to protect potentially-shared data.  It's an SLock
        # because getWindow can be called on the main thread.
        self.lock = lock.SLock()
        self.windows = []
        self.count = 0
    def openWindow(self, **kwargs):
        self.lock.acquire()
        try:
            self.count += 1
            count = self.count
            name = 'Graphics_' + `count`
            w = self._newWindow(name, **kwargs) # opens real or ghost gfx window
            self.windows.append(w)
        finally:
            self.lock.release()
        switchboard.notify('open graphics window', w)
        return w
    
    def _newWindow(self, name, **kwargs):
        # This function is redefined if the GUI is loaded.
        from ooflib.common.IO import ghostgfxwindow
        window = ghostgfxwindow.GhostGfxWindow(name, self, **kwargs)
        # Although there's no GUI and the graphics window won't
        # actually appear, it's necessary to pretend to draw it here
        # so that the internal state of the GhostGfxWindow is the same
        # as it would be in GUI mode.  Skipping this step could make
        # scripts behave differently in GUI and text modes.
        window.drawAtTime(window.displayTime)
        return window

    def closeWindow(self, w):
        # This doesn't actually close the window, it just does some
        # bookkeeping that has to be done when a window is closed.  It
        # removes the window from the GfxWindowManager's list of
        # windows, and marks the window as closed, so that it doesn't
        # try to repeat this call when it gets its gtk.destroy signal.
        # You can't just not make the call in that case, because
        # gtk.destroy can be sent either by the window manager, when
        # the window is closed, or at exit-time.
        w.closed = 1
        self.lock.acquire()
        try:
            self.windows.remove(w)
            if len(self.windows) == 0:
                self.count = 0
        finally:
            self.lock.release()
        switchboard.notify('close graphics window', w)

    def closeAllWindows(self):
        # Calling GhostGfxWindow.close will call
        # GfxWindowManager.closeWindow to remove the window from
        # self.windows, so loop over a copy of the list.
        from ooflib.common.IO import mainmenu
        for win in self.windows[:]:
            # Call the window's "Close" menu item callback.
            menuitem = getattr(mainmenu.OOF, win.name).File.Close
            menuitem.callWithDefaults()

    def getWindow(self, name):
        result = None
        self.lock.acquire()
        try:
            for window in self.windows:
                if window.name == name:
                    result = window
                    break
        finally:
            self.lock.release()
        if result is None:
            raise KeyError("No such window: " + `name`)
        return result
    def getAllWindows(self):
        return self.windows[:]


gfxManager = GfxWindowManager()

