# -*- python -*-
# $RCSfile: oofGUI.py,v $
# $Revision: 1.78.2.16 $
# $Author: langer $
# $Date: 2014/10/17 21:48:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import guitop
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import runtimeflags
from ooflib.common import thread_enable
from ooflib.common import utils
from ooflib.common.IO import gfxmanager
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gfxmenu
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import gtkutils
from ooflib.common.IO.GUI import historian
from ooflib.common.IO.GUI import mainthreadGUI
from ooflib.common.IO.GUI import quit
from ooflib.common.IO.GUI import tooltips
from ooflib.common.IO.GUI import widgetscope
import gtk
import ooflib.common.quit
import pango

allPages = {}                           # dictionary of pages keyed by name
pagenames = []                          # ordered list of pages

if config.dimension() == 2:
    oofname = "OOF2"
elif config.dimension() == 3:
    oofname = "OOF3D"

class oofGUI(widgetscope.WidgetScope):
    def __init__(self):
        debug.mainthreadTest()
        widgetscope.WidgetScope.__init__(self, None)
        self.gtk = gtk.Window(gtk.WINDOW_TOPLEVEL)
        self.gtk.set_title(oofname)
        initial_width, initial_height = map(int,
                                            runtimeflags.geometry.split('x'))
        self.gtk.set_default_size(initial_width, initial_height)
        gtklogger.newTopLevelWidget(self.gtk, oofname)
        gtklogger.connect(self.gtk, "delete-event", self.deleteEventCB)
        gtklogger.connect_passive(self.gtk, "configure-event")
        self.gtk.connect("destroy", self.destroyCB)
        guitop.setTop(self)

        self.mainbox = gtk.VBox()
        self.gtk.add(self.mainbox)

        self.menubar = gtk.MenuBar()
        self.mainbox.pack_start(self.menubar, expand=0, fill=0)
        accelgrp = gtk.AccelGroup()
        self.gtk.add_accel_group(accelgrp)

        self.mainmenu = mainmenu.OOF
        self.oofmenu = gfxmenu.gtkOOFMenuBar(self.mainmenu, bar=self.menubar,
                                             accelgroup=accelgrp)
        gtklogger.setWidgetName(self.oofmenu, "MenuBar")
        self.pageChooserFrame = gtk.Frame()
        self.pageChooserFrame.set_shadow_type(gtk.SHADOW_IN)
        self.mainbox.pack_start(self.pageChooserFrame,
                                expand=0, fill=0, padding=2)

        align = gtk.Alignment(xalign=0.5)
        self.pageChooserFrame.add(align)
        chooserBox = gtk.HBox()
        chooserBox.set_border_width(2)
        gtklogger.setWidgetName(chooserBox, 'Navigation')
        align.add(chooserBox)

        self.historian = historian.Historian(self.historianCB,
                                             self.sensitizeHistory)

        label = gtk.Label('Task: ')
        label.set_alignment(1.0, 0.5)
        chooserBox.pack_start(label, expand=0, fill=0)
        
        self.prevHistoryButton = gtkutils.StockButton(gtk.STOCK_GOTO_FIRST)
        chooserBox.pack_start(self.prevHistoryButton, expand=0, fill=0, 
                              padding=3)
        gtklogger.setWidgetName(self.prevHistoryButton, 'PrevHist')
        gtklogger.connect(self.prevHistoryButton, 'clicked', 
                          self.historian.prevCB)
        tooltips.set_tooltip_text(self.prevHistoryButton,
                     "Go to the chronologically previously page.")

        self.prevPageButton = gtkutils.StockButton(gtk.STOCK_GO_BACK)
        chooserBox.pack_start(self.prevPageButton, expand=0, fill=0, padding=3)
        gtklogger.setWidgetName(self.prevPageButton, 'Prev')
        gtklogger.connect(self.prevPageButton, 'clicked', self.prevPageCB)
        self.pageChooser = chooser.ChooserWidget([],
                                                 callback=self.pageChooserCB,
                                                 name="PageMenu")
        chooserBox.pack_start(self.pageChooser.gtk, expand=0, fill=0)
        self.currentPageName = None

        self.nextPageButton = gtkutils.StockButton(gtk.STOCK_GO_FORWARD)
        chooserBox.pack_start(self.nextPageButton, expand=0, fill=0, padding=3)
        gtklogger.setWidgetName(self.nextPageButton, 'Next')
        gtklogger.connect(self.nextPageButton, 'clicked', self.nextPageCB)

        self.nextHistoryButton = gtkutils.StockButton(gtk.STOCK_GOTO_LAST)
        chooserBox.pack_start(self.nextHistoryButton, expand=0, fill=0,
                              padding=3)
        gtklogger.setWidgetName(self.nextHistoryButton, 'NextHist')
        gtklogger.connect(self.nextHistoryButton, 'clicked',
                          self.historian.nextCB)
        tooltips.set_tooltip_text(self.nextHistoryButton,
                     "Go to the chronologically next page.")

        # Find the font size, so widgets can be sized appropriately.
        #  digitsize and charsize are in pixels.
        
        self.digitsize,self.charsize = gtkutils.widgetFontSizes(self.gtk)

        # Add a GUI callback to the "OOF2" or "OOF3D" windows item.
        oof_item = getattr(self.mainmenu.Windows, oofname)
        oof_item.add_gui_callback(self.menu_raise)

        # Frame around main pages.  GUI pages are added and removed
        # from it by installPage().
        self.pageframe = gtk.Frame()
        self.pageframe.set_shadow_type(gtk.SHADOW_IN)
        self.mainbox.pack_start(self.pageframe, expand=1, fill=1)

        # Add pages that may have been created before the main GUI was built.
        for pagename, i in zip(pagenames, range(len(allPages))):
            self.addPage(allPages[pagename], i)

    # def tooltip(self, widget, tip):
    #     ## TODO: This is deprecated.  Just call
    #     ## tooltips.set_tooltip_text() directly.
    #     debug.mainthreadTest()
    #     tooltips.set_tooltip_text(widget, tip)
    #     #widget.set_tooltip_text(tip)

    def installPage(self, pagename):
        debug.mainthreadTest()
        # Actually install a page in the page frame.
        oldPage = None
        if self.currentPageName is not None:
            oldPage = allPages[self.currentPageName]
            self.pageframe.remove(oldPage.gtk)
        self.currentPageName = pagename
        self.pageframe.add(allPages[self.currentPageName].gtk)
        if oldPage is not None:
            oldPage.uninstalled()
        allPages[self.currentPageName].installed()
        self.sensitize()
        gtklogger.checkpoint("page installed " + self.currentPageName)

    def show(self, messages=[]):
        debug.mainthreadTest()
        if self.currentPageName is None:
            self.installPage(pagenames[0])
            self.pageChooser.set_state(self.currentPageName)
            self.historian.record(pagenames[0])

        # don't use self.gtk.show_all(), since there may be page
        # components that shouldn't yet be shown.
        self.menubar.show_all()
        self.pageChooserFrame.show_all()
        self.pageframe.show()
        self.mainbox.show()
        for page in allPages.values():
            page.show()
        self.gtk.show()

        for m in messages:
            reporter.report(m)
        
    def addPage(self, page, position):
        debug.mainthreadTest()
        pagetips = {}
        for pg in allPages.values():
            if pg.tip:
                pagetips[pg.name]=pg.tip
        self.pageChooser.update(pagenames, pagetips)
        self.sensitize()

    def pageChooserCB(self, widget, pagename):
        self.installPage(pagename)
        self.historian.record(pagename)

    def nextPageCB(self, button):
        which = pagenames.index(self.currentPageName)
        newpage = pagenames[which+1]
        self.installPage(newpage)
        self.pageChooser.set_state(newpage)
        self.historian.record(newpage)

    def prevPageCB(self, button):
        which = pagenames.index(self.currentPageName)
        newpage = pagenames[which-1]
        self.installPage(newpage)        
        self.pageChooser.set_state(newpage)
        self.historian.record(newpage)

    def historianCB(self, pagename):
        self.installPage(pagename)
        self.pageChooser.set_state(pagename)

    def sensitize(self):
        debug.mainthreadTest()
        # If currentPageName is None, then the GUI hasn't been shown yet.
        if self.currentPageName is not None:
            which = pagenames.index(self.currentPageName)
            self.nextPageButton.set_sensitive(which != len(pagenames)-1)
            self.prevPageButton.set_sensitive(which != 0)

            if which < len(pagenames)-1:
                tooltips.set_tooltip_text(
                    self.nextPageButton,
                    "Go to the %s page" % allPages[pagenames[which+1]].name)
            if which > 0:
                tooltips.set_tooltip_text(
                    self.prevPageButton,
                    "Go to the %s page" % allPages[pagenames[which-1]].name)
        self.sensitizeHistory()

    def sensitizeHistory(self):
        debug.mainthreadTest()
        self.nextHistoryButton.set_sensitive(self.historian.nextSensitive())
        self.prevHistoryButton.set_sensitive(self.historian.prevSensitive())
        next = self.historian.nextVal()
        if next is not None:
            tooltips.set_tooltip_text(self.nextHistoryButton,
                         "Go to the chronologically next page, %s." % next)
        else:
            tooltips.set_tooltip_text(self.nextHistoryButton,
                         "Go to the chronologically next page.")
        prev = self.historian.prevVal()
        if prev is not None:
            tooltips.set_tooltip_text(self.prevHistoryButton,
                         "Go the chronologically previous page, %s." % prev)
        else:
            tooltips.set_tooltip_text(self.prevHistoryButton,
                         "Go the chronologically previous page.")
            

    def deleteEventCB(self, *args):
        # quit.queryQuit() asks for confirmation and then either quits
        # or doesn't.  Since the quitting process begins on another
        # thread (waiting for other threads to finish) queryQuit()
        # will actually return if if it's really quitting.
        quit.queryQuit()
        return 1  # Don't destroy the window.  If we're really
                  # quitting, self.destroy() will be called in due
                  # course.
    def destroyCB(self, gtk):
        self.gtk = None
        guitop.setTop(None)
    def destroy(self):
        debug.mainthreadTest()
        if self.gtk:
            self.gtk.destroy()

            
    def stop(self):
        # Called at exit-time by the Quit menu item, including when
        # exit is triggered by closing the main OOF window.

        debug.mainthreadTest()

        for window in gfxmanager.gfxManager.getAllWindows():
            gfxmanager.gfxManager.closeWindow(window)
          
        from ooflib.common.IO.GUI import console
        if console.current_console:
            console.current_console.gtk.destroy()

        from ooflib.common.IO.GUI import activityViewer
        if activityViewer.activityViewer:
            activityViewer.activityViewer.close()

        from ooflib.common.IO.GUI import reporter_GUI
        # iterate over a copy of the set so that its size doesn't
        # change during iteration.
        for m in set(reporter_GUI.allMessageWindows):
            m.gtk.destroy()

        # *This* line *is* required.
        gtk.main_quit()


    # GUI callback for "OOF2" or "OOF3D" entry in Windows menu.
    # Normally, the "subwindow" class provides this functionality, but
    # the main window is not a subwindow.
    def menu_raise(self, menuitem):
        debug.mainthreadTest()
        self.gtk.window.raise_()
        

    
####################################################

# Pages added to the main OOF window must be subclasses of MainPage.
# The subclass's __init__ should call MainPage.__init__ and install
# all of its widgets into self.gtk, which is a GtkFrame constructed by
# MainPage.__init__.  A single instance of the subclass should be
# created.

class MainPage(widgetscope.WidgetScope):
    def __init__(self, name, ordering, tip=None):
        debug.mainthreadTest()
        widgetscope.WidgetScope.__init__(self, parent=gui)
        self.name = name
        self.ordering = ordering
        self.tip = tip
        self.gtk = gtk.Frame()
        self.gtk.set_shadow_type(gtk.SHADOW_NONE)
        # Insert the page in the proper spot
        for i in range(len(pagenames)):
            if self.ordering < allPages[pagenames[i]].ordering:
                pagenames.insert(i, name)
                if guitop.top():        # gui may not be constructed yet!
                    guitop.top().addPage(self, i)
                break
        else:                           # page goes at the end
            pagenames.append(name)
            if guitop.top():            # gui may not be constructed yet!
                guitop.top().addPage(self, len(pagenames))
        allPages[name] = self
        gtklogger.setWidgetName(self.gtk, name+' Page')

    # MainPage.show() should be redefined in subclasses that don't
    # always want to show all their widgets.  show() should call the
    # gtk.show method on the components of the page.  It's called when
    # the page is constructed.  It's *not* called when the GUI
    # switches to the page.  For that, see installed() and uninstalled(),
    # below.
    def show(self):
        self.gtk.show_all()
    def hide(self):                     # This seems not be called at all...
        self.gtk.hide()

    # Pages that have to do some calculation when they become visible
    # can redefine installed() and uninstalled(). 
    def installed(self):
        pass
    def uninstalled(self):
        pass
    def is_current(self):
        return gui.currentPageName == self.name

gui = oofGUI()

def start(messages=[], files=[]):
    debug.mainthreadTest()

    ## See parameter.ParameterMetaClass
    # from ooflib.common.IO import parameter
    # parameter.checkMakeWidget()

    # Only call gui.show() afer the main loop has started.  Some gui
    # components need to have the whole threading machinery available
    # when they're starting up. 
    mainthreadGUI.run_gui(gui.show, (messages,))
    guitop.setMainLoop(True)
    if thread_enable.enabled():
        gtk.gdk.threads_init()
        ## We used to call gtk.gdk.threads_enter() and threads_leave()
        ## here, but they appear not to be necessary on OS X or Linux
        ## and to be detrimental on NetBSD.
        #gtk.gdk.threads_enter()
    try:
        ## The startup files must be loaded *after* the GUI
        ## starts, but this routine doesn't regain control once it
        ## starts the GUI. So we have to install the file loader
        ## (loadStartUpFiles) as an idle callback, which will run on
        ## the main thread.  loadStartUpFiles just issues menu
        ## commands that load the files, and if it runs on the main
        ## thread those menu commands will run by Workers on
        ## subthreads, and won't be run sequentially.  So, instead of
        ## installing loadStartUpFiles as an idle callback, we install
        ## subthread.execute and have it call loadStartUpFiles, since
        ## workers on subthreads don't create additional subthreads to
        ## run their menu items.
        from ooflib.common import subthread
        mainthread.run(subthread.execute_immortal, (loadStartUpFiles, (files,)))
        gtk.main()
    finally:
        guitop.setMainLoop(False)
        # if thread_enable.enabled():
        #     gtk.gdk.threads_leave()
    
def loadStartUpFiles(files):  
    # Files is a list of StartUpFile-like objects
    for phile in files:
        phile.load()
