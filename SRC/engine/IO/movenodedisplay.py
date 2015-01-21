# -*- python -*-
# $RCSfile: movenodedisplay.py,v $
# $Revision: 1.19.12.16 $
# $Author: langer $
# $Date: 2014/09/10 21:28:44 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO import canvaslayers
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common.IO import display
from ooflib.common.IO import ghostgfxwindow
from ooflib.common.IO import mainmenu
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import xmlmenudump
import types

class MoveNodeDisplay(display.DisplayMethod):
    def __init__(self, color, size):
        self.color = color
        self.size = size
        display.DisplayMethod.__init__(self)
        self.tbcallbacks = []

    def destroy(self, destroy_canvaslayer):
        map(switchboard.removeCallback, self.tbcallbacks)
        self.tbcallbacks = []
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

    def draw(self, gfxwindow, device):
        toolbox = gfxwindow.getToolboxByName("Move_Nodes")
        node = toolbox.selectednode.node()
        if node and toolbox.selectednode.visible:
            device.set_lineColor(self.color)
            device.set_lineWidth(self.size)
            device.draw_dot(node.position())

    # def getTimeStamp(self, gfxwindow):
    #     toolbox = gfxwindow.getToolboxByName("Move_Nodes")
    #     return max(self.timestamp,
    #                toolbox.selectednode.getTimeStamp())

    def newLayer(self):
        self.movenodeToolbox = self.gfxwindow.getToolboxByName("Move_Nodes")
        self.tbcallbacks = [
            switchboard.requestCallbackMain(
                ("node selected", self.movenodeToolbox), self.nodeSelectedCB)
            ]
        return canvaslayers.SimplePointCellLayer(self.gfxwindow.oofcanvas,
                                                 "MoveNode")

    def setParams(self):
        self.canvaslayer.set_color(self.color)
        self.canvaslayer.set_pointSize(self.size)

    def nodeSelectedCB(self):   # sb ("node selected", toolbox)
        self.update()
    
    def whoChanged(self):
        self.update()
        return True

    def update(self):
        node = self.movenodeToolbox.selectednode.node()
        if node is not None:
            skelcontext = self.movenodeToolbox.getSkeletonContext()
            self.canvaslayer.newGrid(skelcontext.getObject().getPoints(), 1)
            self.canvaslayer.addCell(node.getCellType(), node.getPointIds())
        else:
            self.canvaslayer.clear()

defaultMoveNodeColor = color.RGBColor(1.0, 0.2, 0.2)
defaultMoveNodeSize = 8

def _setDefaultMoveNodeParams(menuitem, color, size):
    global defaultMoveNodeSize
    global defaultMoveNodeColor
    defaultMoveNodeColor = color
    defaultMoveNodeSize = size

movenodeparams = [color.ColorParameter('color', defaultMoveNodeColor,
                                       tip="Color for the to-be-moved node."),
                  parameter.IntRangeParameter('size', (0, 10, 1),
                                              defaultMoveNodeSize,
                                              tip="Node size.")]

mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    'Moving_Nodes',
    callback=_setDefaultMoveNodeParams,
    params=movenodeparams,
    ordering=7,
    help="Set default parameters for the Move Node toolbox displays.",
    discussion="""<para>

    Set default parameters governing how the
    <link linkend="Section-Graphics-MoveNodes">Move Nodes Toolbox</link>
    displays the moving node in the graphics window.  See
    <xref linkend="RegisteredClass-MoveNodeDisplay"/> for details.
    This command can be put in the &oof2rc; file to set the defaults for
    all &oof2; sessions.

    </para>"""))

moveNodeDisplay = registeredclass.Registration(
    'Moving Nodes',
    display.DisplayMethod,
    MoveNodeDisplay,
    params=movenodeparams,
    ordering=3.0,
    layerordering=display.PointLike(1),
    whoclasses=('Skeleton',),
    tip="Display the node being moved by the Move Node toolbox.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/movenodedisplay.xml')
    )

def defaultMoveNodeDisplay():
    return moveNodeDisplay(color=defaultMoveNodeColor,
                           size=defaultMoveNodeSize)

ghostgfxwindow.PredefinedLayer('Skeleton', '<topmost>', defaultMoveNodeDisplay)
