# -*- python -*-


# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# There is one set of selected pixels for each Microstructure.  It's
# maintained as a list of iPoints.  It's created by
# CMicrostructure.__init__, as modified in cmicrostructure.spy.

# PixelSelections have to know their Microstructures at the C++ level
# so that they can find their active areas.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import switchboard
from ooflib.common import debug
from ooflib.common import genericselection
from ooflib.common import registeredclass
from ooflib.common.IO import oofmenu
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville
from ooflib.SWIG.common import pixelselectioncourier

#####################################

class PixelSelectionContext(whoville.WhoDoUndo):
    def getMicrostructure(self):
        return self.getObject().getMicrostructure()
    def start(self):
        newselection = self.getObject().clone()
        self.pushModification(newselection)

    # These have an embedded active area check.
    def select(self, selectioncourier):
        self.getObject().select(selectioncourier)
    def unselect(self, selectioncourier):
        self.getObject().unselect(selectioncourier)
    def toggle(self, selectioncourier):
        self.getObject().toggle(selectioncourier)
    def selectSelected(self, selectioncourier):
        self.getObject().selectSelected(selectioncourier)
    def clearAndSelect(self, selectioncourier):
        self.getObject().clear()
        self.getObject().select(selectioncourier)
    def selectFromGroup(self, group):
        # Used when copying the pixel selection from one
        # Microstructure to another.  Does *not* check the active
        # area.
        self.getObject().setFromGroup(group)
    def clear(self):
        self.getObject().clear()
    def invert(self):
        self.getObject().invert()
    def getSelection(self):
        return self.getObject().members()
    def undo(self):
        self.undoModification()
    def redo(self):
        self.redoModification()
    def clearable(self):
        sz = self.size()
        if sz is not None:
            return sz != 0
        return 0
    def size(self):
        obj = self.getObject()
        if obj is not None:
            return len(obj)
        return 0
    def empty(self):
        obj = self.getObject()
        return obj is None or obj.empty()
    # def getBitmap(self):        # TODO OPT: Is this still needed?
    #     return self.getObject().getBitmap()
    def getPixelSet(self):
        obj = self.getObject()
        if obj is not None:
            return self.getObject().getPixelGroup()
    def getBounds(self):
        obj = self.getObject()
        if obj is not None:
            return self.getObject().getBounds()

    def intersectionCourier(self, courier):
        # intersectionCourier is used by selectionoperators.Intersect,
        # which needs to fetch a different kind of IntersectSelection
        # courier when selecting different kinds of objects.  It
        # returns a courier that computes the intersection of the
        # given group with selection represented by the given courier.
        currentPxls = self.getPixelSet()
        return pixelselectioncourier.IntersectSelection(
            self.getMicrostructure(), currentPxls, courier)

##################
    
pixelselectionWhoClass = whoville.WhoDoUndoClass(
    'Pixel Selection',
    instanceClass=PixelSelectionContext,
    ordering=999,
    secret=0,
    proxyClasses=['<top microstructure>'])

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# RegisteredClasses and Registrations for voxel selection methods.

# There are two (poorly named) main classes of voxel selection methods.

# VoxelSelectionMethod is the registered class for mouse-based
# selection methods that appear in the Select Voxels toolbox in
# graphics windows.

# VoxelSelectionModifier is the registered class for the selection
# tools that appear in the RCF on the PixelPage.

# All selection operations other than Undo, Redo, Clear, and Invert
# are handled by a single menu item which takes a
# VoxelSelectionModifier or VoxelSelectionMethod arg as well as the
# name of the Microstructure or Image.  They should be registered with
# VoxelSelectionMethodRegistration or VoxelSelectionModRegistration.
# The subclasses need to have a "select" method that takes a "source"
# and a "selection" argument.  The value of "source" is the name of an
# Image or Microstructure.

class VoxelSelectionMethod(genericselection.GenericSelectionMethod):
    registry = []
    # Source is a Microstructure or Image.  Selection is the
    # Microstructure's PixelSelection object. Operator is a
    # PixelSelectionOperator, from selectionoperators.py.  Called from
    # pixelselectionmenu.select(), which is the callback for the menu
    # item OOF.VOxelSelection.Select.
    def select(self, source, selection, operator):
        raise ooferror.ErrPyProgrammingError(
            "'select' isn't defined for " + self.registration.name)
    def notify(self):
        pass

    
class VoxelSelectionMethodRegistration(registeredclass.Registration):
    def __init__(self, name, subclass, ordering, params=[], secret=0, **kwargs):
        registeredclass.Registration.__init__(
            self,
            name=name,
            registeredclass=VoxelSelectionMethod,
            subclass=subclass,
            ordering=ordering,
            params=params,
            secret=secret,
            **kwargs)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class VoxelSelectionModifier(registeredclass.RegisteredClass):
    registry = []
    def notify(self):
        self.getRegistration().notify(self)
    
class VoxelSelectionModRegistration(registeredclass.Registration):
    def __init__(self, name, subclass, ordering, params, secret=0, **kwargs):
        registeredclass.Registration.__init__(
            self,
            name=name,
            registeredclass=VoxelSelectionModifier,
            subclass=subclass,
            ordering=ordering,
            params=params,
            secret=secret,
            **kwargs)
        from ooflib.common.IO import pixelselectionmenu
        self.menuitem = pixelselectionmenu.selectmenu.Select
        
    def callMenuItem(self, microstructure, selectionModifier):
        # Called by PixelPage when the OK button is pressed
        self.menuitem.callWithDefaults(source=microstructure,
                                       method=selectionModifier)
    def notify(self, modifier):
        # This signal is caught by the pixel selection page and used
        # to update its Historian.
        switchboard.notify("voxel selection modifier applied", modifier)
