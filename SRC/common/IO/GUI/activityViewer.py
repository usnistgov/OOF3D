# -*- python -*-
# $RCSfile: activityViewer.py,v $
# $Revision: 1.44.2.5 $
# $Author: fyc $
# $Date: 2014/07/22 17:56:20 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## The Activity Viewer window contains progress bar objects, which are
## defined in progressbarGUI.py.

## TODO 3.1: Put progress bars at the bottom of the Message window,
## and don't have a separate Activity Viewer window.

from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import progress
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import thread_enable
from ooflib.common import threadmanager
from ooflib.common.IO import activityviewermenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import progressbar_delay
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import quit
from ooflib.common.IO.GUI import subWindow
import gobject
import gtk
import string
import sys
import time

activityViewer = None

## Has the Activity Viewer been opened?  If the Activity Viewer has
## already been opened, even if it's not open anymore, it's not opened
## automatically (by updatePBdisplay, below).
_activityViewerOpened = False

def openActivityViewer():
    debug.mainthreadTest()
    global activityViewer
    global _activityViewerOpened
    if activityViewer is None:
        activityViewer = ActivityViewer()
    activityViewer.raise_window()
    _activityViewerOpened = True

def sensitize():
    mainthread.runBlock(sensitize_thread)
def sensitize_thread():
    if activityViewer is not None:
        activityViewer.sensitizeButtons()
    
        
class ActivityViewer(subWindow.SubWindow):
    def __init__(self):
        debug.mainthreadTest()
        self.listofgtkbars = []
        self.makeMenus()  # Sets self.menu.
        # SubWindow init sets self.gtk and self.mainbox.
        
        subWindow.SubWindow.__init__(
            self, title="%s Activity Viewer"%subWindow.oofname(),
            menu=self.menu)

        self.gtk.connect('destroy', self.closeCB)
        self.gtk.set_default_size(400, 300)
        
        # Area at the top containing the editor widget for the line
        self.control_area = gtk.HBox()       # editor widget goes in here
        self.mainbox.pack_start(self.control_area, expand=0, fill=0, padding=2)

        ## Dismiss All bars
        self.dismissall = gtkutils.StockButton(gtk.STOCK_CANCEL, "Dismiss All")
        gtklogger.setWidgetName(self.dismissall, "DismissAll")
        gtklogger.connect(self.dismissall, "clicked", self.dismissAllCB)
        self.control_area.pack_start(self.dismissall, expand=1, fill=0,
                                     padding=2)

        ## stop-all-threads
        self.stopall = gtkutils.StockButton(gtk.STOCK_STOP, "Stop All")
        gtklogger.setWidgetName(self.stopall, "StopAll")
        gtklogger.connect(self.stopall, "clicked", self.stopAll)
        self.control_area.pack_start(self.stopall, expand=1, fill=0, padding=2)
                
        # Create a scrolled window to pack the bars into
        scrolled_window = gtk.ScrolledWindow()
        scrolled_window.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        gtklogger.logScrollBars(scrolled_window, "Scroll")
        self.mainbox.pack_start(scrolled_window, expand=1, fill=1, padding=2)
        
        ## Create VBox where the progressbars can live happily ever after
        self.bars_play_area = gtk.VBox() # homogeneous=True?
        scrolled_window.add_with_viewport(self.bars_play_area)

        self.proglock = lock.SLock()
        self.proglock.acquire()
        try:
            for worker in threadmanager.threadManager.allWorkers():
                worker.threadstate.acquireProgressLock()
                try:
                    progressnames = worker.threadstate.getProgressNames()
                    for pname in progressnames:
                        try:
                            prgrss = worker.threadstate.findProgress(pname)
                        except ooferror.ErrNoProgress:
                            # Progress object already finished
                            pass
                        else:
                            if prgrss.started():
                                self.installBar(prgrss)
                finally:
                    worker.threadstate.releaseProgressLock()
        finally:
            self.proglock.release()

        self.gtk.show_all()
        self.sensitizeButtons()


    def installBar(self, prgrss):
        debug.mainthreadTest()
        if not prgrss.hasProgressBar():
            pbar = prgrss.makeGUIBar()
            self.listofgtkbars.append(pbar)
            self.bars_play_area.pack_start(pbar.gtk, expand=0, fill=0,
                                           padding=2)
            pbar.updateGUI()
            pbar.show()
            pbar.schedule()

    def sensitizeButtons(self):
        debug.mainthreadTest()
        nrunning = 0
        nstopped = 0
        for pbar in self.listofgtkbars:
            if pbar.halted():
                nstopped += 1
            else:
                nrunning += 1
        self.stopall.set_sensitive(nrunning > 0)
        self.dismissall.set_sensitive(nstopped > 0)
            
    def dismissAllCB(self, button):
        completedbars = [bar for bar in self.listofgtkbars if bar.halted()]
        for bar in completedbars:
            bar.destroy()
        self.sensitizeButtons()

    def stopAll(self, button):
        threadmanager.threadManager.stopAll()
        self.sensitizeButtons()

    def dismissGTKBar(self, bar):
        debug.mainthreadTest()
        self.proglock.acquire()
        try:
            self.listofgtkbars.remove(bar)
        finally:
            self.proglock.release()
        self.sensitizeButtons()

    def makeMenus(self): ## Adds quit Button
        self.menu = activityviewermenu.activityviewermenu
        # Because we have our own submenu, these are not automatically
        # added in the SubWindow class. 
        self.menu.File.addItem(oofmenu.OOFMenuItem(
            'Close', help="Close this Activity Viewer window.",
            callback=self.close, no_log = 1, gui_only = 1, accel='w',
            threadable = oofmenu.UNTHREADABLE))
        self.menu.File.addItem(oofmenu.OOFMenuItem(
            'Quit', help="TTFN",
            callback=quit.queryQuit, no_log = 1, gui_only = 1, accel='q',
            threadable = oofmenu.UNTHREADABLE))
    
    def closeCB(self, *args):           # GTK callback.
        if activityViewer:
            activityviewermenu.activityviewermenu.File.Close()
            
    def close(self, *args):             # Main-thread menu callback.
        debug.mainthreadTest()
        global activityViewer
        if activityViewer:
            self.gtk.hide()
            # bar.disconnect() must be called for each bar before
            # setting activityViewer to None.  The disconnected bar
            # will be removed from listofgtkbars, so we have to loop
            # over a copy of the list.
            for bar in self.listofgtkbars[:]:
                bar.disconnect()
            # Setting activityViewer to None before destroying the gtk
            # objects prevents this function from being called
            # recursively.
            activityViewer = None
            self.gtk.destroy()
            self.gtk = None

    ## Add a gtkprogressbar to the scrolled window.
    def addGTKBar (self, prgrss):
        debug.mainthreadTest()
        # Because the window initializes itself with all existing
        # Progress objects, and because there's a delay between
        # creating a Progress object and opening the window, it's
        # possible that addGTKBar will be called for an object that
        # already has a bar.
        self.proglock.acquire()
        try:
            self.installBar(prgrss)
            self.sensitizeButtons()
        finally:
            self.proglock.release()

    #####################################################

# Display a new progress bar after a short delay, unless the delay
# time is less than the normal time between progress bar updates, in
# which case display the bar immediately.  The delay suppresses
# short-lived progress bars which wouldn't be very useful anyway.

def delayed_add_ProgressBar(progressid):
    debug.mainthreadTest()
    if thread_enable.query():
        if progressbar_delay.delay < progressbar_delay.period:
            _updatePBdisplayNow(progressid) # immediate display
        else:
            gobject.timeout_add(progressbar_delay.delay,
                                _updatePBdisplay, progressid)

# Time-out callback function invoked by delayed_add_ProgressBar.

def _updatePBdisplay(progressid):
    gtk.gdk.threads_enter()
    try:
        _updatePBdisplayNow(progressid)
    finally:
        gtk.gdk.threads_leave()
    return False

def _updatePBdisplayNow(progressid):
    debug.mainthreadTest()
    # Don't do anything unless threads are enabled and the gui has
    # been started.
    if thread_enable.query() and guitop.top():
        prog = progress.findProgressByID(progressid)
        if prog is not None and not (prog.finished() or prog.stopped()):
            # Create just one activity viewer.  If it's been opened
            # and closed already, don't reopen it automatically.
            if not _activityViewerOpened:
                # The newly created Activity Viewer window
                # automatically calls installBar for every existing
                # Progress object, including the one identified by the
                # argument to this routine.
                openActivityViewer()
            else:
                # The Activity Viewer might have been closed, in which
                # case activityViewer is None.
                if activityViewer is not None:
                    activityViewer.addGTKBar(prog)

switchboard.requestCallbackMain("new progress", delayed_add_ProgressBar)
