# -*- python -*-
# $RCSfile: pixelselectionmethodGUI.py,v $
# $Revision: 1.1.2.1 $
# $Author: rdw1 $
# $Date: 2015/08/07 12:55:59 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# See NOTES/selection_machinery.txt

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.common import debug
from ooflib.common import mainthread
from ooflib.common import pixelselectionmethod
from ooflib.common import selectionoperators
from ooflib.common.IO import mousehandler
from ooflib.common.IO import voxelregionselectiondisplay
from ooflib.common.IO.GUI import genericselectGUI
from ooflib.common.IO.GUI import pixelselectparamwidgets
import gtk
import math

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#


class SingleClickVoxelSelectionMethodGUI(genericselectGUI.SelectionMethodGUI):
    def mouseHandler(self):
        return mousehandler.SingleClickMouseHandler(self)
    def getVoxel(self, x, y):
        # getVoxel returns a tuple containing the Who object that was
        # clicked on and the 3D position of the click.
        viewobj = mainthread.runBlock(self.gfxwindow().oofcanvas.get_view)
        point = mainthread.runBlock(self.gfxwindow().oofcanvas.display2Physical,
                                    (viewobj, x, y))

        # Get all layers displaying the target objects, from bottom to
        # top in the window's layer ordering.
        layers = self.gfxwindow().allWhoClassLayers(
            *self.methodRegistration.whoclasses)
        # Find the position of the click on the topmost object.  This
        # is actually the center of the topmost vtk cell that was
        # clicked, which may not be the actual click point, but is
        # what we need to know to identify the clicked voxel.
        who, point = self.gfxwindow().findClickedCellCenterMulti(
            layers, point, viewobj)
        if who is not None:
            ms = who.getMicrostructure()
            voxel = ms.pixelFromPoint(point)
            return (who, voxel)
        return (None, None)

    def down(self, x, y, buttons):
        who, voxel = self.getVoxel(x, y)
        if voxel is not None:
            self.toolbox.setParamValues(
                point=voxel,
                operator=selectionoperators.getSelectionOperator(buttons))

    def modkeys(self, buttons):
        self.toolbox.setParamValues(
            operator=selectionoperators.getSelectionOperator(buttons))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

@genericselectGUI.selectionGUIfor(pixelselectionmethod.PointSelector)
class PointSelectorGUI(SingleClickVoxelSelectionMethodGUI):
    def up(self, x, y, buttons):
        who, voxel = self.getVoxel(x, y)
        if who is not None:
            self.toolbox.setParamValues(point=voxel)
            operator = selectionoperators.getSelectionOperator(buttons)
            self.toolbox.invokeMenuItem(
                who,
                pixelselectionmethod.PointSelector(voxel, operator))

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# TODO: Allow the user to adjust the box by selecting edges and
# corners too (see TODOs in common/IO/canvaslayer.C for some of the
# BoxWidgetLayer functions).

from ooflib.common import selectionshape

@genericselectGUI.selectionGUIfor(pixelselectionmethod.RectangularPrismSelector)
class RectangularPrismSelectorGUI(genericselectGUI.SelectionMethodGUI):
    def __init__(self, toolbox):
        # toolbox is a PixelSelectToolboxGUI object.
        genericselectGUI.SelectionMethodGUI.__init__(self, toolbox)
        self.widget = None      # gtk widget in the toolbox

        # id of the vtk cell currently being edited.
        self.cellID = None

        # Previous position, in display coordinates, of the mouse.
        self.last_x = None
        self.last_y = None

        # The VoxelRegionSelectionDisplay canvas layer that's being
        # updated.
        self.layer = toolbox.gfxwindow().getLayerByClass(
            voxelregionselectiondisplay.VoxelRegionSelectionDisplay)
        assert self.layer is not None
        
        # This flag will be True whenever the user is currently using
        # the mouse on the canvas to edit the dimensions of the box
        # enclosing the voxels to be selected. The flag will be set to
        # False again once the user has pressed the 'Done' button.
        self._editing = False

    def __call__(self, params, scope=None, name=None, verbose=False):
        # This function returns the VoxelRegionSelectWidget that
        # creates buttons and other gui elements in the toolbox.
        self.widget = pixelselectparamwidgets.VoxelRegionSelectWidget(
            self, params, scope=scope, name=name, verbose=verbose)
        return self.widget

    def sensitize(self):
        if self.widget:
            self.widget.sensitize()

    def editing(self):
        return self._editing

    def mouseHandler(self):
        return mousehandler.KangarooMouseHandler(self, ("up", "move", "down"))

    def start(self):
        # Called by VoxelRegionSelectWidget.startCB, in response to
        # the 'Start' button.
        self._editing = True
        self.layer.start()
        self.sensitize()
        self.gfxwindow().oofcanvas.render()
        self.voxelbox = self.layer.get_box()
        self.setPointWidgets()

    def done(self):
        # Call the menu item that actually makes the selection.
        self._editing = False
        self.layer.stop()
        self.sensitize()
        ## TODO: Converting from CRectangularPrism to Coords here is
        ## clumsy. The Coords are converted back to a
        ## CRectangularPrism when the BoxSelection courier is created
        ## in RectangularPrismSelectorGUI.select in
        ## pixelselectionmethod.py.  The only reason for converting
        ## here is that we don't have a gtk widget for
        ## CRectangularPrism parameters.

        ## TODO: Creating the RectangularPrismSelector here without
        ## using the Registration is odd.  The actual parameters in
        ## the Registration are never used.  This could use
        ## toolbox.getParamValues() or just instantiate the object
        ## from the Registration.

        operator = self.toolbox.getParamValues('operator')
        
        self.toolbox.invokeMenuItem(
            self.toolbox.getSelectionSource(),
            pixelselectionmethod.RectangularPrismSelector(
                self.voxelbox.lowerleftback(),
                self.voxelbox.upperrightfront(),
                operator))
        # There's no need to redraw, since the menu item will do it.
        # self.gfxwindow().oofcanvas.render()
        
    def cancel(self):
        if self._editing:
            self._editing = False
            self.layer.stop()
            self.sensitize()
            self.gfxwindow().oofcanvas.render()

    def reset(self):
        if self._editing:
            self.layer.reset()
            self.gfxwindow().oofcanvas.render()
            self.voxelbox = self.layer.get_box()
            self.setPointWidgets()

    # install and uninstall are called by the toolbox when switching
    # between selection methods in this toolbox.
    def install(self):
        self.activate()
    def uninstall(self):
        self.cancel()           # Cancel any editing in progress.
        self.deactivate()

    # activate and deactivate are called when switching between
    # toolboxes.  Switching to a different toolbox doesn't halt the
    # editing session in this toolbox, but it temporarily dims the vtk
    # widget.
    def activate(self):
        self.layer.activate()
    def deactivate(self):
        self.layer.deactivate()

    def setPointWidgets(self):
        # Copy coordinates from self.voxelbox (the vtk box in the
        # canvas) to the parameters displayed in the gtk toolbox.
        self.toolbox.setParamValues(corner0=self.voxelbox.lowerleftback(),
                                    corner1=self.voxelbox.upperrightfront())
        
    def up(self, x, y, buttons):
        # An 'up' event is being processed.
        if not self._editing:
            return
        self.last_x = None
        self.last_y = None
        self.cellID = None
        return
        
    def down(self, x, y, buttons):
        # A 'down' event is being processed.
        if not self._editing:
            return
        viewobj = mainthread.runBlock(self.gfxwindow().oofcanvas.get_view)
        point = mainthread.runBlock(self.gfxwindow().oofcanvas.display2Physical,
                                    (viewobj, x, y))
        # Get the clicked position on the box widget and the ID of the
        # clicked cell.
        ## TODO: We know the layer, so use a (new) findClickedCell
        ## method that takes a layer arg instead of a layer class arg.
        (self.cellID, click_pos, self.layer) = \
               self.gfxwindow().findClickedCellIDByLayerClass_nolock(
                   voxelregionselectiondisplay.VoxelRegionSelectionDisplay,
                   point, viewobj)
        self.last_x = x;
        self.last_y = y;
        self.voxelbox = self.layer.get_box()
        self.setPointWidgets()
        

    def move(self, x, y, buttons):
        if not self._editing:
            return
        viewobj = mainthread.runBlock(self.gfxwindow().oofcanvas.get_view)
        last_mouse_coords = mainthread.runBlock(
            self.gfxwindow().oofcanvas.display2Physical, (viewobj, self.last_x,
                                                        self.last_y))
        mouse_coords = mainthread.runBlock(
            self.gfxwindow().oofcanvas.display2Physical, (viewobj, x, y))
        diff = mouse_coords - last_mouse_coords
        diff_size = math.sqrt(diff ** 2)
        if diff_size == 0:
            return
        diff = diff / diff_size
        normal = self.layer.canvaslayer.get_cellNormal_Coord3D(self.cellID)
        if (normal is None):
            return
        center = self.layer.canvaslayer.get_cellCenter(self.cellID)
        camera_pos = mainthread.runBlock(
            self.gfxwindow().oofcanvas.get_camera_position_v2)
        dist = math.sqrt((camera_pos - center) ** 2)
        view_angle = mainthread.runBlock(
            self.gfxwindow().oofcanvas.get_camera_view_angle)
        canvas_size = mainthread.runBlock(self.gfxwindow().oofcanvas.get_size)
        offset = (diff.dot(normal) * dist * math.tan(math.radians(view_angle))
                  * math.sqrt((x - self.last_x) ** 2 +
                              (y - self.last_y) ** 2) / canvas_size[1])
        
        # Update the canvaslayer.
        self.layer.canvaslayer.offset_cell(self.cellID, offset)
        self.layer.canvaslayer.setModified()

        self.last_x = x;
        self.last_y = y;
        mainthread.runBlock(self.gfxwindow().oofcanvas.render)
        self.voxelbox = self.layer.get_box()
        self.setPointWidgets()
