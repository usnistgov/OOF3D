# -*- python -*-
# $RCSfile: pixelselecttoolboxGUI.py,v $
# $Revision: 1.23.10.9 $
# $Author: langer $
# $Date: 2014/08/01 15:25:28 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Pixel selection tools.  See comments in common/pixelselectmethod.py.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO.GUI import rubberband3d as rubberband
from ooflib.common import debug
from ooflib.common import pixelselectionmethod
from ooflib.common import primitives
from ooflib.common.IO import pixelselectiontoolbox
from ooflib.common.IO.GUI import genericselectGUI
from ooflib.common.IO.GUI import regclassfactory


class PixelSelectionMethodFactory(regclassfactory.RegisteredClassFactory):
    def __init__(self, registry, obj=None, title=None,
                 callback=None, fill=0, expand=0, scope=None, name=None,
                 widgetdict={}, *args, **kwargs):
        self.current_who_class = None
        regclassfactory.RegisteredClassFactory.__init__(
            self, registry, obj=obj, title=title, callback=callback,
            fill=fill, expand=expand, scope=scope, name=name,
            widgetdict=widgetdict, *args, **kwargs)

    def set_whoclass_name(self, name):
        self.current_who_class = name

    def includeRegistration(self, registration):
        if self.current_who_class is None:
            return True
        return self.current_who_class in registration.whoclasses
        

class PixelSelectToolboxGUI(genericselectGUI.GenericSelectToolboxGUI):
    def __init__(self, pixelselecttoolbox, method):
        debug.mainthreadTest()
        if config.dimension() == 2:
            name = "Pixel Selection"
        elif config.dimension() == 3:
            name = "Voxel Selection"
        genericselectGUI.GenericSelectToolboxGUI.__init__(self,
                                                   name,
                                                   pixelselecttoolbox,
                                                   method)

        # Switchboard callbacks that should be performed even when the
        # toolbox isn't active go here.  Callbacks that are performed
        # only when the toolbox IS active are installed in activate().
        self.sbcallbacks.extend([
            switchboard.requestCallbackMain('new pixel selection',
                                            self.newSelection),
            switchboard.requestCallbackMain((self.gfxwindow(),
                                             'layers changed'),
                                            self.layerChangeCB)
            ])

    # In parent class, RCF is assigned to self.selectionMethodFactory
    def methodFactory(self):
        return PixelSelectionMethodFactory(
            self.method.registry, title="Method:", name="Method")
    
    def activate(self):
        if not self.active:
            genericselectGUI.GenericSelectToolboxGUI.activate(self)
            self.activecallbacks = [
                switchboard.requestCallbackMain('pixel selection changed',
                                                self.changedSelection)
            ]

    def deactivate(self):
        if self.active:
            genericselectGUI.GenericSelectToolboxGUI.deactivate(self)
            map(switchboard.removeCallback, self.activecallbacks)
            self.activecallbacks = []
            
    def getSource(self):
        return self.gfxwindow().topwho('Microstructure', 'Image')
    
    def finish_up(self, ptlist, view, shift, ctrl, selmeth):
        # copy parameters from widgets to the registration
        self.selectionMethodFactory.set_defaults()
        
        # Invoke the selection method by calling the corresponding
        # toolbox menu item. The arguments are the Registration
        # parameters, plus the list of Points, the view, and the
        # keyboard modifiers.  The view is needed to translate the
        # point in space to a point on the microstructure.  The
        # translation in general depends on what's being clicked on,
        # so it can't be done here.
        menuitem = getattr(self.toolbox.menu, selmeth.name())
        menuitem.callWithDefaults(source=self.getSourceName(),
                                  points=ptlist,
                                  view=view, 
                                  shift=shift, ctrl=ctrl)

    def undoCB(self, button):
        self.toolbox.menu.Undo(source=self.getSourceName())

    def redoCB(self, button):
        self.toolbox.menu.Redo(source=self.getSourceName())

    def clearCB(self, button):
        self.toolbox.menu.Clear(source=self.getSourceName())

    def invertCB(self, button):
        self.toolbox.menu.Invert(source=self.getSourceName())

    # This is all nice safe main-thread activity.
    def layerChangeCB(self):
        # This must be called even when the toolbox isn't active,
        # because the selection method factory has to list only those
        # methods that are valid for the current top layer.
        # set_whoclass_name has to be called whenever the top layer
        # changes, or it has to be called when the toolbox is
        # activated AND when the toolbox is active and the layer
        # changes.
        source = self.getSource()
        if source:
            self.selectionMethodFactory.set_whoclass_name(source.getClassName())
        else:
            self.selectionMethodFactory.set_whoclass_name(None)
        self.updateSelectionMethods()
        genericselectGUI.GenericSelectToolboxGUI.layerChangeCB(self)
        
        



#######################################

# Redefine PixelSelectToolbox.makeGUI() so that it returns a
# PixelSelectToolboxGUI object.

def _makeGUI(self):
    return PixelSelectToolboxGUI(self, self.method)

pixelselectiontoolbox.PixelSelectToolbox.makeGUI = _makeGUI


######################

## Assign rubberband creation functions to the
## PixelSelectionRegistrations.  Most assignments are to *instances*,
## and as such are not member functions.  The default assignment (no
## rubberband) is to the class, and so the function needs a 'self'
## argument.

def _NoRubberBand(self, reg):
    return rubberband.NoRubberBand()
pixelselectionmethod.PixelSelectionRegistration.getRubberBand = _NoRubberBand


if config.dimension() == 2:

    def _BrushSelectorRB(reg):
        style = reg.getParameter('style').value
        return rubberband.BrushRubberBand(style)

    pixelselectionmethod.brushSelectorRegistration.getRubberBand = _BrushSelectorRB


    def _RectangleSelectorRB(reg):
        return rubberband.RectangleRubberBand()

    pixelselectionmethod.rectangleSelectorRegistration.getRubberBand = \
                                                         _RectangleSelectorRB


    def _CircleSelectorRB(reg):
        return rubberband.CircleRubberBand()

    pixelselectionmethod.circleSelectorRegistration.getRubberBand = \
                                                                  _CircleSelectorRB


    def _EllipseSelectorRB(reg):
        return rubberband.EllipseRubberBand()

    pixelselectionmethod.ellipseSelectorRegistration.getRubberBand = \
                                                                 _EllipseSelectorRB
