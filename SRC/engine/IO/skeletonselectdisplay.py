# -*- python -*-
# $RCSfile: skeletonselectdisplay.py,v $
# $Revision: 1.1.2.34 $
# $Author: langer $
# $Date: 2014/11/07 22:33:27 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## TODO 3.1: Opacity shouldn't be a separate parameter if translucent
## colors are available.  It might be simpler simply to not have
## translucent colors as parameters, and get rid of the translucent
## color class.  Opacity can be a separate parameter.

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
from ooflib.engine import skeletonselmodebase


class SkeletonSelectionDisplay(display.DisplayMethod):
    def __init__(self, mode):
        display.DisplayMethod.__init__(self)
        self.mode = mode
        self.tbcallbacks = [] 
        
    def nameClass(self):
      return "SkeletonSelectionDisplay"

    def draw(self, gfxwindow, canvas): # This is only used in 2D
        skel = self.who().resolve(gfxwindow)
        if skel is not None:
            self.set_params(canvas)
            selection = self.mode.getSelectionContext(skel)
            # selection = skel.__dict__[self.selectiontype] 
            selection.begin_reading()
            try:
                selectables = selection.retrieve()
                numCells = len(selectables)
                if numCells:
                    canvas.create_grid(skel.getObject().getPoints(), numCells, 
                                       True)
                    for s in selectables:
                        canvas.add_cell_to_grid(s.getCellType(),
                                                s.getPointIds())
                        
            finally:
                selection.end_reading()  

    def setupSignals(self):
        self.tbcallbacks.append(switchboard.requestCallbackMain(
                self.mode.changedselectionsignal, self.changedSelectionCB))

    def changedSelectionCB(self, selection):
        skel = self.who().resolve(self.gfxwindow)
        
        # selection = self.mode.getSelectionContext(skel)
        if skel and selection is self.mode.getSelectionContext(skel):
            self.updateSelection(skel, selection)
            # selectables = selection.retrieve()
            # numCells = len(selectables)
            # self.canvaslayer.newGrid(skel.getObject().getPoints(), numCells)
            # for s in selectables:
            #     self.canvaslayer.addCell(s.getCellType(), s.getPointIds())

    def whoChanged(self):
        skel = self.who().resolve(self.gfxwindow)
        if skel is not None:
            self.updateSelection(skel, self.mode.getSelectionContext(skel))
        else:
            self.canvaslayer.clear()
        return True

    def updateSelection(self, skelctxt, selection):
        ## TODO 3.1: This ought to acquire the selection's read lock, but
        ## it can't because it's running on the main thread.  See TODO 3.1
        ## LOCK in display.py
        cskeletonselectable.rebuildLayerCells(
            skelctxt.getObject(),
            self.canvaslayer,
            selection.currentSelectionTracker())
	
    def destroy(self, destroy_canvaslayer):
        map(switchboard.removeCallback, self.tbcallbacks)
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# The default opacity for selected elements is 1.0, because if it's
# less than that they (sometimes) don't show up when superimposed on
# an opaque image.
defaultSelectedElementColor = color.RGBColor(0.88, 0.14, 0.07)
defaultSelectedElementOpacity = 0.7

class SkeletonElementSelectionDisplay(SkeletonSelectionDisplay):
    def __init__(self, color, opacity):
        self.color = color
        self.opacity = opacity
        SkeletonSelectionDisplay.__init__(
            self, skeletonselmodebase.getMode("Element"))
        
    def newLayer(self):
        self.setupSignals()
        return canvaslayers.SimpleFilledCellLayer(self.gfxwindow.oofcanvas, 
                                                  "SkeletonSelectedElement")

    def nameClass(self):
      return "SkeletonElementSelectionDisplay"

    def setParams(self):
        self.canvaslayer.set_color(self.color)
        self.canvaslayer.set_opacity(self.opacity)

def _setSelectedElementParams(menuitem, color, opacity):
    global defaultSelectedElementColor
    global defaultSelectedElementOpacity
    defaultSelectedElementColor = color
    defaultSelectedElementOpacity = opacity

selectedElementParams = [
    color.ColorParameter('color', defaultSelectedElementColor,
                         tip="Color for the selected elements."),
    parameter.FloatRangeParameter('opacity', (0., 1., 0.01),
                                  defaultSelectedElementOpacity,
                                  tip="Opacity of the selected elements.")]

mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    'Selected_Elements',
    callback=_setSelectedElementParams,
    ordering=1,
    params=selectedElementParams,
    help="Set default parameters for displaying selected skeleton elements.",
    discussion="""<para>

    Set default parameters for the
    <xref linkend="RegisteredClass:SkeletonElementSelectionDisplay"/>,
    which displays the currently selected &skel; &elems; in the graphics
    window.  See
    <xref linkend="RegisteredClass:SkeletonElementSelectionDisplay"/>
    for a discussion of the parameters. This command may be put in the
    &oof2rc; file to set defaults for all &oof2; sessions.
    
    </para>"""))

elementSelectDisplay = registeredclass.Registration(
    'Selected Elements',
    display.DisplayMethod,
    SkeletonElementSelectionDisplay,
    params=selectedElementParams,
    ordering=2.0,
    layerordering=display.SemiPlanar,
    whoclasses=('Skeleton',),
    tip="Display the currently selected elements",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/elementselectdisplay.xml'))
                                                

def predefinedElemSelLayer():
    return elementSelectDisplay(color=defaultSelectedElementColor,
                                opacity=defaultSelectedElementOpacity)

ghostgfxwindow.PredefinedLayer('Skeleton', '<topmost>', predefinedElemSelLayer)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkeletonFaceSelectionDisplay(SkeletonSelectionDisplay):
    def __init__(self, color, opacity):
        self.color = color
        self.opacity = opacity
        SkeletonSelectionDisplay.__init__(
            self, skeletonselmodebase.getMode("Face"))

    def newLayer(self):
        self.setupSignals()
        return canvaslayers.SimpleFilledCellLayer(self.gfxwindow.oofcanvas,
                                                  "SkeletonSelectedFace")

    def setParams(self):
        self.canvaslayer.set_color(self.color)
        self.canvaslayer.set_opacity(self.opacity)

defaultSelectedFaceColor = color.RGBColor(0.33, 0.0, 1)
defaultSelectedFaceOpacity = 0.7

def _setSelectedFaceParams(menuitem, color, opacity):
    global defaultSelectedFaceColor
    global defaultSelectedFaceOpacity
    defaultSelectedFaceColor = color
    defaultSelectedFaceOpacity = opacity

selectedFaceParams = [
    color.ColorParameter('color', defaultSelectedFaceColor,
                         tip="Color for the selected faces."),
    parameter.FloatRangeParameter('opacity', (0., 1., 0.01),
                                  defaultSelectedFaceOpacity,
                                  tip="Opacity of the selected faces.")]

mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    'Selected_Faces',
    callback=_setSelectedFaceParams,
    ordering=1,
    params=selectedFaceParams,
    help="Set default parameters for displaying selected skeleton faces.",
    discussion="""<para>

    Set default parameters for the
    <xref linkend="RegisteredClass:SkeletonFaceSelectionDisplay"/>,
    which displays the currently selected &skel; &faces; in the graphics
    window.  See
    <xref linkend="RegisteredClass:SkeletonFaceSelectionDisplay"/>
    for a discussion of the parameters. This command may be put in the
    &oof2rc; file to set defaults for all &oof2; sessions.
    
    </para>"""))

faceSelectDisplay = registeredclass.Registration(
    'Selected Faces',
    display.DisplayMethod,
    SkeletonFaceSelectionDisplay,
    params=selectedFaceParams,
    ordering=2.0,
    layerordering=display.SemiPlanar,
    whoclasses=('Skeleton',),
    tip="Display the currently selected faces",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/faceselectdisplay.xml'))
                                                

def predefinedFaceSelLayer():
    return faceSelectDisplay(color=defaultSelectedFaceColor,
                                opacity=defaultSelectedFaceOpacity)

ghostgfxwindow.PredefinedLayer('Skeleton', '<topmost>', predefinedFaceSelLayer)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

defaultSegSelColor = color.RGBColor(0.7, 0.1, 0.1)
defaultSegSelWidth = 5

class SkeletonSegmentSelectionDisplay(SkeletonSelectionDisplay):
    def __init__(self, color, line_width):
        self.color = color
        self.line_width = line_width
        SkeletonSelectionDisplay.__init__(
            self, skeletonselmodebase.getMode("Segment"))

    def newLayer(self):
        self.setupSignals()
        # The second arg to the SimpleWireframeCellLayer constructor
        # tells it not to extract edges from the cells (because the
        # cells will already be edges).
        return canvaslayers.SimpleWireframeCellLayer(
            self.gfxwindow.oofcanvas, False, "SkeletonSelectedSegment")

    def setParams(self):
        self.canvaslayer.set_color(self.color)
        self.canvaslayer.set_lineWidth(self.line_width)


def _setSegSelParams(menuitme, color, line_width):
    global defaultSegSelColor
    global defaultSegSelWidth
    defaultSegSelColor = color
    defaultSegSelWidth = line_width

segselparams = [
    color.ColorParameter('color', defaultSegSelColor,
                         tip="Color for the selected segments."),
    parameter.FloatRangeParameter('line_width', (0,10,0.1), defaultSegSelWidth,
                                  tip="Line width.")]

mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    'Selected_Segments',
    callback=_setSegSelParams,
    ordering=3,
    params=segselparams,
    help="Set default parameters for displaying selected skeleton segments.",
    discussion="""<para>

    Set default parameters for the
    <xref linkend="RegisteredClass:SkeletonSegmentSelectionDisplay"/>,
    which displays the currently selected &skel; &sgmts; in the graphics
    window.  See
    <xref linkend="RegisteredClass:SkeletonSegmentSelectionDisplay"/>
    for a discussion of the parameters. This command may be put in the
    &oof2rc; file to set defaults for all &oof2; sessions.
    
    </para>"""))

segmentSelectDisplay = registeredclass.Registration(
    'Selected Segments',
    display.DisplayMethod,
    SkeletonSegmentSelectionDisplay,
    params=segselparams,
    ordering=2.1,
    layerordering=display.SemiLinear(4),
    whoclasses=('Skeleton',),
    tip="Display the currently selected segments.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/engine/reg/segmentselectdisplay.xml')
    )

def defaultSegmentSelectDisplay():
    return segmentSelectDisplay(color=defaultSegSelColor,
                                line_width=defaultSegSelWidth)

ghostgfxwindow.PredefinedLayer('Skeleton', '<topmost>',
                               defaultSegmentSelectDisplay)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SkeletonNodeSelectionDisplay(SkeletonSelectionDisplay):
    def __init__(self, color, size):
        self.color = color
        self.size = size
        SkeletonSelectionDisplay.__init__(
            self, skeletonselmodebase.getMode("Node"))

    def newLayer(self):
        self.setupSignals()
        return canvaslayers.SimplePointCellLayer(self.gfxwindow.oofcanvas,
                                                 "SkeletonSelectedNode")
    
    def setParams(self):
        self.canvaslayer.set_color(self.color)
        self.canvaslayer.set_pointSize(self.size)



defaultNodeSelColor = color.RGBColor(0.07, 0.09, 0.96)
defaultNodeSelSize = 8.

def _setNodeSelParams(menuitem, color, size):
    global defaultNodeSelColor
    global defaultNodeSelSize
    defaultNodeSelColor = color
    defaultNodeSelSize = size

nodeselparams = [
    color.ColorParameter('color', defaultNodeSelColor,
                         tip="Color for the selected nodes."),
    parameter.FloatRangeParameter('size', (0,20,0.1), defaultNodeSelSize,
                                  tip="Node size.")]

mainmenu.gfxdefaultsmenu.Skeletons.addItem(oofmenu.OOFMenuItem(
    'Selected_Nodes',
    callback=_setNodeSelParams,
    ordering=2,
    params=nodeselparams,
    help="Set default parameters for displaying selected skeleton nodes.",
    discussion="""<para>

    Set default parameters for the
    <xref linkend="RegisteredClass:SkeletonNodeSelectionDisplay"/>,
    which displays the currently selected &skel; &nodes; in the graphics
    window.  See
    <xref linkend="RegisteredClass:SkeletonNodeSelectionDisplay"/>
    for a discussion of the parameters. This command may be put in the
    &oof2rc; file to set defaults for all &oof2; sessions.
    
    </para>"""))

nodeSelectDisplay = registeredclass.Registration(
    'Selected Nodes',
    display.DisplayMethod,
    SkeletonNodeSelectionDisplay,
    params=nodeselparams,
    ordering=2.2,
    layerordering= display.PointLike(3),
    whoclasses=('Skeleton',),
    tip="Display the currently selected nodes.",
    discussion=xmlmenudump.loadFile(
        'DISCUSSIONS/engine/reg/nodeselectdisplay.xml')
    )

def defaultNodeSelectDisplay():
    return nodeSelectDisplay(color=defaultNodeSelColor, size=defaultNodeSelSize)

ghostgfxwindow.PredefinedLayer('Skeleton', '<topmost>',
                               defaultNodeSelectDisplay)
