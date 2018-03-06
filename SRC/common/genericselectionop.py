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
from ooflib.SWIG.common import ooferror
from ooflib.common import enum
from ooflib.common import registeredclass

# Classes for building UIs and GUIs for making selections.  Not to be
# confused with cpixelselection.* and cskeletonselectable.* which
# contain the classes that describe the selected sets themselves.

# Selection operation classes must be registered with the "register"
# decorator defined here, which stores them in a dict so that the GUI
# can find and list them.  They don't otherwise need to belong to a
# particular class hierarchy.  They must provide the following
# class-level data and methods:

## Data:
# * sources: a tuple of names of WhoClasses that the selection operates on,
#   eg ('Skeleton') or ('Microstructure', 'Image')
# * target: the name of the objects being selected, eg 'Voxels', 'Elements'
# * mouseBehavior: an instance of the MouseBehavior enum
# * tip: A help string to be displayed in the GUI
# * order: number determining ordering in GUI menus
# * name: The name to appear in the GUI.  If missing, the name of the
#   class is used.
# * params: Parameters to be displayed in the gui and passed to the menu item
#   (eg, brush width).
## Methods:
# * __init__(self)   takes no other args!
# * up(x, y, button, shift, ctrl)
# * down(x, y, button, shift, ctrl) if mouseBehavior is anything but SingleClick
# * move(x, y, button, shift, ctrl) if mouseBehavior is ClickAndDrag+
#   or MultiClick+
# (Mouse handling methods are optional if the selection operation has a
# widgetType that handles events.)


# _selectables[source][target] is a dict, keyed by operation name, of
# SelectionOperations applicable to the given source and target. 'source' and
# 'target' are strings.

_selectables = {}

def register(cls):
    try:
        nm = cls.name
    except AttributeError:
        nm = cls.__name__
        cls.name = nm
    try:
        for src in cls.sources:
            srcdict = _selectables.setdefault(src, {})
            srcdict.setdefault(cls.target, {})[nm] = cls
        switchboard.notify("new selection operation " + cls.target)
    except KeyError:
        raise ooferror.ErrPyProgrammingError(
            "Class " + cls.__name__ + " doesn't provide sources and target")
    return cls

def getSelectionOperations(source, target):
    try:
        return _selectables[source][target]
    except KeyError:
        return []

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# The MouseBehavior enum determines which mouse events are passed to
# the SelectionOperation subclass.  This is not necessarily the same
# as which events are actually used in the final menu command.  For
# instance, a GUI widget may use motion events to draw itself, but the
# menu command might only care about its final state.

class MouseBehavior(enum.EnumClass(
        ('SingleClick', 'A single down/up combo, using the location of the up'),
        ('ClickAndDrag', 'A down, move, up sequence, retaining only the down and up locations'),
        ('ClickAndDrag+', 'A down, move, up sequence, retaining all positions'),
        ('MultiClick', 'Multiple down/up combos, using the up locations'),
        ('MultiDrag', 'Multiple down, move, up combos, retaining the down and up'),
        ('MultiDrag+', 'Multiple down, move, up combos, retaining all positions')
)):
    tip = "How the mouse is used by a SelectionOperation"


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectionBoolean(registeredclass.RegisteredClass):
    registry = []
    
class SelectNEW(SelectionBoolean):
    def operate(self, selection, courier):
        selection.select(courier)

class SelectOnlyNEW(SelectionBoolean):
    def operate(self, selection, courier):
        selection.clearAndSelect(courier)

class UnselectNEW(SelectionBoolean):
    def operator(self, selection, courier):
        selection.unselect(courier)

class IntersectNEW(SelectionBoolean):
    def operator(self, selection, courier):
        selection.intersect(courier)
        # # The selection needs to be cloned before calling
        # # clearAndSelect, or else it will be empty by the time the
        # # intersection is actually computed.  The clone has to be
        # # stored in a variable here, so that it won't be garbage
        # # collected until the calculation is complete.
        # selgrp = selection.getSelectionAsGroup().clone()
        # selection.clearAndSelect(
        #     voxelselectioncourier.IntersectSelection(
        #         courier.getMicrostructure(), selgrp, courier))

registeredclass.Registration(
    'Select',
    SelectionBoolean,
    SelectNEW,
    ordering=0,
    tip="Select new objects, leaving the old ones selected.")

registeredclass.Registration(
    "Select Only",
    SelectionBoolean,
    SelectOnlyNEW,
    ordering=1,
    tip="Select new objects after deselecting the old ones.")

registeredclass.Registration(
    "Unselect",
    SelectionBoolean,
    UnselectNEW,
    ordering=2,
    tip="Unselect only the given objects, leaving others selected.")

registeredclass.Registration(
    "Intersect",
    SelectionBoolean,
    IntersectNEW,
    ordering=3,
    tip="Unselect all objects that are not in the given set.")
    
#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#
