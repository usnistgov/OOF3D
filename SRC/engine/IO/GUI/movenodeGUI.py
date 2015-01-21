# -*- python -*-
# $RCSfile: movenodeGUI.py,v $
# $Revision: 1.82.8.11 $
# $Author: langer $
# $Date: 2014/10/31 17:58:49 $


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
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO.GUI import rubberband3d as rubberband
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import primitives
from ooflib.common import subthread
from ooflib.common import utils
from ooflib.common.IO import mainmenu
from ooflib.common.IO.GUI import gtklogger
from ooflib.common.IO.GUI import mousehandler
from ooflib.common.IO.GUI import toolboxGUI
from ooflib.common.IO.GUI import tooltips
from ooflib.engine.IO import movenode
import gtk
import sys
import types

class MoveNodeToolboxGUI(toolboxGUI.GfxToolbox, mousehandler.MouseHandler):
    def __init__(self, movenodetoolbox):
        debug.mainthreadTest()
        self.downed = 0                 # is the mouse button down?
        self.moving = 0                 # in the middle of a move
        self.movingnode = None          # node being moved
        # writable should only be set by self.set_writable, which
        # issues a checkpoint.
        self.writable = True            # is the top most Skeleton writable?
        ## TODO 3.1: Make Mouse mode the default in 3D too, when it's fixed.
        if config.dimension() == 2:
            self.mode = "Mouse"
        else:
            self.mode = "Keyboard"
        self.mouselock = lock.Lock()
        
        toolboxGUI.GfxToolbox.__init__(self, "Move Nodes", movenodetoolbox)
        mainbox = gtk.VBox()
        self.gtk.add(mainbox)

        hbox = gtk.HBox()
        mainbox.pack_start(hbox, expand=0, fill=0)
        gtklogger.setWidgetName(hbox, "MoveWith")
        hbox.pack_start(gtk.Label("Move with: "), expand=0, fill=0)

        modes = [("Mouse", "Click and drag a node to move it."),
                 ("Keyboard",
                  "Select a node, type a position, and click the Move button")
                 ]
        self.modebuttons = []
        for mode, tip in modes:
            if self.modebuttons:
                button = gtk.RadioButton(label=mode,
                                         group=self.modebuttons[0])
            else:
                button = gtk.RadioButton(label=mode)
            gtklogger.setWidgetName(button, mode)
            self.modebuttons.append(button)
            tooltips.set_tooltip_text(button, tip)
            hbox.pack_start(button, expand=0, fill=0)
            button.set_active(self.mode is mode)
            gtklogger.connect(button, 'clicked', self.changeMode, mode)
        
        ## TODO 3.1: Delete this when Mouse mode is fixed in 3D
        if config.dimension() == 3:
            self.modebuttons[0].set_sensitive(0)

        # allow illegal move?
        self.allow_illegal = gtk.CheckButton("Allow illegal moves")
        gtklogger.setWidgetName(self.allow_illegal, "AllowIllegal")
        mainbox.pack_start(self.allow_illegal, expand=0, fill=0, padding=1)
        mainbox.pack_start(gtk.HSeparator(), expand=0, fill=0, padding=3)
        gtklogger.connect(self.allow_illegal, "clicked", self.illegal_status)
        if movenodetoolbox.allow_illegal:
            self.allow_illegal.set_active(1)
        else:
            self.allow_illegal.set_active(0)
 
        self.table = gtk.Table()
        mainbox.pack_start(self.table, expand=0, fill=0)

        label = gtk.Label('index=')
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, 0,1, xpadding=5, xoptions=gtk.FILL)
        self.itext = gtk.Entry()
        gtklogger.setWidgetName(self.itext, 'i')
        self.itext.set_editable(0)
        self.table.attach(self.itext, 1,2, 0,1,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        tooltips.set_tooltip_text(self.itext, "Index of the selected node.")

        if config.dimension() == 2:
            coords = "xy"
        else:
            coords = "xyz"
        r = 1                   # row number
        self.texts = []
        self.signals = []
        for crd in coords:
            label = gtk.Label(crd+'=')
            label.set_alignment(1.0, 0.5)
            self.table.attach(label, 0,1, r,r+1, xpadding=5, xoptions=gtk.FILL)
            entry = gtk.Entry()
            self.texts.append(entry)
            gtklogger.setWidgetName(entry, crd)
            self.signals.append(gtklogger.connect_passive(entry, 'changed'))
            entry.set_size_request(12*guitop.top().digitsize, -1)
            entry.set_editable(1)
            self.table.attach(entry, 1,2, r,r+1,
                              xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
            tooltips.set_tooltip_text(entry, crd+" position of the node.")
            r += 1

        label = gtk.Label("Change in... ")
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, r,r+1, xpadding=4,
                          xoptions=gtk.EXPAND|gtk.FILL)

        label = gtk.Label("shape energy=")
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, r+1,r+2, xpadding=5, xoptions=gtk.FILL)
        self.shapetext = gtk.Entry()
        self.shapetext.set_editable(0)
        gtklogger.setWidgetName(self.shapetext,"shape")
        self.shapetext.set_size_request(12*guitop.top().digitsize, -1)        
        self.table.attach(self.shapetext, 1,2, r+1,r+2,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        tooltips.set_tooltip_text(self.shapetext,
                                  "total change in shape energy")

        label = gtk.Label("homogeneity=")
        label.set_alignment(1.0, 0.5)
        self.table.attach(label, 0,1, r+2,r+3, xpadding=5, xoptions=gtk.FILL)
        self.homogtext = gtk.Entry()
        self.homogtext.set_editable(0)
        gtklogger.setWidgetName(self.homogtext,"homog")
        self.homogtext.set_size_request(12*guitop.top().digitsize, -1)        
        self.table.attach(self.homogtext, 1,2, r+2,r+3,
                          xpadding=5, xoptions=gtk.EXPAND|gtk.FILL)
        tooltips.set_tooltip_text(self.homogtext, "total change in homogeneity")

        mainbox.pack_start(gtk.HSeparator(), expand=0, fill=0, padding=3)
        self.statusText = gtk.Label()
        gtklogger.setWidgetName(self.statusText, "Status")
        mainbox.pack_start(self.statusText, expand=0, fill=0, padding=3)
        
        bbox = gtk.HBox(homogeneous=1, spacing=2)
        mainbox.pack_end(bbox, expand=0, fill=0, padding=3)
        self.undobutton = gtk.Button(stock=gtk.STOCK_UNDO)
        tooltips.set_tooltip_text(self.undobutton, "Undo the latest node move.")
        self.movebutton = gtk.Button('Move')
        tooltips.set_tooltip_text(self.movebutton,
                           "Move the selected node to the specified position.")
        self.redobutton = gtk.Button(stock=gtk.STOCK_REDO)
        tooltips.set_tooltip_text(self.redobutton, "Redo the latest UNDO.")

        gtklogger.setWidgetName(self.undobutton, 'Undo')
        gtklogger.setWidgetName(self.redobutton, 'Redo')
        gtklogger.setWidgetName(self.movebutton, 'Move')
        bbox.pack_start(self.undobutton, expand=1, fill=1)
        bbox.pack_start(self.movebutton, expand=1, fill=1)
        bbox.pack_start(self.redobutton, expand=1, fill=1)
        gtklogger.connect(self.undobutton, 'clicked', self.undoCB)
        gtklogger.connect(self.movebutton, 'clicked', self.moveCB)
        gtklogger.connect(self.redobutton, 'clicked', self.redoCB)

        self.sbcallbacks = [
            switchboard.requestCallbackMain(('who changed', 'Skeleton'),
                                            self.skelChanged),
            switchboard.requestCallbackMain("made reservation",
                                            self.rsrvChanged,
                                            1),
            switchboard.requestCallbackMain("cancelled reservation",
                                            self.rsrvChanged, 0),
            switchboard.requestCallbackMain(("node selected",
                                             movenodetoolbox),
                                            self.nodeSelected),
            switchboard.requestCallbackMain(("illegal-move status changed",
                                             movenodetoolbox),
                                            self.illegal_status_changed),
            switchboard.requestCallbackMain(("skeleton changed", 
                                             movenodetoolbox),
                                            self.layersChanged)
            ]

        # Bits of the mode button callback have to be done at
        # initialization time too.
        self.move_info(None, '---', '---', '')
        self.toolbox.selectednode.set_visible(self.mode=="Keyboard")

    def node(self):
        return self.toolbox.selectednode.node()

    def illegal_status_changed(self, status):
        debug.mainthreadTest()
        self.allow_illegal.set_active(status)
        
    def illegal_status(self, gtkobj):
        debug.mainthreadTest()
        if self.allow_illegal.get_active():
            self.toolbox.menu.AllowIllegal(allowed=1)
        else:
            self.toolbox.menu.AllowIllegal(allowed=0)
            
    def changeMode(self, button, mode): # mode button callback
        debug.mainthreadTest()
        if button.get_active():
            self.mode = mode
            self.toolbox.selectednode.set_visible(mode=="Keyboard")
            if self.mode == "Mouse":
                self.move_info(None, "---", "---", "")
            else:
                if self.node() is not None:
                    self.move_info(self.node().position(),
                                   "---", "---", "")
            self.sensitize()
            switchboard.notify('redraw')

    def getSkeletonContext(self):
        return self.gfxwindow().topwho('Skeleton')
    
    def getSkeleton(self):
        return self.gfxwindow().topmost('Skeleton')

    def illegalityText(self):
        skel = self.getSkeleton()
        if skel:
            n = self.getSkeleton().getIllegalCount()
            if n:
                return "%d illegal element%s in the skeleton.\n" % (n,
                                                                    "s"*(n!=1))
        return ""

    def skelChanged(self, skelcontext): # sb ("who changed", "Skeleton")
        debug.mainthreadTest()
        if skelcontext is self.getSkeletonContext():
            self.statusText.set_text(self.illegalityText())
            self.sensitize()
        
    def sensitize(self):
        debug.mainthreadTest()
        skeletoncontext = self.getSkeletonContext()
        reserved = skeletoncontext is not None and \
                   skeletoncontext.query_reservation()
        self.undobutton.set_sensitive(skeletoncontext is not None
                                      and not reserved
                                      and skeletoncontext.undoable())
        self.redobutton.set_sensitive(skeletoncontext is not None
                                      and not reserved
                                      and skeletoncontext.redoable())
        
        self.movebutton.set_sensitive(self.mode == "Keyboard"
                                      and self.node() is not None
                                      and not reserved)
        editable = (self.mode == "Keyboard" and self.node() is not None)

        for text in self.texts:
            text.set_editable(editable)

        gtklogger.checkpoint(self.gfxwindow().name + " " +
                             self._name + " sensitized")

    def rsrvChanged(self, reserved, whocls):
        skelcontext = self.getSkeletonContext()
        if (skelcontext and skelcontext.path() == whocls.path()):
            self.sensitize()
            self.set_writable(not reserved)

    def set_writable(self, val):
        self.writable = val
        # This checkpoint is required because the state of
        # self.writable affects which mouse events are processed.
        # Those mouse events can trigger other checkpoints, so if the
        # writable flag is set wrongly, the other checkpoints might
        # not be reached.
        gtklogger.checkpoint("Move Node toolbox writable changed")

    def nodeChanged(self):
        # See comment in set_writable()
        gtklogger.checkpoint("Move Node toolbox node changed")
        
    # Notice if the new topmost skeleton is writable.  Callback for
    # switchboard "skeleton changed" signal, which is emitted by the
    # non-gui part of this toolbox when the topmost gfxwindow skeleton
    # changes (in response to the "layers changed" switchboard signal).
    def layersChanged(self, *args): # switchboard "skeleton changed"
        skelcontext = self.getSkeletonContext()
        self.set_writable(skelcontext and not skelcontext.query_reservation())
        mainthread.runBlock(self.move_info, 
                            (None, "---", "---", self.illegalityText()))
        mainthread.runBlock(self.sensitize)

    def activate(self):
        if not self.active:
            toolboxGUI.GfxToolbox.activate(self)
            self.gfxwindow().setMouseHandler(self)
            self.sensitize()
            if config.dimension() == 3:
                self.gfxwindow().toolbar.setSelect()

    def deactivate(self):
        if self.active:
            toolboxGUI.GfxToolbox.deactivate(self)
            self.gfxwindow().removeMouseHandler()

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        toolboxGUI.GfxToolbox.close(self)

    def move_info(self, point, homogtext, shapetext, labeltext):
        debug.mainthreadTest()
        self.showPosition(point)
        self.homogtext.set_text(homogtext)
        self.shapetext.set_text(shapetext)
        self.statusText.set_text(labeltext)
        gtklogger.checkpoint("Move Node toolbox info updated")

    def showPosition(self, point, mobility=None):
        debug.mainthreadTest()
        for signal in self.signals:
            signal.block()
        try:
            if point is None:
                for text in self.texts:
                    text.set_text('---')
                    text.set_sensitive(False)
            else:
                for i, text in enumerate(self.texts):
                    text.set_text(("%-11.4g" % point[i]).rstrip())
                # Desensitize the input fields if the node isn't
                # movable in that direction.  If mobility==None, then
                # keep the previous sensitization.  We're just
                # updating the position, not changing nodes.
                if mobility is not None:
                    for i, text in enumerate(self.texts):
                        text.set_sensitive(mobility[i])
        finally:
            for signal in self.signals:
                signal.unblock()

    def showIndex(self, node):
        debug.mainthreadTest()
        if node is not None:
            self.itext.set_text(`node.uiIdentifier()`)
        else:
            self.itext.set_text('')

    def acceptEvent(self, eventtype):
        if not self.writable: # Don't accept events if the skeleton is busy.
            return 0       
        if self.mode == "Mouse":
            return eventtype=='down' or \
                   (self.downed and eventtype in ('move', 'up'))
        elif self.mode == "Keyboard":
            return eventtype=='up'

    def down(self, x, y, shift, ctrl):
        subthread.execute(self.down_subthread, (x,y,shift,ctrl))

    def down_subthread(self, x, y, shift, ctrl):
        debug.subthreadTest()
        self.mouselock.acquire()
        try:
            self.downed = 1
            point = primitives.Point(x,y)
            mainthread.runBlock(self.move_info, (point, "0", "0", ''))
            skel = mainthread.runBlock(self.getSkeleton)
            skelctxt = mainthread.runBlock(self.getSkeletonContext)
            reserved = skel is not None and skelctxt.query_reservation()
            if skel is not None and not reserved and point is not None:
                self.movingnode = skel.nearestNode(point)
                self.nodeChanged()
                #Store this point for use by the up callback's call to MoveNode
                self.downpt=point
                if self.movingnode.pinned():
                    self.nodeChanged() # TODO: Is this required? Redundant?
                    self.movingnode = None
                else:
                    # Mouse-down events are only accepted in Mouse mode,
                    # so the end_reading() call corresponding to this
                    # begin_reading() is in the "Mouse" section of the
                    # up() callback.
                    skelctxt.begin_reading()
                    self.nbrnodes = skel.getNeighborNodes(self.movingnode)
                    # self.movingnode.aperiodicNeighborNodes(skel)
                    self.nbrelements = self.movingnode.getElements()
                    self.startpt = tuple(self.movingnode.position())
                    # Get initial values of homogeneity and shape energy
                    self.homogeneity0 = 0.0
                    self.shapeenergy0 = 0.0
                    for element in self.nbrelements:
                        if not element.illegal():
                            self.homogeneity0 += element.homogeneity(
                                skel.getMicrostructure())
                            self.shapeenergy0 += element.energyShape()
                    # Create rubberband
                    points = []
                    for n in self.nbrnodes:
                        pos = n.position()
                        points.append(primitives.Point(pos[0],pos[1],pos[2]))
                    # points = [n.position() for n in self.nbrnodes]
                    rb = mainthread.runBlock(rubberband.SpiderRubberBand,
                                             (points,))
                    mainthread.runBlock(
                        self.gfxwindow().setRubberband, (rb,) )
            gtklogger.checkpoint("Move Node toolbox down event")
        finally:
            self.mouselock.release()
            
    def move(self, x, y, shift, ctrl):
        skeleton = self.getSkeleton()
        subthread.execute(self.move_thread, (skeleton, x, y, shift, ctrl))
    def move_thread(self, skeleton, x, y, shift, ctrl):
        debug.subthreadTest()
        self.mouselock.acquire()
        try:
            if self.movingnode is not None:
                self.moving = 1
                homogeneity = 0.0
                shapeenergy = 0.0
                point = primitives.Point(x,y)
                # It's generally forbidden to call node.moveTo instead of
                # skeleton.moveNodeTo, but since we're going to move the
                # node back (see up(), below), it's ok.
                if point is not None:
                    # this should be cleaned up when we clean up use of Coords
                    self.movingnode.moveTo((point.x,point.y,point.z))
                if self.movingnode.illegal():
                    homogtext = "---"
                    shapetext = "---"
                    labeltext = "Illegal node position!"
                else:
                    for element in self.nbrelements:
                        # Evaluating homogeneity and shape energy is
                        # safe, because the Skeleton's read lock was
                        # acquired when the mouse went down.
                        homogeneity += element.homogeneity(
                            skeleton.getMicrostructure())
                        shapeenergy += element.energyShape()
                    homogtext = "%-11.4g" % (homogeneity-self.homogeneity0)
                    shapetext = "%-11.4g" % (shapeenergy-self.shapeenergy0)
                    labeltext = ""
                mainthread.runBlock(self.move_info,
                                    (point, homogtext, shapetext, labeltext))
                gtklogger.checkpoint("Move Node toolbox move event")
        finally:
            self.mouselock.release()

    # self.allow_illegal CheckButton to decide whether or not illegal
    # moves are allowed, and if it gets an illegal-and-not-allowed
    # move, the move is not performed -- no menu items are called,
    # nothing is scripted.

    def up(self, x, y, shift, ctrl):
        # "Downed" must be cleared at the earliest opportunity,
        # otherwise spurious "move" events can be processed,
        # unilaterally changing the node position.
        self.downed = 0 
        if self.mode == "Keyboard":
            canvas = self.toolbox.gfxwindow().oofcanvas
            view = canvas.get_view()
            pt = canvas.display2Physical(view, x, y)
            self.toolbox.menu.SelectNode(position=pt, view=view)
        else:                   # self.mode == "Mouse"
            subthread.execute(self.up_subthread_mouse, (x,y,shift,ctrl))

    def up_subthread_mouse(self, x, y, shift, ctrl):
        debug.subthreadTest()
        self.mouselock.acquire()
        try:
            point = primitives.Point(x,y)
            # if self.mode == "Mouse":
            skelcontext = mainthread.runBlock(self.getSkeletonContext)
            if skelcontext is not None:
                skelcontext.end_reading()
            if self.moving:
                self.moving = 0 # Dunmovin, CA is east of the Sierra Nevada
                mainthread.runBlock(self.showPosition, (point,))
                # Accept/reject conditon:
                # Allow_illegal is ON : unconditionally accept everything
                # Allow_illegal is OFF : any node associated with
                # illegal nodes before or after will not be moved.
                aige = mainthread.runBlock(self.allow_illegal.get_active)
                if self.movingnode.illegal() and not aige:
                    # Restore the state of the skeleton, and show
                    # the original position in the toolbox.
                    self.movingnode.moveTo(self.startpt)
                    mainthread.runBlock(self.showPosition, (self.startpt,))
                    mainthread.runBlock(self.statusText.set_text,
                                        (self.illegalityText(),))
                else:
                    # Restore the state of the skeleton so that the non-GUI
                    # movenode command can do the real work.
                    self.movingnode.moveTo(self.startpt)
                    try:
                        self.toolbox.menu.MoveNode(
                            origin=self.downpt,
                            destination=point)
                    finally:
                        rbb = mainthread.runBlock(rubberband.NoRubberBand)
                        mainthread.runBlock(self.gfxwindow().setRubberband,
                                            (rbb,) )
                        self.nbrnodes = []

            # elif self.mode == "Keyboard":
            #     self.toolbox.menu.SelectNode(position=point)
            gtklogger.checkpoint("Move Node toolbox up event")
        finally:
            self.mouselock.release()

    def nodeSelected(self):             # sb ("node selected", toolbox)
        # This is called via the switchboard after the SelectNode menu
        # callback has finished.  It must be called this way, so that
        # the menu callback is guaranteed to have finished and
        # self.toolbox.selectednode has been set.
        self.nodeChanged()
        node = self.node()
        if node is not None:
            pos = node.position()
            if config.dimension() == 2:
                mob = (node.movable_x(), node.movable_y())
            else:
                mob = (node.movable_x(), node.movable_y(), node.movable_z())
        else:
            pos = None
            mob = None
        self.showPosition(pos, mob)
        self.showIndex(node)
        self.sensitize()
        
    def undoCB(self, button):
        mainmenu.OOF.Skeleton.Undo(skeleton=self.getSkeletonContext().path())

    def redoCB(self, button):
        mainmenu.OOF.Skeleton.Redo(skeleton=self.getSkeletonContext().path())

    # Move button callback in Keyboard mode
    def moveCB(self, button):
        debug.mainthreadTest()
        xyz = [utils.OOFeval(text.get_text()) for text in self.texts]
        point = primitives.Point(*xyz)
        skelctxt = self.getSkeletonContext()
        subthread.execute(self.kbmove_subthread, (skelctxt, point))

    def kbmove_subthread(self, skelctxt, point):
        debug.subthreadTest()
        # In order to prohibit illegal node moves, we have to actually
        # move the node, check it, and move the node back.  If it's
        # ok, then we call the menu item, which makes the permanent
        # move.
        skelctxt.begin_writing()
        skeleton = skelctxt.getObject()
        try:
            # Compute initial energy of neighboring elements
            neighbors = self.node().getElements()

            homogeneity0 = 0.0
            shapeenergy0 = 0.0
            for element in neighbors:
                if element.illegal():
                    continue
                homogeneity0 += \
                    element.homogeneity(skeleton.getMicrostructure())
                shapeenergy0 += element.energyShape()

            # Energy after node move
            self.node().moveTo(point.asTuple())
            illegal = False
            homogeneity = 0.0
            shapeenergy = 0.0
            for element in neighbors:
                if not illegal:
                    if element.illegal():
                        illegal = True
                    else:
                        homogeneity += \
                            element.homogeneity(skeleton.getMicrostructure())
                        shapeenergy += element.energyShape()
            self.node().moveBack()
        finally:
            skelctxt.end_writing()

        if illegal:
            if self.allow_illegal.get_active():
                mainthread.runBlock(self.move_info, (point, "---", "---", ""))
                self.toolbox.menu.MoveNode(node=self.node().uiIdentifier(),
                                           destination=point)
                
            else:
                # Illegal move not allowed.  Reset the x and y text so
                # that the user can try again.
                mainthread.runBlock(
                    self.move_info,
                    (self.node().position(),
                     "---", "---", ""))
        else:
            mainthread.runBlock(self.move_info,
                                (point,
                                 "%-11.4g" % (homogeneity - homogeneity0),
                                 "%-11.4g" % (shapeenergy - shapeenergy0),
                                 ""))
            self.toolbox.menu.MoveNode(node=self.node().uiIdentifier(),
                                       destination=point)

def _makeGUI(self):
    return MoveNodeToolboxGUI(self)

movenode.MoveNodeToolbox.makeGUI = _makeGUI
