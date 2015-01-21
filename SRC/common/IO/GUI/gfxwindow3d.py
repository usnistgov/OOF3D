# -*- python -*-
# $RCSfile: gfxwindow3d.py,v $
# $Revision: 1.9.2.50 $
# $Author: langer $
# $Date: 2014/10/17 21:48:01 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

import gobject
import gtk

from ooflib.SWIG.common import guitop
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO.GUI import oofcanvas3d 
from ooflib.SWIG.common.IO.GUI import rubberband3d as rubberband
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import utils
from ooflib.common.IO import gfxmanager
from ooflib.common.IO import ghostgfxwindow
from ooflib.common.IO import mainmenu
from ooflib.common.IO.GUI import chooser
from ooflib.common.IO.GUI import gfxwindowbase
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import quit
from ooflib.common.IO.GUI import subWindow
from ooflib.common.IO.GUI import toolbarGUI

# during_callback() is called (by CanvasOutput.show()) only in
# non-threaded mode, so we don't worry about the thread-safety of a
# global variable here.  It may not be necessary with the vtk canvas
# at all.
_during_callback = 0
def during_callback():
    return _during_callback

class GfxWindow3D(gfxwindowbase.GfxWindowBase):
    initial_height = 800
    initial_width = 1000

    def preinitialize(self, name, gfxmanager, clone):
        debug.mainthreadTest()
        self.gtk = None
        self.closed = None # State data used at window-close time.
        self.name = name
        self.oofcanvas = None
        self.realized = 0
        self.zoomed = 0
        self.settings = ghostgfxwindow.GfxSettings()
        self.mouseHandler = mousehandler.nullHandler # doesn't do anything
        self.rubberband = rubberband.NoRubberBand()

        # Build all the GTK objects for the interior of the box.  These
        # actually get added to the window itself after the SubWindow
        # __init__ call.  They need to be created first so the
        # GhostGfxWindow can operate on them, and then create the menus
        # which are handed off to the SubWindow.
        self.mainpane = gtk.VPaned()
        gtklogger.setWidgetName(self.mainpane, 'Pane0')

        # Pane dividing upper pane horizontally into 2 parts.
        self.paned1 = gtk.HPaned()
        gtklogger.setWidgetName(self.paned1, "Pane2")
        self.mainpane.pack1(self.paned1, resize=True)
        gtklogger.connect_passive(self.paned1, 'size-allocate')

        # The toolbox is in the left half of paned1 (ie the left frame of 3)
        toolboxframe = gtk.Frame()
        toolboxframe.set_shadow_type(gtk.SHADOW_IN)
        self.paned1.pack1(toolboxframe, resize=True)
        ## TODO OPT: Does the frame size really need to be logged?  It
        ## should just follow from the pane size.
        gtklogger.setWidgetName(toolboxframe, "ToolboxFrame")
        gtklogger.connect_passive(toolboxframe, 'size-allocate')

        # Box containing the toolbox label and the scroll window for
        # the toolbox itself.
        toolboxbox1 = gtk.VBox()
        toolboxframe.add(toolboxbox1)
        hbox = gtk.HBox()
        toolboxbox1.pack_start(hbox, expand=0, fill=0, padding=2)
        hbox.pack_start(gtk.Label("Toolbox:"), expand=0, fill=0, padding=3)
        
        self.toolboxchooser = chooser.ChooserWidget([],
                                                    callback=self.switchToolbox,
                                                    name="TBChooser")
        hbox.pack_start(self.toolboxchooser.gtk, expand=1, fill=1, padding=3)

        # Scroll window for the toolbox itself.
        toolboxbox2 = gtk.ScrolledWindow()
        gtklogger.logScrollBars(toolboxbox2, 'TBScroll')
        
        toolboxbox2.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        toolboxbox1.pack_start(toolboxbox2, expand=1, fill=1)

        # Actually, the tool box goes inside yet another box, so that
        # we have a gtk.VBox that we can refer to later.
        self.toolboxbody = gtk.VBox()
        toolboxbox2.add_with_viewport(self.toolboxbody)

        self.toolboxGUIs = []           # GUI wrappers for toolboxes.
        self.current_toolbox = None

        # The canvas is in the right half of paned1.  The toolbar goes
        # on top of the canvas.
        self.canvasBox = gtk.VBox()
        toolbarFrame = gtk.Frame()
        toolbarFrame.set_shadow_type(gtk.SHADOW_IN)
        self.canvasBox.pack_start(toolbarFrame, expand=0, fill=0,
                                  padding=0)
        self.toolbarBox = gtk.VBox()
        toolbarFrame.add(self.toolbarBox)

        self.canvasFrame = gtk.Frame()
        self.canvasFrame.set_shadow_type(gtk.SHADOW_IN)
        gtklogger.setWidgetName(self.canvasFrame, "Canvas")
        self.canvasBox.pack_start(self.canvasFrame, expand=1, fill=1, padding=0)

        self.paned1.pack2(self.canvasBox, resize=True)

        # HACK.  Set the position of the toolbox/canvas divider.  This
        # prevents the toolbox pane from coming up minimized.
        ##self.paned1.set_position(300)


        # Bottom part of main pane is a list of layers.  The actual
        # DisplayLayer objects are stored in self.display.

        layerFrame = gtk.Frame(label='Layers')
        
        self.mainpane.pack2(layerFrame, resize=False)
        self.layerScroll = gtk.ScrolledWindow()
        gtklogger.logScrollBars(self.layerScroll, "LayerScroll")
        self.layerScroll.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        layerFrame.add(self.layerScroll)

        self.layerList = gtk.ListStore(gobject.TYPE_PYOBJECT)
        self.layerListView = gtk.TreeView(self.layerList)
        gtklogger.setWidgetName(self.layerListView, "LayerList")
        self.layerListView.set_row_separator_func(self.layerRowSepFunc)
        self.layerListView.set_reorderable(True)
        self.layerListView.set_fixed_height_mode(False)
        self.layerScroll.add(self.layerListView)

        gtklogger.adoptGObject(self.layerList, self.layerListView,
                              access_method=self.layerListView.get_model)

        # The row-deleted and row-inserted signals are used to detect
        # when the user has reordered rows manually.  When the program
        # does anything that might cause these signals to be emitted,
        # it must first call suppressRowOpSignals.
        self.rowOpSignals = [
            gtklogger.connect(self.layerList, "row-deleted",
                             self.listRowDeletedCB),
            gtklogger.connect(self.layerList, "row-inserted",
                             self.listRowInsertedCB)
            ]
        self.destination_path = None

        showcell = gtk.CellRendererToggle()
        showcol = gtk.TreeViewColumn("Show")
        showcol.pack_start(showcell, expand=False)
        showcol.set_cell_data_func(showcell, self.renderShowCell)
        self.layerListView.append_column(showcol)
        gtklogger.adoptGObject(showcell, self.layerListView,
                               access_function=gtklogger.findCellRenderer,
                               access_kwargs={'col':0, 'rend':0})
        gtklogger.connect(showcell, 'toggled', self.showcellCB)        

##         cmapcell = gtk.CellRendererToggle()
##         cmapcell.set_radio(True)
##         cmapcol = gtk.TreeViewColumn("Map")
##         cmapcol.pack_start(cmapcell, expand=False)
##         cmapcol.set_cell_data_func(cmapcell, self.renderCMapCell)
##         self.layerListView.append_column(cmapcol)
##         gtklogger.adoptGObject(cmapcell, self.layerListView,
##                                access_function='findCellRenderer',
##                                access_kwargs={'col':1, 'rend':0})
##         gtklogger.connect(cmapcell, 'toggled', self.cmapcellCB)        

        layercell = gtk.CellRendererText()
        layercol = gtk.TreeViewColumn("What")
        layercol.set_resizable(True)
        layercol.pack_start(layercell, expand=True)
        layercol.set_cell_data_func(layercell, self.renderLayerCell)
        self.layerListView.append_column(layercol)

        methodcell = gtk.CellRendererText()
        methodcol = gtk.TreeViewColumn("How")
        methodcol.set_resizable(True)
        methodcol.pack_start(methodcell, expand=True)
        methodcol.set_cell_data_func(methodcell, self.renderMethodCell)
        self.layerListView.append_column(methodcol)

        gtklogger.adoptGObject(self.layerListView.get_selection(),
                              self.layerListView,
                              access_method=self.layerListView.get_selection)
        self.selsignal = gtklogger.connect(self.layerListView.get_selection(), 
                                          'changed', self.selectionChangedCB)
        gtklogger.connect(self.layerListView, 'row-activated',
                         self.layerDoubleClickCB)
        

    def postinitialize(self, name, gfxmanager, clone):
        debug.mainthreadTest() 
        # Add gui callbacks to the non-gui menu created by the GhostGfxWindow.
        filemenu = self.menu.File
        filemenu.Quit.add_gui_callback(quit.queryQuit)
        layermenu = self.menu.Layer
        # There's no gui callback for layermenu.New.
        ## TODO OPT: Why are these added to the menu here, when the
        ## functions themselves are defined in gfxwindowbase.py?
        layermenu.Edit.add_gui_callback(self.editLayer_gui)
        layermenu.Delete.add_gui_callback(self.deleteLayer_gui)
        layermenu.Hide.add_gui_callback(self.hideLayer_gui)
        layermenu.Show.add_gui_callback(self.showLayer_gui)
#         layermenu.Raise.One_Level.add_gui_callback(self.raiseLayer_gui)
#         layermenu.Raise.To_Top.add_gui_callback(self.raiseToTop_gui)
#         layermenu.Lower.One_Level.add_gui_callback(self.lowerLayer_gui)
#         layermenu.Lower.To_Bottom.add_gui_callback(self.lowerToBottom_gui)
        settingmenu = self.menu.Settings
        toolboxmenu = self.menu.Toolbox

        # The toolbar must be constructed before the toolboxes,
        # because it contains the gtk.Adjustment that's used by the
        # Viewer toolbox.
        self.toolbar = toolbarGUI.ToolBar(self)
        self.toolbarBox.pack_start(self.toolbar.gtk, expand=False, fill=False)
        self.toolbar.gtk.show()
        self.timebox = self.makeTimeBox()
        self.toolbarBox.pack_start(self.timebox, expand=False, fill=False)

        # Construct gui's for toolboxes.  This must be done after the
        # base class is constructed so that *all* non-gui toolboxes
        # are created before any of their gui versions.  Some gui
        # toolboxes need to know about more than one non-gui toolbox.

        map(self.makeToolboxGUI, self.toolboxes)
        if self.toolboxGUIs:
            self.selectToolbox(self.toolboxGUIs[0].name())
            self.toolboxchooser.set_state(self.toolboxGUIs[0].name())

        # raise_window routine is in SubWindow class.
        getattr(mainmenu.OOF.Windows.Graphics, name).add_gui_callback(
            self.raise_window)

        # SubWindow initializer makes the menu bar, and sets up the
        # .gtk and .mainbox members.  ".gtk" is the window itself,
        # and .mainbox is a gtk.VBox that holds the menu bar.
        windowname = utils.underscore2space("OOF3D " + name)
        subWindow.SubWindow.__init__(self, windowname, menu=self.menu)

        self.gtk.connect('destroy', self.destroyCB)
        self.gtk.connect_after('realize', self.realizeCB)
        self.gtk.set_default_size(GfxWindow3D.initial_width,
                                  GfxWindow3D.initial_height)

        self.mainbox.set_spacing(3)

        self.mainbox.pack_start(self.mainpane, fill=1, expand=1)

        self.oofcanvas.set_bgColor(self.settings.bgcolor)
        self.oofcanvas.setAntiAlias(self.settings.antialias)

        self.oofcanvas.setAxisLabelColor(self.settings.axislabelcolor)
        self.oofcanvas.setAxisLabelFontSize(self.settings.axisfontsize)
        self.oofcanvas.setAxisOffset(self.settings.axisoffset.resolve(self))
        self.oofcanvas.setAxisLength(self.settings.axislength.resolve(self))

        self.oofcanvas.setContourMapBGColor(self.settings.contourmap_bgcolor,
                                            self.settings.contourmap_bgopacity)
        self.oofcanvas.setContourMapTextColor(
            self.settings.contourmap_textcolor)
        self.oofcanvas.setContourMapSize(self.settings.contourmap_size[0],
                                         self.settings.contourmap_size[1])
        self.oofcanvas.setContourMapPosition(
            self.settings.contourmap_position[0],
            self.settings.contourmap_position[1])
        
        self.gtk.show_all()    # calls realizeCB(), which calls drawAtTime()

        self.updateToolboxChooser()

    def __repr__(self):
        return 'GfxWindow("%s")' % self.name

    ################################################

    def newCanvas(self):
        # Create the canvas object.
        debug.mainthreadTest()

        view = None
        if self.oofcanvas:
            view = self.oofcanvas.get_view()
            self.oofcanvas.widget().destroy()

        self.oofcanvas = oofcanvas3d.OOFCanvas3D() #self.settings)
        self.oofcanvas.set_bgColor(self.settings.bgcolor)
        self.canvasFrame.add(self.oofcanvas.widget())
        
        # Retrieving the drawing area and initiating the logging.
        canvasdrawingarea = self.oofcanvas.widget()
        init_canvas_logging(canvasdrawingarea) 
        # Since the drawing area isn't a gtk widget it must be adopted
        # by its frame in order to record and replay events.
        gtklogger.adoptGObject(canvasdrawingarea, self.canvasFrame,
                               access_function=findCanvasDrawingArea,
                               access_kwargs={"windowname":self.name})
        # Setting the connection.
        gtklogger.connect_passive(canvasdrawingarea, "event")
        
        self.oofcanvas.set_mouse_callback(self.mouseCB)

        # self.oofcanvas.widget().connect("configure-event",
        #                                 self.canvasConfigureCB)

        #self.oofcanvas.set_rubberband(self.rubberband)
        #if view is not None:
        #    self.oofcanvas.set_view(view)

        self.oofcanvas.show()

    # def canvasConfigureCB(self, *args):
    #     gtklogger.checkpoint("canvas configured %s" % self.name)

    ################################################

    def draw(self):
        if self.closed or not self.realized:
            return
        self.acquireGfxLock()
        try:
            self.initializeView()
            self.updateTimeControls()
            mainthread.runBlock(self.oofcanvas.render)
        finally:
            self.releaseGfxLock()

    def show_contourmap_info(self):
        # TODO MERGE: This is only used in 2D and will go away when 2D
        # uses vtk for contouring.
        debug.fmsg()
        if not self.gtk:
            return
        current_contourmethod = self.current_contourmap_method
        if current_contourmethod:
            current_contourmethod.draw_contourmap(
                self, self.oofcanvas)

    def zoomFillWindow_thread(self):
        if self.closed:
            return
        if self.oofcanvas and not self.empty:
            self.oofcanvas.reset()
            self.updateview()
            switchboard.notify("view changed", self)


    def bgColor(self, menuitem, color):
        self.acquireGfxLock()
        try:
            ghostgfxwindow.GhostGfxWindow.bgColor(self, menuitem, color)
            mainthread.runBlock(self.oofcanvas.set_bgColor, (color,))
            mainthread.run(self.oofcanvas.render)
        finally:
            self.releaseGfxLock()

    def setRubberband(self, rubberband):
        self.rubberband = rubberband
        self.oofcanvas.set_rubberband(rubberband)
       
    def marginCB(self, menuitem, fraction):
        ghostgfxwindow.GhostGfxWindow.marginCB(self, menuitem, fraction)
        self.oofcanvas.set_margin(fraction)

    # setCanvasSize operates on the *vtk* render window, not the gtk
    # drawing area.  It's used in gui log files, to ensure that
    # recorded mouse clicks are replayed in the same environment in
    # which they were recorded.  Only the vtk size is relevant,
    # because vtk is processing the click.  This is convenient,
    # because it's really hard to change the gtk widget size
    # precisely.
        
    def setCanvasSize(self, width, height):
        debug.mainthreadTest()
        if self.oofcanvas is None:
            return
        oldsize = self.getCanvasSize()
        self.oofcanvas.set_size(width, height)
        return oldsize          # 2-tuple
    
    def getCanvasSize(self):
        sz = self.oofcanvas.get_size()
        return (sz[0], sz[1])

###########################################

## Support for logging and replaying mouse clicks.

# Although the Canvas *is* a gtk Widget, it's not a pygtk Widget, and
# it's hard to use the widget logging machinery directly on it. So we
# pretend that it's some other kind of gtk object and use the
# adoptGObject machinery instead.  It's adopted by
# GfxWindow.canvasFrame.  adoptGObject is told the name of the window.
# The log uses the window name and findCanvasDrawingArea to retrieve the
# Canvas's drawing area, which is the crucial bit for emitting signals.


def findCanvasDrawingArea(gtkobj, windowname):
    # We retrieve the canvas widget differently from the 2D where we
    # were retrieving the root object.
    window = gfxmanager.gfxManager.getWindow(windowname)
    # oofcanvas.widget() returns pygobject_new(drawing_area), where
    # drawing_area is the GtkWidget* for the canvas.
    return window.oofcanvas.widget()

def findCanvasGdkWindow(windowname):
    # We get the widget window as in the 2D this does not have to change.
    window = gfxmanager.gfxManager.getWindow(windowname)
    return window.oofcanvas.widget().window

def findOOFWindow(windowname):
    return gfxmanager.gfxManager.getWindow(windowname)
                    

# The tracking events list.
desired_events = [gtk.gdk.BUTTON_PRESS,
                  gtk.gdk.BUTTON_RELEASE,
                  gtk.gdk.MOTION_NOTIFY
                  ]

# The canvas logging variable.
_canvaslogging_initialized = False

# The init canvas in generic to handle the 3D without no changes. We
# profiled it looking for side effects. None found.
def init_canvas_logging(canvasgroup):
    global _canvaslogging_initialized
    if _canvaslogging_initialized:
        return
    _canvaslogging_initialized = True

    # Inject findCanvasDrawingArea into the gtklogger replay namespace, which
    # is where gui scripts are run.
    gtklogger.replayDefine(findCanvasDrawingArea)
    gtklogger.replayDefine(findCanvasGdkWindow)
    gtklogger.replayDefine(findOOFWindow)
    #print "logging process...."

    # The GtkLogger for Canvas events has to be defined *after* the
    # first canvas has been created, because the GnomeCanvasGroup
    # class isn't in pygtk.  We snag the object returned by
    # OOFCanvas::rootitem and use its class for the CanvasLogger.
    class CanvasLogger(gtklogger.adopteelogger.AdopteeLogger):
        classes = (canvasgroup.__class__,)
        # def location(self, obj, *args):
        #     return super(CanvasLogger, self).location(obj, *args)
        buttonup = True
        def record(self, obj, signal, *args):
            if signal == "event":
                event = args[0]
                if event.type in desired_events:
                    # event.type.value_name is something of the form
                    # GDK_XXXXXX, but the python variable is
                    # gtk.gdk.XXXXXX, so we have to strip off the
                    # "GDK_".
                    eventname = event.type.value_name[4:]
                    windowname = obj.oofparent_access_kwargs["windowname"]
                    window = gfxmanager.gfxManager.getWindow(windowname)
                    csize = window.getCanvasSize()
                    if event.type in (gtk.gdk.BUTTON_PRESS,
                                      gtk.gdk.BUTTON_RELEASE):
                        CanvasLogger.buttonup = (event.type ==
                                                 gtk.gdk.BUTTON_RELEASE)
                        return [
                            "window = findOOFWindow('%s')" % windowname,
                            "oldsize = window.setCanvasSize(%d, %d)"
                            % (csize[0], csize[1]),
                            "canvasobj = %s" % self.location(obj, *args),
                            "canvasobj.emit('event', event(gtk.gdk.%s,x=%20.13e,y=%20.13e,button=%d,state=%d,window=findCanvasGdkWindow('%s')))"
                            % (eventname, event.x, event.y, event.button,
                               event.state, windowname),
                            "window.setCanvasSize(oldsize[0], oldsize[1])"
                            ]
                    if event.type == gtk.gdk.MOTION_NOTIFY:
                        # If the mouse is down, ignore the
                        # suppress_motion_events flag.  Always log
                        # mouse-down motion events, and log all motion
                        # events if they're not suppressed.
                        if (gtklogger.suppress_motion_events(obj) and
                            self.buttonup):
                            return self.ignore
                        return [
                            "window = findOOFWindow('%s')" % windowname,
                            "oldsize = window.setCanvasSize(%d, %d)"
                            % (csize[0], csize[1]),
                            "canvasobj = %s" % self.location(obj, *args),
                            "canvasobj.emit('event', event(gtk.gdk.MOTION_NOTIFY,x=%20.13e,y=%20.13e,state=%d,window=findCanvasGdkWindow('%s')))"
                            % (event.x, event.y, event.state, windowname),
                            "window.setCanvasSize(oldsize[0], oldsize[1])"
                        ]
                return self.ignore      # silently ignore other events
            super(CanvasLogger, self).record(obj, signal, *args)

##############################################

# This function redefines the one in GfxWindowManager when the GUI
# code is loaded.

def _newWindow(self, name, **kwargs):
    if guitop.top(): # if in GUI mode
        return GfxWindow3D(name, self, **kwargs)
    return ghostgfxwindow.GhostGfxWindow(name, self, **kwargs)

gfxmanager.GfxWindowManager._newWindow = _newWindow



