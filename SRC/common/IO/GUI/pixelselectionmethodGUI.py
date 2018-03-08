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

from ooflib.SWIG.common import config
from ooflib.common import debug
from ooflib.SWIG.common import ooferror
from ooflib.common import mainthread
from ooflib.common import pixelselectionmethod
from ooflib.common import subthread
from ooflib.common import thread_enable
from ooflib.common.IO import mousehandler
from ooflib.common.IO import voxelregionselectiondisplay
from ooflib.common.IO.GUI import pixelselectparamwidgets
from ooflib.common.IO.GUI import parameterwidgets
from ooflib.common.IO.GUI import regclassfactory
from ooflib.SWIG.common import lock
from ooflib.SWIG.common import switchboard
import gtk
import math

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Each SelectionMethodGUI should use this decorator. The argument(s)
# of the decorator are the SelectionMethods that the gui applies to.
# The decorator adds a "gui" member to the SelectionMethod's
# registration.

def selectionGUIfor(*_selectorClasses):
    def decorator(guicls):
        for cls in _selectorClasses:
            cls.registration.gui = guicls
        return guicls
    return decorator
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## TODO:  Update these comments.
# Subclasses of SelectionMethodGUI are in charge of managing what
# state a particular tool for selecting regions of pixels (or voxels)
# is in, and they also act as MouseHandlers for that particular tool.
# They should have a class-level 'selectionMethod' datum that
# indicates which PixelSelectionMethod they apply to.

# Some selection methods/tools (e.g. that to select a rectangular
# prism of voxels) require the user to perform multiple steps
# (e.g. create a new box-shaped region, edit that region using the
# mouse, finish editing the region and finally select all voxels
# within that region). Therefore, we must somehow keep track of which
# step the user is currently performing. It makes sense to have this
# tracking done by an object that is registered with (but separate
# from) the PixelSelectToolboxGUI that the user is working with, and
# to have this object's class associated with the selection
# method/tool whose GUI it is managing.  So, we let this object be an
# instance of a certain SelectionMethodGUI subclass, and we associate
# each subclass of SelectionMethodGUI
# (e.g. RectangularPrismSelectorGUI) with a subclass of
# SelectionMethod (e.g. RectangularPrismSelector) using the dictionary
# selmethGUIdict.

class SelectionMethodGUI(mousehandler.MouseHandler):
    # Base class for RectangularPrismSelectorGUI, SphereSelectorGUI,
    # etc.
    def __init__(self, toolbox):
        self.toolbox = toolbox
    def gfxwindow(self):
        return self.toolbox.gfxwindow()
    
    def __call__(self, params, scope=None, name=None, verbose=False):
        # This function may be redefined for derived classes.  It
        # should return a ParameterWidget of some sort.  It must be
        # called __call__ because it's called by
        # RegisteredClassFactory.makeWidget, which thinks it's
        # instantiating an object of a class.  The default version
        # here does what RegisteredClassFactory does if it doesn't a
        # specialized widget isn't defined.
        return parameterwidgets.ParameterTable(params, scope, name, verbose)
    
    # def cancel(self):
    #     # This function should be redefined for derived classes. It
    #     # should be used to notify a SelectionMethodGUI to cancel any
    #     # subthreads it started, and should be called when the
    #     # SelectionMethodGUI's toolboxGUI is being closed.
    #     pass

    def mouseHandler(self):
        return mousehandler.NullMouseHandler()

    def close(self):
        # close() is called whent the toolbox is closing.  It should
        # do any necessary cleanup.  It can assume that the
        # mousehandler (if any) has already been stopped.
        pass

    # activate() and deactivate() are called when the toolbox is
    # activated and deactivated.
    def activate(self):
        pass
    def deactivate(self):
        pass

    def sensitize(self):
        pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# TODO: Have the done function in RectangularPrismSelectorGUI call the
# menu item to select a rectangular-prism-shaped region of
# voxels. Right now, we just have a little click-and-drag-able curio
# that does nothing useful.

# TODO: Allow the user to adjust the box by selecting edges and
# corners too (see TODOs in common/IO/canvaslayer.C for some of the
# BoxWidgetLayer functions).

@selectionGUIfor(pixelselectionmethod.RectangularPrismSelector)
class RectangularPrismSelectorGUI(SelectionMethodGUI):
    # targetName = pixelselectionmethod.RectangularPrismSelector
    def __init__(self, toolbox):
        SelectionMethodGUI.__init__(self, toolbox)
        self.widget = None

        # ID of the vtk cell currently being edited.
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
        self._editing = True
        self.layer.start()
        self.sensitize()
        self.gfxwindow().oofcanvas.render()

    def done(self):
        self._editing = False
        self.layer.stop()
        self.sensitize()
        ## TODO: Make the selection!
        self.gfxwindow().oofcanvas.render()
        
    def cancel(self):
        self._editing = False
        self.layer.stop()
        self.sensitize()
        self.gfxwindow().oofcanvas.render()

    def reset(self):
        self.layer.reset()
        self.gfxwindow().oofcanvas.render()

    def activate(self):
        self.layer.activate()
    def deactivate(self):
        self.layer.deactivate()
        
    def up(self, x, y, button, shift, ctrl):
        # Commands which need to be run when an 'up' event is being
        # processed.
        self.last_x = None
        self.last_y = None
        self.cellID = None
        return
        
    def down(self, x, y, button, shift, ctrl):
        # Commands which need to be run when a 'down' event is being
        # processed.
        viewobj = mainthread.runBlock(self.gfxwindow().oofcanvas.get_view)
        point = mainthread.runBlock(self.gfxwindow().oofcanvas.display2Physical,
                                    (viewobj, x, y))
        ## TODO: We know the layer, so use a (new) findClickedCell
        ## method that takes a layer arg instead of a layer class arg.
        (self.cellID, click_pos, self.layer) = \
               self.gfxwindow().findClickedCellIDByLayerClass_nolock(
                   voxelregionselectiondisplay.VoxelRegionSelectionDisplay,
                   point, viewobj)
        self.last_x = x;
        self.last_y = y;

    def move(self, x, y, button, shift, ctrl):
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

   
                                      
    
