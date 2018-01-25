# -*- python -*-
# $RCSfile: voxelregionselectiondisplay.py,v $
# $Revision: 1.1.2.1 $
# $Author: rdw1 $
# $Date: 2015/08/07 12:45:05 $


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import coord
from ooflib.SWIG.common import direction
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

import math

# TODO: Finish writing this TODO list.

# VoxelRegionSelectionDisplay is a display method for the
# click-and-drag editing of voxel selection regions. 

# It is associated with a canvaslayer that contains a box-shaped
# vtkUnstructuredGrid with faces, edges, and vertices all as separate
# vtkCells, and a vtk arrow (to represent the direction in which
# things are being dragged).

# TODO: Once multiple voxel region selection tools are created
# (e.g. we have tools for selecting both a box-shaped region AND an
# ellipsoid-shaped region), they will either have to all share one
# VoxelRegionSelectionDisplay, or each use separate
# VoxelRegionSelectionDisplays. Figure out which of these two
# situation makes more sense, and make the changes necessary to make
# that situation work.

class VoxelRegionSelectionDisplay(display.DisplayMethod):
    def __init__(self, arrow_color, arrow_tip_radius, arrow_length, point_size, line_width, line_color, face_color, face_opacity):
        self.arrow_color = arrow_color
        self.arrow_tip_radius = arrow_tip_radius
        self.arrow_length = arrow_length
        self.point_size = point_size
        self.line_width = line_width
        self.line_color = line_color
        self.face_color = face_color
        self.face_opacity = face_opacity
        self.sbcallbacks = None
        display.DisplayMethod.__init__(self)

    def destroy(self, destroy_canvaslayer):
        if self.sbcallbacks is not None:
            map(switchboard.removeCallback, self.sbcallbacks)
            self.sbcallbacks = None
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

    def newLayer(self):
        # The following switchboard callbacks are used for updating
        # what is displayed in the layer.
        self.sbcallbacks = [switchboard.requestCallbackMain("region editing begun", self.beginRegion),
                            switchboard.requestCallbackMain("region editing finished", self.hideRegion)
                            ]

        # Create an object of class BoxAndArrowLayer.
        return canvaslayers.BoxAndArrowLayer(self.gfxwindow.oofcanvas,
                                             "BoxAndArrow") 

    def setParams(self):
        self.canvaslayer.set_totalVisibility(False)
        self.canvaslayer.set_arrowVisibility(False)
        self.canvaslayer.set_arrowColor(self.arrow_color)
        self.canvaslayer.set_arrowTipRadius(self.arrow_tip_radius)
        self.canvaslayer.set_arrowShaftRadius(0.3 * self.arrow_tip_radius)
        self.canvaslayer.set_arrowLength(self.arrow_length)
        self.canvaslayer.set_pointSize(self.point_size)
        self.canvaslayer.set_lineWidth(self.line_width)
        self.canvaslayer.set_lineColor(self.line_color)
        self.canvaslayer.set_faceColor(self.face_color)
        self.canvaslayer.set_faceOpacity(self.face_opacity)

    def beginRegion(self, gfxwindow):
        if gfxwindow is not self.gfxwindow:
            return
        microstructure = self.gfxwindow.findMicrostructure()
        if microstructure is None:
            return
        dimensions = microstructure.size()
        self.canvaslayer.set_box(dimensions)
        self.canvaslayer.setModified()
        self.canvaslayer.set_arrowVisibility(False)
        self.canvaslayer.set_totalVisibility(True)

    def hideRegion(self, gfxwindow):
        if gfxwindow is not self.gfxwindow:
            return
        self.canvaslayer.set_totalVisibility(False)

defaultVoxelRegionSelectionArrowColor = color.red
defaultVoxelRegionSelectionArrowTipRadius = 0.1
defaultVoxelRegionSelectionArrowLength = 0.5
defaultVoxelRegionSelectionPointSize = 5.0
defaultVoxelRegionSelectionLineWidth = 3.0
defaultVoxelRegionSelectionLineColor = color.blue
defaultVoxelRegionSelectionFaceColor = color.blue
defaultVoxelRegionSelectionFaceOpacity = 0.85
arrowRadiusRange = (0, 0.2, 0.02)
arrowLengthRange = (0.2, 1, 0.05)
pointSizeRange = (0, 15, 1)
lineWidthRange = (1, 10, 1)
opacityRange = (0, 1, 0.05)

def _setDefaultVoxelRegionSelectionParams(menuitem, arrow_color, arrow_tip_radius, arrow_length, plane_color, plane_opacity):
    global defaultVoxelRegionSelectionArrowColor
    defaultVoxelRegionSelectionArrowColor = arrow_color
    global defaultVoxelRegionSelectionArrowTipRadius
    defaultVoxelRegionSelectionArrowTipRadius = arrow_tip_radius
    global defaultVoxelRegionSelectionArrowLength
    defaultVoxelRegionSelectionArrowLength = arrow_length
    global defaultVoxelRegionSelectionPointSize
    defaultVoxelRegionSelectionPointSize = point_size
    global defaultVoxelRegionSelectionLineWidth
    defaultVoxelRegionSelectionLineWidth = line_width
    global defaultVoxelRegionSelectionLineColor
    defaultVoxelRegionSelectionLineColor = line_color
    global defaultVoxelRegionSelectionFaceColor
    defaultVoxelRegionSelectionFaceColor = face_color
    global defaultVoxelRegionSelectionFaceOpacity
    defaultVoxelRegionSelectionFaceOpacity = face_opacity

# Sizing and coloring options for the box and arrow. These can be
# set in the graphics defaults menu.
voxelregionselectionparams = [
    color.ColorParameter(
        'arrow_color', 
        defaultVoxelRegionSelectionArrowColor,
        tip="Color of the arrow."),
    parameter.FloatRangeParameter(
        'arrow_tip_radius', 
        arrowRadiusRange,
        defaultVoxelRegionSelectionArrowTipRadius,
        tip="Radius of the arrow tip."),
    parameter.FloatRangeParameter(
        'arrow_length', 
        arrowLengthRange,
        defaultVoxelRegionSelectionArrowLength,                                        
        tip="Length of the arrow."),
    parameter.FloatRangeParameter(
        'point_size', 
        pointSizeRange,
        defaultVoxelRegionSelectionPointSize,                                        
        tip="Size of the points on the corners of the box."),
    parameter.FloatRangeParameter(
        'line_width', 
        lineWidthRange,
        defaultVoxelRegionSelectionLineWidth,                                        
        tip="Width of the lines on the edges of the box."),
    color.ColorParameter(
        'line_color', 
        defaultVoxelRegionSelectionLineColor,                                             
        tip="Color for the edges of the box."), 
    color.ColorParameter(
        'face_color', 
        defaultVoxelRegionSelectionFaceColor,                                             
        tip="Color of the faces of the box."),                   
    parameter.FloatRangeParameter(
        'face_opacity', 
        opacityRange,                                                 
        defaultVoxelRegionSelectionFaceOpacity,                                             
        tip="Opacity of the faces of the box.")]

mainmenu.gfxdefaultsmenu.Voxel_Selection.addItem(oofmenu.OOFMenuItem(
    "Voxel_Region_Selection",
    callback=_setDefaultVoxelRegionSelectionParams,
    ordering=1,
    params=voxelregionselectionparams,
    help="Set default parameters for voxel region selection tools.",
    discussion="""<para>

    Set default parameters for <link linkend="RegisteredClass:VoxelRegionSelectionDisplay"><classname>VoxelRegionSelectionDisplays</classname></link>.
    See <xref linkend="RegisteredClass:VoxelRegionSelectionDisplay"/> for the details.

    </para>"""))

voxelRegionSelectionDisplay = registeredclass.Registration(
    'Voxel Region Click-and-Drag Editor',
    display.DisplayMethod,
    VoxelRegionSelectionDisplay,
    params=voxelregionselectionparams,
    ordering=3.1,
    layerordering=display.Celestial(0.5),
    whoclasses=('Microstructure'),
    tip="Display the widget for editing a region containing all the voxels to be selected."
    )

########################

from ooflib.common.IO import whoville

def predefinedVoxelRegionSelectionLayer():
    # When a new graphics window is opened, a
    # VoxelRegionSelectionDisplay will be automatically created with
    # the default sizing and coloring options.
    return VoxelRegionSelectionDisplay(
        arrow_color=defaultVoxelRegionSelectionArrowColor,
        arrow_tip_radius=defaultVoxelRegionSelectionArrowTipRadius,
        arrow_length=defaultVoxelRegionSelectionArrowLength,
        point_size=defaultVoxelRegionSelectionPointSize,
        line_width=defaultVoxelRegionSelectionLineWidth,
        line_color=defaultVoxelRegionSelectionLineColor,
        face_color=defaultVoxelRegionSelectionFaceColor,
        face_opacity=defaultVoxelRegionSelectionFaceOpacity)

ghostgfxwindow.PredefinedLayer('Microstructure', '<topmost>',
                               predefinedVoxelRegionSelectionLayer)
