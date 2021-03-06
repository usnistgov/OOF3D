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
from ooflib.common import debug
from ooflib.common import registeredclass
from ooflib.common.IO import parameter

class SelectionOperator(registeredclass.RegisteredClass):
    registry = []

class Select(SelectionOperator):
    def operate(self, selection, courier):
        selection.clearAndSelect(courier)

class AddSelection(SelectionOperator):
    def operate(self, selection, courier):
        selection.select(courier)

class Unselect(SelectionOperator):
    def operate(self, selection, courier):
        selection.unselect(courier)

class Toggle(SelectionOperator):
    def operate(self, selection, courier):
        selection.toggle(courier)

class Intersect(SelectionOperator):
    def operate(self, selection, courier):
        # selection.intersectionCourier returns a courier that
        # computes the intersection of courier's pixels and the
        # current selection.  It must copy the current selection,
        # because clearAndSelect will clear the selection before
        # using the courier.
        selection.clearAndSelect(selection.intersectionCourier(courier))

registeredclass.Registration(
    "Select",
    SelectionOperator,
    Select,
    ordering=0,
    tip="Select new objects after deselecting the old ones.")

registeredclass.Registration(
    'Add Selection',
    SelectionOperator,
    AddSelection,
    ordering=1,
    tip="Select new objects, leaving the old ones selected.")

registeredclass.Registration(
    "Unselect",
    SelectionOperator,
    Unselect,
    ordering=2,
    tip="Unselect only the given objects, leaving others selected.")

registeredclass.Registration(
    "Toggle",
    SelectionOperator,
    Toggle,
    ordering=3,
    tip="Unselect the given objects if they're currently selected,"
    " and select them if they're not.")

registeredclass.Registration(
    "Intersect",
    SelectionOperator,
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


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Many (but not all) selection methods will have a SelectionOperator
# argument that indicates how the new selection combines with the
# previous selection.  That argument will appear in the toolbox GUI
# for the selection method.  In many cases, however, its value should
# be set by modifier keys (shift, ctrl, etc) and not by the toolbox
# widget for the parameter.  To make it less confusing (we hope) for
# the user, the parameter widget can be made passive so that it
# reflects the state of the modifier keys but does not affect them.
# Use this parameter class with passive=True in those cases.
# This is better than parameter.passive(parameter.RegisteredParameter(...))
# only because it also sets the tip string.

class SelectionOperatorParam(parameter.RegisteredParameter):
    def __init__(self, name, value=Select(), default=Select(),
                 tip=None, auxData={}, passive=False):
        if tip is None:
            if passive:
                tip = """\
How the new selection modifies the existing selection.
Use control and shift keys while clicking on the canvas
to change the value of this parameter."""
            else:
                tip="How the new selection modifies the existing selection."
        parameter.RegisteredParameter.__init__(
            self, name, SelectionOperator,
            value=value, default=default,
            tip=tip,
            auxData=auxData)
        if passive:
            self.set_data('passiveWidget', True)
