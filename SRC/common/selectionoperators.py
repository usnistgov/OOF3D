# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Different ways that selections can be applied.

from ooflib.SWIG.common import config
from ooflib.common import registeredclass

## TODO: This file should work with generic selections, and not be
## specific to Pixel selections.
from ooflib.SWIG.common import pixelselectioncourier

class PixelSelectionOperator(registeredclass.RegisteredClass):
    registry = []

class Select(PixelSelectionOperator):
    def operate(self, selection, courier):
        selection.clearAndSelect(courier)

class AddSelection(PixelSelectionOperator):
    def operate(self, selection, courier):
        selection.select(courier)

class Unselect(PixelSelectionOperator):
    def operate(self, selection, courier):
        selection.unselect(courier)

class Toggle(PixelSelectionOperator):
    def operate(self, selection, courier):
        selection.toggle(courier)

class Intersect(PixelSelectionOperator):
    def operate(self, selection, courier):
        # The selection needs to be cloned before calling
        # clearAndSelect, or else it will be empty by the time the
        # intersection is actually computed.  The clone has to be
        # stored in a variable here, so that it won't be garbage
        # collected until the calculation is complete.
        selgrp = selection.getSelectionAsGroup().clone()
        selection.clearAndSelect(
            pixelselectioncourier.IntersectSelection(
                courier.getMicrostructure(), selgrp, courier))

registeredclass.Registration(
    "Select",
    PixelSelectionOperator,
    Select,
    ordering=0,
    tip="Select new objects after deselecting the old ones.")

registeredclass.Registration(
    'Add Selection',
    PixelSelectionOperator,
    AddSelection,
    ordering=1,
    tip="Select new objects, leaving the old ones selected.")

registeredclass.Registration(
    "Unselect",
    PixelSelectionOperator,
    Unselect,
    ordering=2,
    tip="Unselect only the given objects, leaving others selected.")

registeredclass.Registration(
    "Toggle",
    PixelSelectionOperator,
    Toggle,
    ordering=3,
    tip="Unselect the given objects if they're currently selected,"
    " and select them if they're not.")

registeredclass.Registration(
    "Intersect",
    PixelSelectionOperator,
    Intersect,
    ordering=3,
    tip="Unselect all objects that are not in the given set.")


## TODO: Make the interpretation of the modifier keys settable by the
## user?

def getSelectionOperator(buttons):
    if buttons.shift:
        if buttons.ctrl:
            return Unselect()   # shift and ctrl
        return AddSelection()   # shift only
    if buttons.ctrl:
        return Toggle()         # ctrl only
    return Select()             # no modifier keys

