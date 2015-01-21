# -*- python -*-
# $RCSfile: pinnodesdisplay.py,v $
# $Revision: 1.14.18.18 $
# $Author: langer $
# $Date: 2014/10/01 21:28:34 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO import canvaslayers
from ooflib.SWIG.engine import cskeletonselectable
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import display
from ooflib.common.IO import ghostgfxwindow
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump

class PinnedNodesDisplay(display.DisplayMethod):
    def __init__(self, color, size):
        self.color = color
        self.size = size
        display.DisplayMethod.__init__(self)
        self.tbcallbacks = []
    def destroy(self, destroy_canvaslayer):
        map(switchboard.removeCallback, self.tbcallbacks)
        display.DisplayMethod.destroy(self, destroy_canvaslayer)
    def draw(self, gfxwindow, canvas): # 2D only
        skel = self.who().resolve(gfxwindow)
        nodes = skel.pinnednodes.retrieve()
        num = len(nodes)
        if num:
            canvas.set_lineColor(self.color)
            canvas.set_lineWidth(self.size)
            canvas.create_grid(skel.getObject().getPoints(), num, True)
            for node in nodes:
                canvas.add_cell_to_grid(node.getCellType(), node.getPointIds())

    def newLayer(self):
        self.tbcallbacks.append(switchboard.requestCallbackMain(
                "new pinned nodes", self.pinnednodeschangedCB))
        return canvaslayers.SimplePointCellLayer(self.gfxwindow.oofcanvas,
                                                 "PinnedNodes")

    def pinnednodeschangedCB(self, skelctxt): # sb "new pinned nodes"
        if skelctxt is self.who().resolve(self.gfxwindow):
            self.updatePinned(skelctxt)

    def whoChanged(self):
        skelctxt = self.who().resolve(self.gfxwindow)
        if skelctxt is not None:
            self.updatePinned(skelctxt)
        else:
            self.canvaslayer.clear()
        return True

    def updatePinned(self, skelctxt):
        cskeletonselectable.rebuildLayerCells(
            skelctxt.getObject(),
            self.canvaslayer,
            skelctxt.pinnednodes.currentSelectionTracker())

    def setParams(self):
        self.canvaslayer.set_color(self.color)
        self.canvaslayer.set_pointSize(self.size)
                

defaultPinNodeColor = color.RGBColor(1., 0.65, 0.0)
defaultPinNodeSize = 7

def _setPinNodeParams(menuitem, color, size):
    global defaultPinNodeColor
    global defaultPinNodeSize
    defaultPinNodeColor = color
    defaultPinNodeSize = size

pinnodeparams = [
    color.ColorParameter('color', defaultPinNodeColor,
                         tip="Color for the pinned nodes."),
    parameter.IntRangeParameter('size', (0,10), defaultPinNodeSize,
                                tip="Node size.")]

mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    'Pinned_Nodes',
    callback=_setPinNodeParams,
    params=pinnodeparams,
    ordering=6,
    help="Set default parameters for displaying pinned skeleton nodes.",
    discussion="""<para>

    Set the default parameters for the
    <xref linkend="RegisteredClass-PinnedNodesDisplay"/>, which
    graphically indicates which &nodes; are
    <link linkend="Section-Concepts-Pin">pinned</link>.
    This command may be put in the &oof2rc; file to set defaults
    for all &oof2; sessions.

    </para>"""))

pinnedNodesDisplay = registeredclass.Registration(
    'Pinned Nodes',
    display.DisplayMethod,
    PinnedNodesDisplay,
    params=pinnodeparams,
    layerordering=display.PointLike(2),
    ordering=3.1,
    whoclasses=('Skeleton',),
    tip="Display the pinned nodes.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/pinnodesdisplay.xml')
    )

def defaultPinnedNodesDisplay():
    return pinnedNodesDisplay(color=defaultPinNodeColor,
                              size=defaultPinNodeSize)


ghostgfxwindow.PredefinedLayer('Skeleton', '<topmost>', 
                               defaultPinnedNodesDisplay)
