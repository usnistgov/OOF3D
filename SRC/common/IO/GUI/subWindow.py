# -*- python -*-
# $RCSfile: subWindow.py,v $
# $Revision: 1.42.2.3 $
# $Author: langer $
# $Date: 2014/10/17 21:48:05 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Base class for daughter windows of the main application window.
# This class catches the parent window's destroy signal, and
# calls the local destroy() function, which in turn destroys
# self.gtk, unless overridden.
#
# If you either override or pass in a callback, it should take two
# arguments.  The first will be "self" and the second will be the
# window emitting the signal (i.e. top.gtk).

# Construct the menu for the window's menubar.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import guitop
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO.GUI import gfxmenu
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import quit 
import gtk
import types

class SubWindow:
    # Base class for non-modal windows which want to be destroyed when
    # the main OOF GUI window, which from here is guitop.top().gtk, gets
    # destroyed.
    def __init__(self, title, menu=None, callback=None, guiloggable=True):
        debug.mainthreadTest()
        self.gtk = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.gtk.set_title(title)
        if guiloggable:
            gtklogger.newTopLevelWidget(self.gtk, title)
            gtklogger.connect_passive(self.gtk, 'delete-event')
            gtklogger.connect_passive(self.gtk, 'configure-event')
        self.mainbox = gtk.VBox()
        self.gtk.add(self.mainbox)

        # Checking the type is clumsy; the idea is that the caller
        # must provide either the name for the auto-generated menu, or
        # a menu to use instead.  TODO 3.1: It would be cleaner for
        # the Activity Viewer if the SubWindow class could provide the
        # window-specific (i.e "Close" and "Quit") menu items under
        # "File" (creating it, if necessary, and prepending it to the
        # passed-in menu) even when a menu is passed in.  This would
        # prevent duplication of effort by separate subclasses of
        # subwindow.
        if type(menu)==types.StringType:
            # If no menu is provided, then build a non-logging local
            # one with 'Close' and 'Quit'.
            self.subwindow_menu = oofmenu.OOFMenuItem(
                menu, secret=1, gui_only=1, no_log=1)

            file_item = oofmenu.OOFMenuItem('File', gui_only=1, no_log=1)
            self.subwindow_menu.addItem(file_item)

            file_item.addItem(oofmenu.OOFMenuItem(
                'Close', help="Close this window.",
                callback=self.menu_close,
                no_log=1, gui_only=1, accel='w'))
            
            file_item.addItem(oofmenu.OOFMenuItem(
                'Quit', gui_callback=quit.queryQuit,
                no_log=1, gui_only=1,
                help="Quit the OOF application.",
                accel='q', threadable = oofmenu.UNTHREADABLE))
                              
            mainmenu.OOF.addItem(self.subwindow_menu)
            self._local_menu = menu
        elif isinstance(menu, oofmenu.OOFMenuItem):
            self.subwindow_menu = menu
            self._local_menu = None # Flag indicating menu was passed in.
        else:
            raise TypeError("Incorrect type passed as menu to SubWindow.")

        # Build the menu bar and add it to the window.
##        self.menu_bar = None
        self.accel_group = gtk.AccelGroup()
        self.gtk.add_accel_group(self.accel_group)
        self.menu_bar = gfxmenu.gtkOOFMenuBar(
            self.subwindow_menu, accelgroup=self.accel_group)
        if guiloggable:
            gtklogger.setWidgetName(self.menu_bar, "MenuBar")

        self.mainbox.pack_start(self.menu_bar, fill=0, expand=0)

        # Add the "Windows" menu to the bar.
        self.windows_gtk_menu_item = gfxmenu.gtkOOFMenu(mainmenu.OOF.Windows,
                                                        self.accel_group)
        self.menu_bar.append(self.windows_gtk_menu_item)

        self.menu_bar.connect("destroy", self.menu_bar_destroyed)
        
        if callback is None:
            callback = self.destroySubWindow
        guitop.top().gtk.connect("destroy", callback)

    # It is assumed, here, that if the menu bar has been destroyed,
    # the destruction of the SubWindow wrapper object is imminent,
    # so it's safe to cut the menu loose.
    def menu_bar_destroyed(self, gtk):
        if self._local_menu:
            # Disconnect the menu.
            self.subwindow_menu.clearMenu()
            mainmenu.OOF.removeItem(self._local_menu)
            self.subwindow_menu = None
    
    # Default close routine, callback for the default menu item.
    def menu_close(self, menuitem):
        mainthread.runBlock(self.close_thread)
    def close_thread(self):
        debug.mainthreadTest()
        self.gtk.destroy()

    def destroySubWindow(self, *args):
        debug.mainthreadTest()
        if self.gtk:
            self.gtk.destroy()
            self.gtk = 0

    # This takes arguments so it can be used as a callback.
    def raise_window(self, *args):
        debug.mainthreadTest()
        self.gtk.window.raise_()

# used by several of the subwindows for naming window.
def oofname():
    if config.dimension() == 2:
        return "OOF2"
    elif config.dimension() == 3:
        return "OOF3D"
    



