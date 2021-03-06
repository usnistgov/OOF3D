# -*- python -*-


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
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import primitives
from ooflib.common import subthread
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO import reporter
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import toolboxGUI
from ooflib.common.IO.GUI import tooltips
from ooflib.engine.IO import pinnodes
from ooflib.engine.IO import pinnodesmenu

import gtk

class PinnedNodesToolboxGUI(toolboxGUI.GfxToolbox, mousehandler.MouseHandler):
    def __init__(self, pinnodestoolbox):
        debug.mainthreadTest()

        toolboxGUI.GfxToolbox.__init__(self, pinnodestoolbox)
        mainbox = gtk.VBox()
        self.gtk.add(mainbox)

        infoframe = gtk.Frame()
        mainbox.pack_start(infoframe, expand=0, fill=0)
        info = gtk.Label("""Click a node to pin it.
Shift-click to pin additional nodes.
Ctrl-click to toggle a node.
Shift-ctrl-click to unpin a node.""")
        infoframe.add(info)
            
        self.updateLock = lock.Lock()
       
        self.table = gtk.Table(columns=3, rows=4)
        r = 0
        mainbox.pack_start(self.table, expand=0, fill=0)

        label = gtk.Label("Node")
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, r,r+config.dimension(),
                          xpadding=2, xoptions=0)

        label = gtk.Label('x=')
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 1,2, r,r+1, xpadding=2, xoptions=gtk.FILL)
        self.nodextext = gtk.Entry()
        gtklogger.setWidgetName(self.nodextext,"Node X")
        self.nodextext.set_size_request(12*guitop.top().digitsize, -1)
        self.nodextext.set_editable(0)
        self.table.attach(self.nodextext, 2,3, r,r+1,
                          xpadding=2, xoptions=gtk.EXPAND|gtk.FILL)
        r += 1

        label = gtk.Label('y=')
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 1,2, r,r+1, xpadding=2, xoptions=gtk.FILL)
        self.nodeytext = gtk.Entry()
        gtklogger.setWidgetName(self.nodeytext,"Node Y")
        self.nodeytext.set_size_request(12*guitop.top().digitsize, -1)        
        self.nodeytext.set_editable(0)
        self.table.attach(self.nodeytext, 2,3, r,r+1,
                          xpadding=2, xoptions=gtk.EXPAND|gtk.FILL)
        r += 1

        label = gtk.Label('z=')
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 1,2, r,r+1, xpadding=2, xoptions=gtk.FILL)
        self.nodeztext = gtk.Entry()
        gtklogger.setWidgetName(self.nodeztext,"Node Z")
        self.nodeztext.set_size_request(12*guitop.top().digitsize, -1)        
        self.nodeztext.set_editable(0)
        self.table.attach(self.nodeztext, 2,3, r,r+1,
                          xpadding=2, xoptions=gtk.EXPAND|gtk.FILL)
        r += 1
            
        self.pintext = gtk.Label()
        gtklogger.setWidgetName(self.pintext,"Pin Label")
        self.pintext.set_alignment(0.0, 0.5)
        self.table.attach(self.pintext, 2,3, r,r+1,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)

        modbox = gtk.VBox()
        mainbox.pack_end(modbox, expand=0, fill=0)

        bbox1 = gtk.HBox(homogeneous=True, spacing=2)
        modbox.pack_end(bbox1, expand=0, fill=0, padding=2)

        self.undobutton = gtk.Button(stock=gtk.STOCK_UNDO)
        gtklogger.setWidgetName(self.undobutton, 'Undo')
        gtklogger.connect(self.undobutton, "clicked", self.undoCB)
        tooltips.set_tooltip_text(self.undobutton, "Undo the latest action.")
        bbox1.pack_start(self.undobutton, expand=1, fill=1)

        self.redobutton = gtk.Button(stock=gtk.STOCK_REDO)
        gtklogger.setWidgetName(self.redobutton, 'Redo')
        gtklogger.connect(self.redobutton, "clicked", self.redoCB)
        tooltips.set_tooltip_text(self.redobutton,
                                  "Redo the latest undone action.")
        bbox1.pack_start(self.redobutton, expand=1, fill=1)

        bbox2 = gtk.HBox(homogeneous=True, spacing=2)
        modbox.pack_end(bbox2, expand=0, fill=0, padding=2)

        self.unpinallbutton = gtk.Button("Unpin All")
        gtklogger.setWidgetName(self.unpinallbutton, 'UnPinAll')
        gtklogger.connect(self.unpinallbutton, "clicked", self.unpinallCB)
        tooltips.set_tooltip_text(self.unpinallbutton, 
                                  "Unpin all the pinned nodes.")
        bbox2.pack_start(self.unpinallbutton, expand=1, fill=1)

        self.invertbutton = gtk.Button("Invert")
        gtklogger.setWidgetName(self.invertbutton, 'Invert')
        gtklogger.connect(self.invertbutton, "clicked", self.invertCB)
        tooltips.set_tooltip_text(self.invertbutton,
                             "Invert - pin the unpinned and unpin the pinned.")
        bbox2.pack_start(self.invertbutton, expand=1, fill=1)

        self.status = gtk.Label()
        gtklogger.setWidgetName(self.status,"Status")
        self.status.set_alignment(0.0, 0.5)
        mainbox.pack_end(self.status, expand=0, fill=0, padding=5)

        self.sbcallbacks = [
            switchboard.requestCallbackMain(('who changed', 'Skeleton'),
                                            self.skelChanged),
            switchboard.requestCallbackMain((self.gfxwindow(),
                                             'layers changed'),
                                            self.update),
            switchboard.requestCallbackMain("new pinned nodes",
                                            self.newPinState)
            ]

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        toolboxGUI.GfxToolbox.close(self)

    def getSkeletonContext(self):
        return self.gfxwindow().topwho('Skeleton')

    def getSkeletonPath(self):
        # Should never be called unless getSkeletonContext is
        # guaranteed not to return None.
        return self.getSkeletonContext().path()
            
    def update(self, skeleton=None, *args):
        debug.mainthreadTest()
        skelctxt = skeleton or self.getSkeletonContext()
        if skelctxt:
            n = len(skelctxt.pinnednodes.retrieve())
            self.status.set_text("%d node%s pinned." % (n, 's'*(n!=1)))
        else:
            self.status.set_text("No skeleton!")

        self.unpinallbutton.set_sensitive(skelctxt is not None and n > 0)
        self.undobutton.set_sensitive(skelctxt is not None and
                                      skelctxt.pinnednodes.undoable())
        self.redobutton.set_sensitive(skelctxt is not None and
                                      skelctxt.pinnednodes.redoable())
        self.invertbutton.set_sensitive(skelctxt is not None)

        gtklogger.checkpoint(self.gfxwindow().name + " " +
                             self.name() + " updated")

    def currentSkeleton(self):
        return self.gfxwindow().topwho('Skeleton')

    # Switchboard, "new pinned nodes".
    def newPinState(self, skelctxt):
        self.update(skeleton=skelctxt)
        switchboard.notify("redraw")

    # Called when a skeleton has changed.
    def skelChanged(self, skelcontext):
        if skelcontext is self.getSkeletonContext():
            self.update(skeleton=skelcontext)

    def activate(self):
        if not self.active:
            toolboxGUI.GfxToolbox.activate(self)
            if config.dimension() == 2: 
                gtklogger.log_motion_events(
                    self.gfxwindow().oofcanvas.rootitem())
            self.update()
            if config.dimension() == 3:
                self.gfxwindow().toolbar.setSelect()

    def deactivate(self):
        if self.active:
            toolboxGUI.GfxToolbox.deactivate(self)
            if config.dimension() == 2: 
                gtklogger.dont_log_motion_events(
                    self.gfxwindow().oofcanvas.rootitem())

    def installMouseHandler(self):
        self.gfxwindow().setMouseHandler(self)

    def showPosition(self, point):
        if config.dimension() == 2:
            debug.mainthreadTest()
            self.xtext.set_text("%-11.4g" % point[0])
            self.ytext.set_text("%-11.4g" % point[1])

    def showNodePosition(self, point, pinned):
        debug.mainthreadTest();
        self.nodextext.set_text("%-11.4g" % point[0])
        self.nodeytext.set_text("%-11.4g" % point[1])
        self.nodeztext.set_text("%-11.4g" % point[2])
        if pinned:
            self.pintext.set_text('pinned')
        else:
            self.pintext.set_text('unpinned')
    def showNoNodePosition(self):
        self.nodextext.set_text('')
        self.nodeytext.set_text('')
        self.nodeztext.set_text('')
        self.pintext.set_text('')

    #=--=##=--=##=--=##=--=##=--=##=--=#

    def acceptEvent(self, eventtype):
        return eventtype in ('move', 'up')

    def up(self, x, y, buttons):
        debug.mainthreadTest()
        skelctxt = self.getSkeletonContext()
        if skelctxt:
            canvas = self.gfxwindow().oofcanvas
            view = canvas.get_view()
            pt = canvas.display2Physical(view, x, y)
            subthread.execute(self.up_subthread, (view, buttons, pt))

    def up_subthread(self, view, buttons, pt):
        # findClickedPoint must be run on a subthread
        skelctxt = self.getSkeletonContext()
        point = self.gfxwindow().findClickedPoint(skelctxt, pt, view)
        if point is not None:
            path = skelctxt.path()
            if buttons.shift and buttons.ctrl:
                pinnodesmenu.pinnodesmenu.UnPin(skeleton=path, node=point)
            elif buttons.ctrl:
                pinnodesmenu.pinnodesmenu.TogglePin(skeleton=path, node=point)
            elif buttons.shift:
                pinnodesmenu.pinnodesmenu.AddPin(skeleton=path, node=point)
            else:
                pinnodesmenu.pinnodesmenu.Pin(skeleton=path, node=point)

    def move(self, x, y, buttons):
        # The toolbox is updated when the mouse *moves*, even before a
        # click, because it's displaying node information which helps
        # the user decide which node to click on.
        debug.mainthreadTest()
        ## TODO OPT: During a move, the skeleton context and view can't
        ## change, so it's inefficient to retrieve them here.  They
        ## should be cached whenever they change.  A previous attempt
        ## to do that missed some changes, so the caching was removed.
        skelctxt = self.getSkeletonContext()
        view = self.toolbox.gfxwindow().oofcanvas.get_view()
        canvas = self.toolbox.gfxwindow().oofcanvas
        pt = canvas.display2Physical(view, x, y)
        subthread.execute(self.move3, (skelctxt, view, pt))

    def move3(self, skelctxt, view, pt):
        debug.subthreadTest()
        self.updateLock.acquire()
        try:
            if skelctxt is not None:
                point = self.gfxwindow().findClickedPoint(skelctxt, pt, view)
                if point is not None:
                    node = skelctxt.getObject().nearestNode(point)
                    if node is not None:
                        mainthread.runBlock(self.showNodePosition,
                                            (node.position(), node.pinned()))
                        return
            # No Skeleton, point, or Node
            mainthread.runBlock(self.showNoNodePosition)

        finally:
            gtklogger.checkpoint(self.gfxwindow().name + " Pin Nodes move 3D")
            self.updateLock.release()

    # The buttons for which these are callbacks are not sensitized if
    # there is no skeleton context, so it's safe to use
    # getSkeletonPath.
    def invertCB(self, button):
        pinnodesmenu.pinnodesmenu.Invert(skeleton=self.getSkeletonPath())
    
    def undoCB(self, button):
        pinnodesmenu.pinnodesmenu.Undo(skeleton=self.getSkeletonPath())

    def unpinallCB(self, button):
        pinnodesmenu.pinnodesmenu.UnPinAll(skeleton=self.getSkeletonPath())

    def redoCB(self, button):
        pinnodesmenu.pinnodesmenu.Redo(skeleton=self.getSkeletonPath())

def _makeGUI(self):
    return PinnedNodesToolboxGUI(self)

pinnodes.PinnedNodesToolbox.makeGUI = _makeGUI
