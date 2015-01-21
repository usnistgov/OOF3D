# -*- python -*-
# $RCSfile: movenode.py,v $
# $Revision: 1.34.12.12 $
# $Author: fyc $
# $Date: 2014/07/28 22:17:27 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

## TODO MER: 3D Switching to Mouse mode is disabled in movenodeGUI.py.
## It's difficult to implement correctly, so it's being postponed.
## The initial location for a move can be resolved using
## findClickedPoint, but the end point cannot be.  One way to do it
## would be to only move nodes in the plane parallel to the screen.
## Another would be to let the user choose what plane to move in, or
## to choose a ray along which to move the node.  Or use some more
## powerful widget -- possibly see
## http://en.wikipedia.org/wiki/Direct_manipulation_interface.  Maybe
## click on a node to select it.  Draw an arrow through the node.
## Drag the head of the arrow to change its orientation.  Drag the
## node to move it along the arrow.

from ooflib.SWIG.common import switchboard
# from ooflib.SWIG.common import timestamp
from ooflib.SWIG.common.IO import view
from ooflib.common import debug
from ooflib.common import parallel_enable
from ooflib.common import primitives
from ooflib.common import ringbuffer
from ooflib.common import toolbox
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
from ooflib.engine import skeletondiff

class SelectedNode:
    def __init__(self, node=None):
        # self.timestamp = timestamp.TimeStamp()
        self.node_ = node
        # visible is set by the gui toolbox when it switches into
        # keyboard mode.
        self.visible = node is not None

    def __repr__(self):
        # Is this ever used?  Perhaps just for debugging?
        return "SelectedNode(%s)" % self.node

    def set(self, node=None):
        self.node_ = node
        if node is None: 
            visible = False
        # self.timestamp.increment()
        return self

    def set_visible(self, val):
        self.visible = val
        # self.timestamp.increment()

    def node(self):
        return self.node_

    # def getTimeStamp(self):
    #     return self.timestamp

##########################################################################

class MoveNodeToolbox(toolbox.Toolbox):
    def __init__(self, gfxwindow):
        toolbox.Toolbox.__init__(self, 'Move_Nodes', gfxwindow)
        self.whoset = ('Skeleton',)
        self.selectednode = SelectedNode()
        self.allow_illegal = False
        self.skeleton = None
        self.sbcallbacks = [
            switchboard.requestCallback((self.gfxwindow(), "layers changed"),
                                        self.layersChangedCB),
            switchboard.requestCallback(("who changed", "Skeleton"),
                                        self.whoChangedCB)
            ]

    def close(self):
        map(switchboard.removeCallback, self.sbcallbacks)
        
    def getSkeletonContext(self):
        return self.gfxwindow().topwho(*self.whoset)

    def makeMenu(self, menu):
        self.menu = menu
        menu.addItem(oofmenu.OOFMenuItem(
                'MoveNode',
                callback = self.moveNode,
                params=[
                    parameter.IntParameter(
                        'node', tip='Index of the node to be moved.'),
                        primitives.PointParameter(
                        'destination', tip=parameter.emptyTipString)],
                help="Move a node to another positon.",
                discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/engine/menu/move_node.xml')
                ))
        menu.addItem(oofmenu.OOFMenuItem(
                'SelectNode',
                callback = self.selectNode,
                params=[
                    primitives.PointParameter(
                        'position', tip=parameter.emptyTipString),
                    view.ViewParameter('view')],
                help="Select a node to move.",
                discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/engine/menu/select_move_node.xml')
                ))
        menu.addItem(oofmenu.OOFMenuItem(
                'AllowIllegal',
                callback = self.allowIllegal,
                params=[parameter.BooleanParameter(
                        'allowed', 0, tip=parameter.emptyTipString)],
                help="Are illegal elements allowed?",
                discussion=xmlmenudump.loadFile(
                    'DISCUSSIONS/engine/menu/allow_illegal.xml')
                ))

    def activate(self):
        pass
        
    def moveNode(self, menuitem, node, destination):
        # The OOF2 version of this menu command has an "origin" arg,
        # which is a Point, instead of the "node" arg, which is an
        # integer index.  The problem with the Point arg is that it
        # can be ambiguous if the skeleton is illegal and two nodes
        # are coincident.
        skelcontext = self.gfxwindow().topwho('Skeleton')
        if skelcontext:
            skeleton = skelcontext.resolveCSkeleton(
                skelcontext.getObject().deputyCopy())
            skeleton.activate()
            skelcontext.reserve()
            skelcontext.begin_writing()
            try:
                nodeobj = skeleton.getNode(node)
                skeleton.moveNodeTo(nodeobj, destination.asTuple())
                if nodeobj.illegal():
                    if self.allow_illegal:
                        skeleton.setIllegal()
                    else:
                        nodeobj.moveBack()
                elif skeleton.illegal():
                    # node motion may have rehabilitated elements
                    skeleton.checkIllegality()
                skelcontext.pushModification(skeleton)
            finally:
                skelcontext.end_writing()
                skelcontext.cancel_reservation()
            skeleton.needsHash()
            # pushModification calls whoChangedCB via the switchboard,
            # which clears the selection.  Re-select it, in the *new*
            # skeleton.
            self.selectednode.set(skelcontext.getObject().getNode(node))
            switchboard.notify(("node selected", self))
            switchboard.notify('redraw')
            

    def selectNode(self, menuitem, position, view):
        context = self.gfxwindow().topwho(*self.whoset)
        if context:
            skeleton = context.getObject()
            pt = self.gfxwindow().findClickedPoint(context, position, view)
            if pt is not None:
                node = skeleton.nearestNode(pt)
            else:
                node = None
            self.selectednode.set(node)
            switchboard.notify(("node selected", self))
            switchboard.notify('redraw')

    def allowIllegal(self, menuitem, allowed):
        self.allow_illegal = allowed
        switchboard.notify(("illegal-move status changed", self), allowed)

    def layersChangedCB(self):  # sb (gfxwindow, "layers changed")
        skelctxt = self.getSkeletonContext()
        if skelctxt is not self.skeleton:
            self.skeleton = skelctxt
            self.selectednode.set() # clears selection
            switchboard.notify(("skeleton changed", self))

    def whoChangedCB(self, who): # sb ("who changed", "Skeleton")
        ## TODO 3.1: Use the SkeletonSelectable parent/child relations to
        ## reselect a node if possible.
        self.selectednode.set()  # clears selection
        switchboard.notify(("skeleton changed", self))

    tip="Move Skeleton nodes interactively."
    discussion="""<para>
    Menu commands for moving &skel; nodes, based on mouse input.
    </para>"""
toolbox.registerToolboxClass(MoveNodeToolbox, ordering=2.6)
