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
from ooflib.common import debug
from ooflib.common.IO import whoville
import types

# class PixelSelection(cpixelselection.CPixelSelection):
#     def __repr__(self):
#         return "PixelSelection(%s)" % len(self)
#     def getMicrostructure(self):
#         return self.getCMicrostructure()
#         # Find which Microstructure corresponds to this CMicrostructure.
#         #return common.microstructure.microStructures[cms.name()]

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
    def getSelectionAsGroup(self):
        return self.getObject().getPixelGroup()
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

##################
    
pixelselectionWhoClass = whoville.WhoDoUndoClass(
    'Pixel Selection',
    instanceClass=PixelSelectionContext,
    ordering=999,
    secret=0,
    proxyClasses=['<top microstructure>'])

