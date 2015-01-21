# -*- python -*-
# $RCSfile: meshinfodisplay.py,v $
# $Revision: 1.27.10.27 $
# $Author: langer $
# $Date: 2014/09/10 21:28:43 $

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

## TODO 3.1: MeshInfoDisplay and SkeletonInfoDisplay share a lot of code
## and should have a common base class (other than just
## DisplayMethod).

class MeshInfoDisplay(display.DisplayMethod):
    def __init__(self, query_color, peek_color, node_size,
                 line_width):
        self.query_color = query_color
        self.peek_color = peek_color
        self.colors = {"query": self.query_color, "peek": self.peek_color}
        self.node_size = node_size
        self.line_width = line_width
        self.tbcallbacks = []
        display.DisplayMethod.__init__(self)
        self.drawFuncs = {"Element": self.drawElement,
                          "Node": self.drawNode}

    ## TODO 3.1: Add Segment and Face modes, later, when interface physics
    ## is added.
    layerNames = ["Element", "Node"] # all sublayers
    linearLayerNames = ["Element"] # sublayers drawn with lines
    # if config.dimension() == 3:
    #     layerNames.append("Face")
    #     linearLayerNames.append("Face")

    def destroy(self, destroy_canvaslayer):
        map(switchboard.removeCallback, self.tbcallbacks)
        self.tbcallbacks = []
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

    def draw(self, gfxwindow, device): # 2D only
        toolbox = gfxwindow.getToolboxByName("Mesh_Info")
        mesh = toolbox.meshcontext()
        mesh.begin_reading()
        mesh.restoreCachedData(gfxwindow.displayTime)
        try:
            # Drawing "queried" item.
            if toolbox.querier and toolbox.querier.object:
                self.drawFuncs[toolbox.querier.targetname](device, toolbox, 
                                                           toolbox.querier.object,
                                                           which="query")
            # Drawing "peeked" item.
            if toolbox.peeker and toolbox.peeker.objects.values():
                for objtype in toolbox.peeker.objects:
                    if toolbox.peeker.objects[objtype]:
                        self.drawFuncs[objtype](device, toolbox, 
                                                toolbox.peeker.objects[objtype],
                                                which="peek")
        finally:
            mesh.releaseCachedData()
            mesh.end_reading()

    def drawElement(self, device, toolbox, element, which="query"): # 2D only
        device.set_lineColor(self.colors[which])
        device.set_lineWidth(self.line_width)
        if config.dimension() == 2:
            node_iter = element.cornernode_iterator().exteriornode_iterator()
            p_list = [node.position() for node in node_iter]
            displaced_p_list = [
                toolbox.meshlayer.displaced_from_undisplaced(
                toolbox.gfxwindow, x) for x in p_list]
            for i in range(len(displaced_p_list)):
                p0 = displaced_p_list[i]
                p1 = displaced_p_list[(i+1)%len(displaced_p_list)]
                device.draw_segment(primitives.Segment(p0, p1))
        elif config.dimension() == 3:
            device.draw_cell(element)


    def drawNode(self, device, toolbox, node, which="query"): # 2D only
        device.set_lineColor(self.colors[which])
        device.set_lineWidth(self.node_size)
        if config.dimension() == 2:
            displaced_position = toolbox.meshlayer.displaced_from_undisplaced(
                toolbox.gfxwindow(), node.position())
            device.draw_dot(displaced_position)
        elif config.dimension() == 3:
            device.draw_dot(node.position())

    # def getTimeStamp(self, gfxwindow): # 2D only
    #     toolbox = gfxwindow.getToolboxByName("Mesh_Info")
    #     if toolbox.querier and toolbox.peeker:
    #         return max(self.timestamp,
    #                    gfxwindow.displayTimeChanged,
    #                    toolbox.querier.getTimeStamp(),
    #                    toolbox.peeker.getTimeStamp())
    #     elif toolbox.querier and not toolbox.peeker:
    #         return max(self.timestamp,
    #                    gfxwindow.displayTimeChanged,
    #                    toolbox.querier.getTimeStamp())
    #     else:
    #         return self.timestamp

    def newLayer(self):
        layer = canvaslayers.ComboCanvasLayer()
        canvas = self.gfxwindow.oofcanvas
        # The names of the layers here must correspond to the
        # targetnames used in meshinfo.py.  "Face" and "Segment"
        # aren't use there currently (4/2012) but may be added later,
        # so they're included here (but not tested!).
        layer.addSublayer(
            "Element",
            canvaslayers.SimpleWireframeCellLayer(canvas, True, 
                                                  "ElementMeshInfo"))
        # layer.addSublayer(
        #     "Face",
        #     canvaslayers.SimpleWireframeCellLayer(canvas, True,
        #                                           "FaceMeshInfo"))
        # layer.addSublayer(
        #     "Segment",
        #     canvaslayers.SimpleWireframeCellLayer(canvas, False,
        #                                           "SegmentMeshInfo"))
        layer.addSublayer(
            "Node",
            canvaslayers.SimplePointCellLayer(canvas, "NodeMeshInfo"))
        self.tbcallbacks = [
            switchboard.requestCallbackMain((self.gfxwindow, "query Mesh"),
                                            self.queryCB),
            switchboard.requestCallbackMain((self.gfxwindow, "peek Mesh"),
                                            self.peekCB),
            switchboard.requestCallbackMain("mesh data changed",
                                            self.meshDataChangedCB)
            ]
        return layer

    def setParams(self):
        toolbox = self.gfxwindow.getToolboxByName("Mesh_Info")
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

    def queryCB(self):          # sb (gfxwindow, "query Mesh")
        toolbox = self.gfxwindow.getToolboxByName("Mesh_Info")
        if toolbox.meshlayer:
            # The queried object or peeked objects may have changed, which
            # changes the color assignments, so call setParams.
            self.setParams()
            meshctxt = self.who().resolve(self.gfxwindow)
            if meshctxt:
                querymode, queryobj = toolbox.getQueryObject()
                if queryobj:
                    for lname in self.layerNames:
                        layer = self.canvaslayer.getSublayer(lname)
                        if lname == querymode.targetName: # draw query sublayer
                            meshsrc = toolbox.meshlayer.source
                            queryobj.drawGridCell(meshsrc, layer)
                        else:
                            layer.clear() # clear peek sublayers
                    return
        self.canvaslayer.clear() # clear all sublayers

    def peekCB(self, peekmode): # sb (gfxwindow, "peek Mesh")
        toolbox = self.gfxwindow.getToolboxByName("Mesh_Info")
        if toolbox.meshlayer:
            meshctxt = self.who().resolve(self.gfxwindow)
            if meshctxt:
                peekobj = toolbox.getPeekObject(peekmode)
                sublayer = self.canvaslayer.getSublayer(peekmode.targetName)
                if peekobj:
                    meshsrc = toolbox.meshlayer.source
                    peekobj.drawGridCell(meshsrc, sublayer)
                else:
                    sublayer.clear()

    def meshDataChangedCB(self, meshctxt):
        if meshctxt is self.who().resolve(self.gfxwindow):
            self.queryCB()
            toolbox = self.gfxwindow.getToolboxByName("Mesh_Info")
            for mode in toolbox.allPeekModes():
                self.peekCB(mode)

# This object should be created via the registration, and not
# directly via the initializer, because the registration creation
# method gives it a timestamp.

defaultQueryColor = color.RGBColor(0.0, 0.4, 0.85)
defaultPeekColor = color.RGBColor(0.9, 0.5, 0.5)
if config.dimension() == 2:
    widthRange = (0,10)
    defaultNodeSize = 3
    defaultLineWidth = 2
elif config.dimension() == 3:
    widthRange = (1,20)        # In vtk, line widths of 0 cause errors
    defaultNodeSize = 10
    defaultLineWidth = 4

def _setMeshInfoParams(menuitem, query_color, peek_color, node_size,
                       line_width):
    global defaultQueryColor
    global defaultPeekColor
    global defaultNodeSize
    global defaultLineWidth
    defaultQueryColor = query_color
    defaultPeekColor = peek_color
    defaultNodeSize = node_size
    defaultLineWidth = line_width

meshinfoparams = [
    color.ColorParameter('query_color', defaultQueryColor,
                         tip="Color for the queried object."),
    color.ColorParameter('peek_color', defaultPeekColor,
                         tip="Color for the peeked object."),
    parameter.IntRangeParameter('node_size', widthRange, defaultNodeSize,
                                tip="Node size."),
    parameter.IntRangeParameter('line_width', widthRange,
                                defaultLineWidth,
                                tip="Line thickness for element edge.")]

mainmenu.gfxdefaultsmenu.Meshes.addItem(oofmenu.OOFMenuItem(
    "Mesh_Info",
    callback=_setMeshInfoParams,
    params=meshinfoparams,
    ordering=1,
    help="Set default parameters for Mesh Info displays.",
    discussion="""<para>

    Set default parameters for
    <link linkend="RegisteredClass-MeshInfoDisplay"><classname>MeshInfoDisplays</classname></link>.
    See <xref linkend="RegisteredClass-MeshInfoDisplay"/> for the details.
    This command may be placed in the &oof2rc; file to set a default value
    for all &oof2; sessions.
    
    </para>"""))

meshInfoDisplay = registeredclass.Registration(
    'Info',
    display.DisplayMethod,
    MeshInfoDisplay,
    params=meshinfoparams,
    ordering=4.0,
    layerordering=display.PointLike(100),
    whoclasses=('Mesh',),
    tip="Set display parameters for the decorations used by the Mesh Info toolbox.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/meshinfodisplay.xml')
    )

def defaultMeshInfoDisplay():
    return meshInfoDisplay(query_color=defaultQueryColor,
                           peek_color=defaultPeekColor,
                           node_size=defaultNodeSize,
                           line_width=defaultLineWidth)

ghostgfxwindow.PredefinedLayer('Mesh', '<topmost>', defaultMeshInfoDisplay)
