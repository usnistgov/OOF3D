# -*- python -*-
# $RCSfile: skeletoninfodisplay.py,v $
# $Revision: 1.23.10.40 $
# $Author: langer $
# $Date: 2014/11/05 16:54:43 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
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

## TODO: SkeletonInfoDisplay and MeshInfoDisplay should share code.

class SkeletonInfoDisplay(display.DisplayMethod):
    def __init__(self, query_color, peek_color, node_size, line_width):
        self.query_color = query_color
        self.peek_color = peek_color
        self.node_size = node_size
        self.line_width = line_width
        self.tbcallbacks = []
        display.DisplayMethod.__init__(self)

    layerNames = ["Element", "Segment", "Node"] # all sublayers
    linearLayerNames = ["Element", "Segment"] # sublayers drawn with lines
    if config.dimension() == 3:
        layerNames.append("Face")
        linearLayerNames.append("Face")


    # def getTimeStamp(self, gfxwindow):
    #     toolbox = gfxwindow.getToolboxByName("Skeleton_Info")
    #     return max(self.timestamp, toolbox.timestamp)

    def destroy(self, destroy_canvaslayer):
        map(switchboard.removeCallback, self.tbcallbacks)
        self.tbcallbacks = []
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

    def newLayer(self):
        layer = canvaslayers.ComboCanvasLayer()
        canvas = self.gfxwindow.oofcanvas
        # The names of the layers here must correspond to the
        # targetnames used in skeletoninfo.py. 
        layer.addSublayer(
            "Element",
            canvaslayers.SimpleWireframeCellLayer(canvas, True,
                                                  "ElementSkelInfo"))
        if config.dimension() == 3:
            layer.addSublayer(
                "Face",
                canvaslayers.SimpleWireframeCellLayer(canvas, True,
                                                      "FaceSkelInfo"))
        layer.addSublayer(
            "Segment",
            canvaslayers.SimpleWireframeCellLayer(canvas, False,
                                                  "SegmentSkelInfo"))
        layer.addSublayer(
            "Node",
            canvaslayers.SimplePointCellLayer(canvas, "NodeSkelInfo"))
        assert not self.tbcallbacks
        self.tbcallbacks = [
            switchboard.requestCallbackMain(
                (self.gfxwindow, "query Skeleton"), self.queryCB),
            switchboard.requestCallbackMain(
                (self.gfxwindow, "peek Skeleton"), self.peekCB)
            ]
        return layer

    def setParams(self):
        toolbox = self.gfxwindow.getToolboxByName("Skeleton_Info")
        querymode = toolbox.currentMode()
        if querymode is not None:
            for lname in self.layerNames:
                layer = self.canvaslayer.getSublayer(lname)
                if lname == querymode.targetName:
                    color = self.query_color
                else:
                    color = self.peek_color
                layer.set_color(color)
                layer.set_opacity(1.0)
                if lname in self.linearLayerNames:
                    layer.set_lineWidth(self.line_width)
                else:
                    layer.set_pointSize(self.node_size)
                
    def queryCB(self):
        toolbox = self.gfxwindow.getToolboxByName("Skeleton_Info")
        # The queried object or peeked objects may have changed, which
        # changes the color assignments, so call setParams.
        self.setParams()
        skelctxt = self.who().resolve(self.gfxwindow)
        if skelctxt:
            try:
                querymode, queryobj = toolbox.getQueryObject()
                if queryobj:
                    for lname in self. layerNames:
                        layer = self.canvaslayer.getSublayer(lname)
                        if lname == querymode.targetName:
                            layer.newGrid(skelctxt.getObject().getPoints(), 1)
                            layer.addCell(queryobj.getCellType(),
                                          queryobj.getPointIds())
                        else:
                            layer.clear() # clear peek sublayers
                    return
            except:
                pass
        self.canvaslayer.clear() # clear all sublayers

    def peekCB(self, peekmode):
        toolbox = self.gfxwindow.getToolboxByName("Skeleton_Info")
        skelctxt = self.who().resolve(self.gfxwindow)
        if skelctxt:
            peekobj = toolbox.getPeekObject(peekmode)
            sublayer = self.canvaslayer.getSublayer(peekmode.targetName)
            if peekobj:
                sublayer.newGrid(skelctxt.getObject().getPoints(), 1)
                sublayer.addCell(peekobj.getCellType(), peekobj.getPointIds())
            else:
                sublayer.clear()
                
# # This object should be created via the registration, and not
# # directly via the initializer, because the registration creation
# # method gives it a timestamp.

defaultSkelInfoQueryColor = color.RGBColor(0.0, 0.5, 1.0)
defaultSkelInfoPeekColor = color.RGBColor(1.0, 0.5, 0.5)
defaultSkelInfoNodeSize = 10
defaultSkelInfoLineWidth = 4
if config.dimension() == 2:
    widthRange = (0,10)
# In vtk, line widths of 0 cause errors
elif config.dimension() == 3:
    widthRange = (1,10)

def _setSkelInfoParams(menuitem, query_color, peek_color, node_size,
                       line_width):
    global defaultSkelInfoQueryColor
    global defaultSkelInfoPeekColor
    global defaultSkelInfoNodeSize
    global defaultSkelInfoLineWidth
    defaultSkelInfoQueryColor = query_color
    defaultSkelInfoPeekColor = peek_color
    defaultSkelInfoNodeSize = node_size
    defaultSkelInfoLineWidth = line_width

skelinfoparams = [
    color.ColorParameter(
        'query_color', defaultSkelInfoQueryColor,
        tip="Color for the queried objects."),
    color.ColorParameter(
        'peek_color', defaultSkelInfoPeekColor,
        tip="Color for the peeked objects."),
    parameter.IntRangeParameter(
        'node_size', widthRange, defaultSkelInfoNodeSize,
        tip="Node size."),
    parameter.IntRangeParameter(
        'line_width', widthRange,
        defaultSkelInfoLineWidth,
        tip="Line width for elements, faces, and segments.")]

mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    'Skeleton_Info',
    callback=_setSkelInfoParams,
    ordering=1,
    params=skelinfoparams,
    help="Set default parameters for the skeleton info toolbox display.",
    discussion="""<para>

    Set default parameters for the
    <xref linkend="RegisteredClass-SkeletonInfoDisplay"/> used by the
    <link linkend="Section-Graphics-SkeletonInfo">Skeleton Info</link> toolbox.
    See <xref linkend="RegisteredClass-SkeletonInfoDisplay"/> for the details.
    This command can be placed in the &oof2rc; file to set values for all
    &oof2; sessions.

    </para>"""))

skeletonInfoDisplay = registeredclass.Registration(
    'SkeletonInfo',
    display.DisplayMethod,
    SkeletonInfoDisplay,
    params=skelinfoparams,
    ordering=4.0,
    layerordering=display.SemiLinear(3),
    whoclasses=('Skeleton',),
    tip="Set parameters for the decorations used by the Skeleton Info toolbox.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/skeletoninfodisplay.xml')
    )

def defaultSkeletonInfoDisplay():
    return skeletonInfoDisplay(query_color=defaultSkelInfoQueryColor,
                               peek_color=defaultSkelInfoPeekColor,
                               node_size=defaultSkelInfoNodeSize,
                               line_width=defaultSkelInfoLineWidth)

ghostgfxwindow.PredefinedLayer('Skeleton', '<topmost>',
                               defaultSkeletonInfoDisplay)

#########################################

class SkeletonIllegalElementDisplay(display.DisplayMethod):
    def __init__(self, color, linewidth):
        self.color = color
        self.linewidth = linewidth
        display.DisplayMethod.__init__(self)
        self.skelModSignal = switchboard.requestCallback(
            "Skeleton changed", self.skelModCB)

    def destroy(self, destroy_canvaslayer):
        switchboard.removeCallback(self.skelModSignal)
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

    def draw(self, gfxwindow, canvas): # 2D only
        skel = self.who().resolve(gfxwindow).getObject()
        elements = skel.getIllegalElements()
        if elements:
            canvas.set_lineColor(self.color)
            canvas.set_lineWidth(self.linewidth)
            # if config.dimension() == 2:
            for el in elements:
                for i in range(el.nnodes()):
                    n0 = el.nodes[i]
                    n1 = el.nodes[(i+1)%el.nnodes()]
                    canvas.draw_segment(primitives.Segment(n0.position(),
                                                           n1.position()))

    def newLayer(self):
        return canvaslayers.SimpleWireframeCellLayer(
            self.gfxwindow.oofcanvas, True, "SkeletonIllegal")

    def skelModCB(self, skeletonPath):
        skelctxt = self.who().resolve(self.gfxwindow)
        if skelctxt and skelctxt.path() == skeletonPath:
            self.whoChanged()

    def whoChanged(self):
        skelctxt = self.who().resolve(self.gfxwindow)
        if skelctxt:
            skelctxt.begin_reading()
            try:
                skel = skelctxt.getObject()
                elements = skel.getIllegalElements()
                if elements:
                    pts = skel.getPoints()
                    self.canvaslayer.newGrid(pts, len(elements))
                    for e in elements:
                        self.canvaslayer.addCell(e.getCellType(),
                                                 e.getPointIds())
                    return
            finally:
                skelctxt.end_reading()
        # If we got here, there's either no skelctxt or no illegal
        # elements.
        self.canvaslayer.clear()
        return True

    def setParams(self):
        self.canvaslayer.set_color(self.color)
        self.canvaslayer.set_lineWidth(self.linewidth)

defaultSkelIllegalColor = color.RGBColor(1.0, 0.01, 0.01)
defaultSkelIllegalWidth = 4

def _setSkelIllegalParams(menuitem, color, linewidth):
    global defaultSkelIllegalColor
    global defaultSkelIllegalWidth
    defaultSkelIllegalColor = color
    defaultSkelIllegalWidth = linewidth

skelillegalparams = [
    color.ColorParameter('color', defaultSkelIllegalColor,
                         tip="Color for illegal elements."),
    parameter.IntRangeParameter('linewidth', widthRange, 
                                defaultSkelIllegalWidth,
                                tip="Line width")]

mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    "Illegal_Elements",
    ordering=8,
    callback=_setSkelIllegalParams,
    params=skelillegalparams,
    help="Set default parameters for displaying illegal skeleton elements.",
    discussion="""<para>

    Set the default parameters for the
    <xref linkend="RegisteredClass-SkeletonIllegalElementDisplay"/> that
    highlights the
    <link linkend="Section-Concepts-Skeleton-Illegality">illegal</link>
    &elems; in a graphics window.  See
    <xref linkend="RegisteredClass-SkeletonIllegalElementDisplay"/> for
    the details.  This command may be placed in the &oof2rc; file
    to set default values for all &oof2; sessions.
    
    </para>"""))

skeletonIllegalDisplay = registeredclass.Registration(
    'Illegal Elements',
    display.DisplayMethod,
    SkeletonIllegalElementDisplay,
    params=skelillegalparams,
    ordering=4.1,
    layerordering=display.SemiLinear(3.1),
    whoclasses=('Skeleton',),
    tip="Display illegal elements in a Skeleton",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/skeletonillegaldisplay.xml')
    )

def defaultSkeletonIllegalDisplay():
    return skeletonIllegalDisplay(color=defaultSkelIllegalColor,
                                  linewidth=defaultSkelIllegalWidth)

ghostgfxwindow.PredefinedLayer('Skeleton', '<topmost>',
                               defaultSkeletonIllegalDisplay)
