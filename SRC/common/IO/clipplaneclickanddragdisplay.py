# -*- python -*-
# $RCSfile: clipplaneclickanddragdisplay.py,v $
# $Revision: 1.1.2.2 $
# $Author: rdw1 $
# $Date: 2015/08/06 21:52:01 $


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
from ooflib.common.IO import viewertoolbox
from ooflib.common.IO import xmlmenudump

import math

# The ClippingPlaneWidget class is an extension of the DisplayMethod
# class. The ClippingPlaneWidget controls a 3D graphical
# representation of a clipping plane that the user has currently
# selected in the "Viewer" toolbox.  This 3D graphical representation
# can be clicked and dragged to allow easy editing of clipping
# planes. It uses the class PlaneAndArrowLayer (described in the next
# paragraph) for the 3D graphical representation.

# ClippingPlaneWidget used to be called ClipPlaneClickAndDragDisplay,
# which was too long.  Some of the internal names in this file haven't
# been updated, though.

# An object of class PlaneAndArrowLayer contains two vtk actors: a
# plane, and an arrow which points out of the plane and represents the
# plane's normal vector.  Some properties of the plane-arrow pair,
# including direction of the normal vector and the location of the
# plane-arrow pair within the OOF 3D canvas, can be set in Python via
# the functions defined in canvaslayers.swg. The PlaneAndArrowLayer
# class is specified in canvaslayers.h.

class ClippingPlaneWidget(display.DisplayMethod):
    def __init__(self, arrow_color, arrow_tip_radius, arrow_length,
                 plane_color, plane_opacity,
                 hide_inactive, dim_inactive):
        self.arrow_color = arrow_color
        self.arrow_tip_radius = arrow_tip_radius
        self.arrow_length = arrow_length;
        self.plane_color = plane_color
        self.plane_opacity = plane_opacity
        self.hide_inactive = hide_inactive
        self.dim_inactive = dim_inactive

        # suppressClip indicates whether or not clipping is
        # suppressed.
        self.suppressClip = False
        
        self.sbcallbacks = []
        display.DisplayMethod.__init__(self)

    def destroy(self, destroy_canvaslayer):
        map(switchboard.removeCallback, self.sbcallbacks)
        self.sbcallbacks = []
        display.DisplayMethod.destroy(self, destroy_canvaslayer)

    def newLayer(self):
        self.toolbox = self.gfxwindow.getToolboxByName("Viewer")

        # The following switchboard callbacks are used for updating
        # what is displayed in the layer.
        self.sbcallbacks.extend([
            switchboard.requestCallbackMain(
                (self.toolbox, "clip selection changed"),
                self.setPlane),
            switchboard.requestCallbackMain(
                "view almost changed", self.updateScale),
            switchboard.requestCallbackMain("toolbox activated Viewer",
                                            self.activatedCB),
            switchboard.requestCallbackMain("toolbox deactivated Viewer",
                                            self.deactivatedCB)
        ])

        # Create an object of class PlaneAndArrowLayer.  The "False"
        # says that the arrow is oriented opposite to the positive
        # plane normal.
        return canvaslayers.PlaneAndArrowLayer(self.gfxwindow.oofcanvas,
                                               "PlaneAndArrow", False)

    def arrowSign(self, plane):
        # The arrow is flipped if the plane is flipped or if all
        # planes are inverted, but not both.
        if plane is not None and plane.flipped() != self.toolbox.invertClip:
            return -1
        return 1

    def planeExists(self):
        return not (self.suppressClip or
                    self.toolbox.currentClipPlane() is None)

    def opacityFactor(self):      # multiplies opacity when inactive
        if self.toolbox.active:
            return 1.0
        return 1. - self.dim_inactive
    
    def setParams(self):
        self.canvaslayer.set_arrowColor(self.arrow_color)
        self.canvaslayer.set_arrowTipRadius(self.arrow_tip_radius)
        if self.toolbox is not None:
            direction = self.arrowSign(self.toolbox.currentClipPlane())
            self.canvaslayer.set_arrowLength(direction * self.arrow_length)
        self.canvaslayer.set_arrowShaftRadius(0.3 * self.arrow_tip_radius)
        self.canvaslayer.set_planeColor(self.plane_color)
        self.canvaslayer.set_planeOpacity(
            self.plane_opacity*self.opacityFactor())
        self.canvaslayer.set_visibility(
            (self.toolbox.active or not self.hide_inactive) and
            self.planeExists())
        self.canvaslayer.setModified()

    def activatedCB(self, gfxwindow):
        if gfxwindow == self.gfxwindow:
            self.canvaslayer.set_visibility(self.planeExists())
            self.canvaslayer.set_planeOpacity(self.plane_opacity)
    def deactivatedCB(self, gfxwindow):
        if gfxwindow == self.gfxwindow:
            self.canvaslayer.set_visibility(not self.hide_inactive
                                            and self.planeExists())
            self.canvaslayer.set_planeOpacity(
                self.plane_opacity*self.opacityFactor())
            

    def setPlane(self, plane):
        # Switchboard callback for "clip selection changed".
        if plane is not None and not self.toolbox.suppressClip:
            # Display the selected plane even if it's not enabled.
            # The user may want to see what it will do.  This used to
            # check plane.enabled() and only display enabled planes.
            self.canvaslayer.set_visibility(True)
            normal = plane.normal()
            offset = plane.offset()
            self.canvaslayer.set_normal(normal)
            self.canvaslayer.offset(offset - self.canvaslayer.get_offset())
            self.canvaslayer.set_arrowLength(
                self.arrowSign(plane) * self.arrow_length)
            self.canvaslayer.setModified()
            return
        # There is no visible clipping plane.
        self.canvaslayer.set_visibility(False)

    def updateScale(self, gfxwindow):
        # Callback for "view almost changed". Updates the scale of the
        # displayed plane and arrow vtkActors, so that the plane fits
        # well into the viewing window when at at the focal distance
        # from the camera.
        if gfxwindow is self.gfxwindow:
            plane = self.toolbox.currentClipPlane()
            if plane is not None:
                dist = self.gfxwindow.oofcanvas.get_camera_distance()
                view_angle = self.gfxwindow.oofcanvas.get_camera_view_angle()
                scale = 0.5 * dist * math.tan(math.radians(view_angle))
                self.canvaslayer.set_scale(scale)      
            
defaultClipPlaneClickAndDragArrowColor = color.red
defaultClipPlaneClickAndDragArrowTipRadius = 0.1
defaultClipPlaneClickAndDragArrowLength = 0.5
defaultClipPlaneClickAndDragColor = color.red
defaultClipPlaneClickAndDragOpacity = 0.85
defaultHideInactive = False
defaultDimInactive = 0.5
radiusRange = (0, 0.2, 0.02)
lengthRange = (0.2, 1, 0.05)
opacityRange = (0, 1, 0.05)


def _setDefaultClipPlaneClickAndDragParams(menuitem,
                                           arrow_color, arrow_tip_radius,
                                           arrow_length,
                                           plane_color, plane_opacity,
                                           hide_inactive, dim_inactive):
    global defaultClipPlaneClickAndDragArrowColor
    defaultClipPlaneClickAndDragArrowColor = arrow_color
    global defaultClipPlaneClickAndDragArrowTipRadius
    defaultClipPlaneClickAndDragArrowTipRadius = arrow_tip_radius
    global defaultClipPlaneClickAndDragArrowLength
    defaultClipPlaneClickAndDragArrowLength = arrow_length
    global defaultClipPlaneClickAndDragColor
    defaultClipPlaneClickAndDragColor = plane_color
    global defaultClipPlaneClickAndDragOpacity
    defaultClipPlaneClickAndDragOpacity = plane_opacity
    global defaultHideInactive
    defaultHideInactive = hide_inactive
    global defaultDimInactive
    defaultDimInactive = dim_inactive
    

# Sizing and coloring options for the plane-arrow pair, which can be
# set in the graphics defaults menu.
clipplaneclickanddragparams = [
    color.ColorParameter(
        'arrow_color', 
        defaultClipPlaneClickAndDragArrowColor,
        tip="Color of the arrow representing the normal vector."),
    parameter.FloatRangeParameter(
        'arrow_tip_radius', 
        radiusRange,
        defaultClipPlaneClickAndDragArrowTipRadius,
        tip="Radius of the arrow tip."),
    parameter.FloatRangeParameter(
        'arrow_length', 
        lengthRange,
        defaultClipPlaneClickAndDragArrowLength,
        tip="Length of the arrow relative to the plane"),
    color.ColorParameter(
        'plane_color', 
        defaultClipPlaneClickAndDragColor,
        tip="Color of the plane."),                   
    parameter.FloatRangeParameter(
        'plane_opacity', 
        opacityRange,                                                 
        defaultClipPlaneClickAndDragOpacity,
        tip="Opacity of the plane."),
    parameter.BooleanParameter(
        'hide_inactive', defaultHideInactive,
        tip='Hide the widget when the toolbox is inactive'),
    parameter.FloatRangeParameter(
        'dim_inactive', opacityRange, defaultDimInactive,
        tip="Factor by which to decrease the opacity of an inactive widget.")
]

mainmenu.gfxdefaultsmenu.Clipping_Planes.addItem(oofmenu.OOFMenuItem(
    "Click_And_Drag_Editing",
    callback=_setDefaultClipPlaneClickAndDragParams,
    ordering=1,
    params=clipplaneclickanddragparams,
    help="Set default parameters for viewing and click-and-drag editing of clipping planes.",
    discussion="""<para>
    Set default parameters for <link linkend="RegisteredClass:ClippingPlaneWidget"><classname>ClippingPlaneWidget</classname></link>.
    See <xref linkend="RegisteredClass:ClippingPlaneWidget"/> for the details.
    </para>"""))

clipPlaneClickAndDragDisplay = registeredclass.Registration(
    'Clipping Plane Click-and-Drag Editor',
    display.DisplayMethod,
    ClippingPlaneWidget,
    params=clipplaneclickanddragparams,
    ordering=3.0,
    layerordering=display.Celestial,
    whoclasses=('Microstructure'),
    tip="Display the widget for viewing and click-and-drag editing of clipping planes."
    )

########################

from ooflib.common.IO import whoville

def predefinedClipPlaneClickAndDragLayer():
    # When a new graphics window is opened, a
    # ClippingPlaneWidget will be automatically created with
    # the default sizing and coloring options.
    return ClippingPlaneWidget(
        arrow_color = defaultClipPlaneClickAndDragArrowColor,
        arrow_tip_radius = defaultClipPlaneClickAndDragArrowTipRadius,
        arrow_length = defaultClipPlaneClickAndDragArrowLength,
        plane_color = defaultClipPlaneClickAndDragColor,
        plane_opacity = defaultClipPlaneClickAndDragOpacity,
        hide_inactive = defaultHideInactive,
        dim_inactive = defaultDimInactive)

ghostgfxwindow.PredefinedLayer('Microstructure', '<topmost>',
                               predefinedClipPlaneClickAndDragLayer)
