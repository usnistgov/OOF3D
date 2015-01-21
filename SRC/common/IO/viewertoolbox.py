# -*- python -*-
# $RCSfile: viewertoolbox.py,v $
# $Revision: 1.4.18.26 $
# $Author: langer $
# $Date: 2014/09/22 18:53:09 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config

from ooflib.SWIG.common import clip
from ooflib.SWIG.common import direction
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO import view
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import primitives
from ooflib.common import toolbox
from ooflib.common import utils
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter

import math

# Toolbox for controlling how the Microstructure, etc, is viewed on
# the graphics window's canvas.  It sets and displays the camera
# parameters and the clipping planes.

class ViewNameParameter(parameter.StringParameter):
    pass

## TODO 3.1: The user should be able to define sets of clipping planes.
## There should be a separate chooser for switching clipping plane
## sets.  The view chooser should not change the clipping planes.

# Switchboard signals:
# "view changed" (gfxwindow, name) 
#    sent by _updateView, _clipPlanesChanged, saveView
#      _updateView called by dollyIn, etc, restoreNamedView
#      _clipPlanesChanged called by newClipCB, editClipCB, etc,
#    caught by ViewerToolbox3DGUI - updates view chooser, camera info, historian
# "clip planes changed" (gfxwindow)
#    sent by _clipPlanesChanged, restoreView
#       restoreView is menuitem callback for Prev, Next buttons
#    caugth by ViewerToolbox3DGUI - updates list of clip planes
# "new view" (name) 
#    sent by saveView menuitem
#    caught by ViewerToolbox3DGUI - updates view chooser, *not* historian
# "view restored" (gfxwindow)
#    sent by restoreView
#    caught by ViewerToolbox3DGUI - updates view chooser, camera info
#     Does *not* call historian.record, unlike "view changed"
# "view deleted"
#    sent by deleteView
#    caught by ViewerToolbox3DGUI - updates view chooser

# There are two kinds of stored views: predefined views aren't
# computed until they're used, because they depend on the
# microstructure dimensions.  User defined views are just constants.

class PredefinedView:
    deletable = False
    def __init__(self, axis, sign):
        # PredefinedViews have the camera on one of the axes.
        self.axis = axis        # axis containing camera: 0=x, 1=y, 2=z
        self.sign = sign        # direction along axis: +1 or -1
    def resolve(self, gfxwindow):
        ms = gfxwindow.findMicrostructure()
        if ms is not None:
            bounds = ms.size()
            up = primitives.Point(0.,0.,0.)
            center = bounds/2.
            if self.axis == 1:
                up[2] = self.sign
            else:
                up[1] = 1
            # Set the distance so that the visible side of the
            # Microstructure is entirely visible, given the camera
            # angle. 
            angle = 30.
            
            # depth is the distance from the center to the edge of the
            # Microstructure in the direction of the camera.
            depth = bounds[self.axis]/2.0
            # width is the maximum distance from the center to the
            # edge in the other two directions.
            width = max(bounds[(self.axis+1)%3], bounds[(self.axis+2)%3])/2.0
            # dist is the distance from the face of the microstructure
            # to the camera.  It includes a fudge factor so that the
            # microstructure doesn't completely fill the view.
            dist = 1.3*width/math.tan(math.radians(angle/2.))
            
            pos = bounds/2.     # center of Microstructure
            pos[self.axis] = pos[self.axis] + self.sign*(dist + depth)
            return view.View(pos, center, up, angle, [], False)
        # If no Microstructure was found, the View can't be defined,
        # so just use the current camera settings.
        return mainthread.runBlock(gfxwindow.oofcanvas.get_view)
    def findName(self):
        # This is a hack for debugging... There isn't any other reason
        # for PredefinedViews to know their names.
        for name, view in namedViews.items():
            if isinstance(view, PredefinedView):
                if view.axis == self.axis and view.sign == self.sign:
                    return name
    def __repr__(self):
        return self.__class__.__name__ + "('" + self.findName() + "')"

class UserDefinedView:
    deletable = True
    def __init__(self, view):
        self.view = view
    def resolve(self, gfxwindow):
        return self.view

namedViews = utils.OrderedDict()

def storeView(name, view):
    if name in namedViews and not namedViews[name].deletable:
        raise ooferror.ErrUserError("Attempt to overwrite a predefined View.")
    namedViews[name] = view

def retrieveView(name, gfxwindow):
    view = namedViews[name]
    # For UserDefinedViews, resolve() just returns the View.  For
    # PredefinedViews, resolve() makes sure that the whole
    # Microstructure is visible.
    return view.resolve(gfxwindow)

# retrieveViewNames is used when setting the view chooser widgets in
# the Viewer toolbox and the canvas toolbar.  It returns the name of
# the current view and the set of names that the chooser should
# display.
def retrieveViewNames(gfxwindow):
    view = gfxwindow.oofcanvas.get_view()
    for (name, namedview) in namedViews.items():
        vue = namedview.resolve(gfxwindow)
        if view.equiv(vue):
            return (name, namedViews.keys())
    return ("", namedViews.keys() + [""])

def viewNames():
    return namedViews.keys()

storeView("Front", PredefinedView(2, 1))
storeView("Back", PredefinedView(2, -1))
storeView("Left", PredefinedView(0, -1))
storeView("Right", PredefinedView(0, 1))
storeView("Top", PredefinedView(1, 1))
storeView("Bottom", PredefinedView(1, -1))

class ViewNameParameter(parameter.StringParameter):
    pass

class ViewerToolbox(toolbox.Toolbox):
    def __init__(self, gfxwindow):
        toolbox.Toolbox.__init__(self, 'Viewer', gfxwindow)
    tip="Seeing is believing."
    discussion="TODO 3.1: write this."

    if config.dimension() == 3:
        def makeMenu(self, menu):
            self.menu = menu
            dollymenu = menu.addItem(oofmenu.OOFMenuItem("Dolly", cli_only=1))
            dollymenu.addItem(oofmenu.OOFMenuItem(
                    "In",
                    callback=self.dollyIn,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("factor")]))
            dollymenu.addItem(oofmenu.OOFMenuItem(
                    "Out",
                    callback=self.dollyOut,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("factor")]))
            dollymenu.addItem(oofmenu.OOFMenuItem(
                    "Fill",
                    threadable=oofmenu.UNTHREADABLE,
                    callback=self.dollyFill))
            trackmenu = menu.addItem(oofmenu.OOFMenuItem("Track", cli_only=1))
            trackmenu.addItem(oofmenu.OOFMenuItem(
                    "Horizontal",
                    callback=self.trackHoriz,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("distance")]))
            trackmenu.addItem(oofmenu.OOFMenuItem(
                    "Vertical",
                    callback=self.trackVert,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("distance")]))
            trackmenu.addItem(oofmenu.OOFMenuItem(
                    "Recenter",
                    callback=self.recenter))

            rotatemenu = menu.addItem(oofmenu.OOFMenuItem("Rotate", cli_only=1))
            rotatemenu.addItem(oofmenu.OOFMenuItem(
                    "Roll",
                    callback=self.roll,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("angle")]))
            rotatemenu.addItem(oofmenu.OOFMenuItem(
                    "Azimuth",
                    callback=self.azimuth,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("angle")]))
            rotatemenu.addItem(oofmenu.OOFMenuItem(
                    "Elevation",
                    callback=self.elevation,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("angle")]))
            rotatemenu.addItem(oofmenu.OOFMenuItem(
                    "Yaw",
                    callback=self.yaw,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("angle")]))
            rotatemenu.addItem(oofmenu.OOFMenuItem(
                    "Pitch",
                    callback=self.pitch,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("angle")]))

            zoommenu = menu.addItem(oofmenu.OOFMenuItem("Zoom", cli_only=1))
            zoommenu.addItem(oofmenu.OOFMenuItem(
                    "In",
                    callback=self.zoomIn,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("factor")]))
            zoommenu.addItem(oofmenu.OOFMenuItem(
                    "Out",
                    callback=self.zoomOut,
                    threadable=oofmenu.UNTHREADABLE,
                    params=[parameter.FloatParameter("factor")]))
            zoommenu.addItem(oofmenu.OOFMenuItem(
                    "Fill",
                    threadable=oofmenu.UNTHREADABLE,
                    callback=self.zoomFill))

            clipmenu = menu.addItem(oofmenu.OOFMenuItem("Clip", cli_only=1))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "New",
                    callback=self.newClipCB,
                    params=[
                        parameter.ConvertibleRegisteredParameter(
                            "normal", direction.Direction, 
                            direction.DirectionX()),
                        parameter.FloatParameter(
                            "offset", 0.0)]))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "Edit",
                    callback=self.editClipCB,
                    params=[parameter.IntParameter("plane"),
                            parameter.ConvertibleRegisteredParameter(
                                "normal", direction.Direction),
                            parameter.FloatParameter("offset")]
                    ))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "Delete",
                    callback=self.delClipCB,
                    params=[parameter.IntParameter("plane")]
                    ))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "Enable",
                    callback=self.clipEnableCB,
                    params=[parameter.IntParameter("plane")]
                    ))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "Disable",
                    callback=self.clipDisableCB,
                    params=[parameter.IntParameter("plane")]
                    ))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "Flip",
                    callback=self.clipFlipCB,
                    params=[parameter.IntParameter("plane")]
                    ))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "Unflip",
                    callback=self.clipUnflipCB,
                    params=[parameter.IntParameter("plane")]
                    ))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "InvertOn",
                    callback=self.clipInvertOnCB))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "InvertOff",
                    callback=self.clipInvertOffCB))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "SuppressOn",
                    callback=self.clipSuppressOnCB))
            clipmenu.addItem(oofmenu.OOFMenuItem(
                    "SuppressOff",
                    callback=self.clipSuppressOffCB))
                         
            menu.addItem(oofmenu.OOFMenuItem(
                    "Restore_View",
                    callback=self.restoreView,
                    params=[view.ViewParameter("view")]))
            menu.addItem(oofmenu.OOFMenuItem(
                    "Restore_Named_View",
                    callback=self._restoreNamedView,
                    params=[ViewNameParameter("view")])
                         )
            menu.addItem(oofmenu.OOFMenuItem(
                    "Save_View",
                    callback=self.saveView,
                    params=[parameter.StringParameter("name")]))
            menu.addItem(oofmenu.OOFMenuItem(
                    "Delete_View",
                    callback=self.deleteView,
                    params=[ViewNameParameter(
                            "view", tip="The name of the View to delete.")
                            ]
                    ))

        def _updateView(self):
            self.gfxwindow().updateview()
            switchboard.notify("view changed", self.gfxwindow())

        def dollyIn(self, menuitem, factor):
            self.gfxwindow().oofcanvas.dolly(factor)
            self._updateView()
        def dollyOut(self, menuitem, factor):
            self.gfxwindow().oofcanvas.dolly(1./factor)
            self._updateView()
        def dollyFill(self, menuitem):
            self.gfxwindow().oofcanvas.dolly_fill()
            self._updateView()
        def trackHoriz(self, menuitem, distance):
            # Get the normalized vector which is horizontal on the screen.
            (yp0, yp1, yp2) = self.gfxwindow().oofcanvas.get_camera_view_up()
            (zp0, zp1, zp2) = \
                self.gfxwindow().oofcanvas.get_camera_direction_of_projection()
            xp0 = -zp1*yp2 + yp1*zp2
            xp1 = -zp2*yp0 + yp2*zp0
            xp2 = -zp0*yp1 + yp0*zp1
            self.gfxwindow().oofcanvas.track(xp0*distance, xp1*distance,
                                             xp2*distance)
            self._updateView()
        def trackVert(self, menuitem, distance):
            (yp0, yp1, yp2) = self.gfxwindow().oofcanvas.get_camera_view_up()
            self.gfxwindow().oofcanvas.track(yp0*distance, yp1*distance, 
                                             yp2*distance)
            self._updateView()
        def recenter(self, menuitem):
            self.gfxwindow().oofcanvas.recenter()
            self._updateView()
            
        def roll(self, menuitem, angle):
            self.gfxwindow().oofcanvas.roll(angle)
            self._updateView()
        def azimuth(self, menuitem, angle):
            self.gfxwindow().oofcanvas.azimuth(angle)
            self._updateView()
        def elevation(self, menuitem, angle):
            self.gfxwindow().oofcanvas.elevation(angle)
            self._updateView()
        def yaw(self, menuitem, angle):
            self.gfxwindow().oofcanvas.yaw(angle)
            self._updateView()
        def pitch(self, menuitem, angle):
            self.gfxwindow().oofcanvas.pitch(angle)
            self._updateView()

        def zoomIn(self, menuitem, factor):
            self.gfxwindow().oofcanvas.zoom(factor)
            self._updateView()
        def zoomOut(self, menuitem, factor):
            self.gfxwindow().oofcanvas.zoom(1./factor)
            self._updateView()
        def zoomFill(self, menuitem):
            self.gfxwindow().oofcanvas.zoom_fill()
            self._updateView()

        def _clipPlanesChanged(self, viewobj, viewname=None):
            # The "true" arg tells set_view to set the clip planes.
            mainthread.runBlock(self.gfxwindow().oofcanvas.set_view,
                                (viewobj, True))
            self.gfxwindow().updateview()
            switchboard.notify("view changed", self.gfxwindow())
            switchboard.notify("clip planes changed", self.gfxwindow())

        def newClipCB(self, menuitem, normal, offset):
            self.gfxwindow().acquireGfxLock()
            try:
                plane = clip.ClippingPlane(normal.cdirection, offset)
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                viewobj.addClipPlane(plane)
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()
        def editClipCB(self, menuitem, plane, normal, offset):
            self.gfxwindow().acquireGfxLock()
            try:
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                newplane = clip.ClippingPlane(normal.cdirection, offset)
                viewobj.replaceClipPlane(plane, newplane)
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()
        def delClipCB(self, menuitem, plane):
            self.gfxwindow().acquireGfxLock()
            try:
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                viewobj.removeClipPlane(plane)
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()
        def clipDisableCB(self, menuitem, plane):
            self.gfxwindow().acquireGfxLock()
            try:
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                viewobj.disableClipPlane(plane)
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()
        def clipEnableCB(self, menuitem, plane):
            self.gfxwindow().acquireGfxLock()
            try:
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                viewobj.enableClipPlane(plane)
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()
        def clipFlipCB(self, menuitem, plane):
            self.gfxwindow().acquireGfxLock()
            try:
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                viewobj.flipClipPlane(plane)
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()
        def clipUnflipCB(self, menuitem, plane):
            self.gfxwindow().acquireGfxLock()
            try:
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                viewobj.unflipClipPlane(plane)
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()
        def clipInvertOnCB(self, menuitem):
            self.gfxwindow().acquireGfxLock()
            try:
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                viewobj.invertClipOn()
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()
        def clipInvertOffCB(self, menuitem):
            self.gfxwindow().acquireGfxLock()
            try:
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                viewobj.invertClipOff()
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()

        def clipSuppressOnCB(self, menuitem):
            self.gfxwindow().acquireGfxLock()
            try:
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                viewobj.suppressClipOn()
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()
        def clipSuppressOffCB(self, menuitem):
            self.gfxwindow().acquireGfxLock()
            try:
                viewobj = mainthread.runBlock(
                    self.gfxwindow().oofcanvas.get_view)
                viewobj.suppressClipOff()
                self._clipPlanesChanged(viewobj)
            finally:
                self.gfxwindow().releaseGfxLock()

        def saveView(self, menuitem, name):
            self.gfxwindow().acquireGfxLock()
            try:
                view = UserDefinedView(
                    mainthread.runBlock(self.gfxwindow().oofcanvas.get_view))
                storeView(name, view)
                switchboard.notify("new view", name)
                switchboard.notify("view changed", self.gfxwindow())
            finally:
                self.gfxwindow().releaseGfxLock()
        def restoreView(self, menuitem, view):
            # Restore_View is invoked by the Next and Prev buttons in
            # the viewer toolbox. 
            self.gfxwindow().acquireGfxLock()
            try:
                # The "False" arg tells set_view not to set the clip
                # planes.
                mainthread.runBlock(self.gfxwindow().oofcanvas.set_view, 
                                    (view, False))
                self.gfxwindow().updateview()
                switchboard.notify("view restored", self.gfxwindow())
                ## TODO OPT: restoring clip planes should be a separate
                ## operation
                # switchboard.notify("clip planes changed", self.gfxwindow())
            finally:
                self.gfxwindow().releaseGfxLock()
        def _restoreNamedView(self, menuitem, view):
            self.gfxwindow().acquireGfxLock()
            try:
                self.restoreNamedView(view)
            finally:
                self.gfxwindow().releaseGfxLock()
        def restoreNamedView(self, view):
            # This is not a menu callback, and doesn't acquire the
            # gfxlock, which should have already been acquired by the
            # calling function.
            newView = retrieveView(view, self.gfxwindow()).clone()
            oldView = mainthread.runBlock(self.gfxwindow().oofcanvas.get_view)
            nclip = oldView.nClipPlanes()
            for i in range(nclip):
                newView.addClipPlane(oldView.getClipPlane(i))
            mainthread.runBlock(self.gfxwindow().oofcanvas.set_view,
                                (newView, False))
            self._updateView()
        def setView(self, viewname): 
            # This is called by the GUI toolbox and the GUI toolbar to
            # invoke the menu command that restores the view.
            menuitem = self.menu.Restore_Named_View
            menuitem.callWithDefaults(view=viewname)

        def deleteView(self, menuitem, view):
            v = namedViews[view]
            if v.deletable:
                del namedViews[view]
                switchboard.notify("view deleted", view)
            else:
                raise ooferror.ErrUserError(
                    "Please don't delete the predefined Views.")

    

toolbox.registerToolboxClass(ViewerToolbox, ordering=0.0)
