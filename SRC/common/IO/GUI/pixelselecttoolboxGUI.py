# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.SWIG.common.IO.GUI import rubberband3d as rubberband
from ooflib.common import debug
from ooflib.common import pixelselectionmethod
from ooflib.common import primitives
from ooflib.common.IO import pixelselectiontoolbox
from ooflib.common.IO.GUI import genericselectGUI
from ooflib.common.IO.GUI import pixelselectionmethodGUI

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
    
class PixelSelectToolboxGUI(genericselectGUI.GenericSelectToolboxGUI):
    def __init__(self, pixelselecttoolbox, method):
        debug.mainthreadTest()

        genericselectGUI.GenericSelectToolboxGUI.__init__(self,
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

    def activate(self):
        if not self.active:
            super(PixelSelectToolboxGUI, self).activate()
            self.activecallbacks = [
                switchboard.requestCallbackMain('pixel selection changed',
                                                self.changedSelection)
            ]

    def deactivate(self):
        if self.active:
            map(switchboard.removeCallback, self.activecallbacks)
            super(PixelSelectToolboxGUI, self).deactivate()
            # genericselectGUI.GenericSelectToolboxGUI.deactivate(self)
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
