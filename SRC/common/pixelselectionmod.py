# -*- python -*-
# $RCSfile: pixelselectionmod.py,v $
# $Revision: 1.29.18.11 $
# $Author: langer $
# $Date: 2014/09/16 00:42:25 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

# Pixel selection modification tools that *don't* depend on the image,
# and hence aren't in the image module.

from ooflib.SWIG.common import config
from ooflib.SWIG.common import pixelselectioncourier
from ooflib.SWIG.common import switchboard
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import primitives
from ooflib.common import registeredclass
from ooflib.common import selectionshape
from ooflib.common.IO import colordiffparameter
from ooflib.common.IO import parameter
from ooflib.common.IO import pixelgroupparam
from ooflib.common.IO import reporter
from ooflib.common.IO import whoville
from ooflib.common.IO import xmlmenudump
import ooflib.common.microstructure
import ooflib.common.units

# First, some basic methods: Clear, Undo, Redo
# These are no longer called from the generic toolbox, but they are
# still set as menu callbacks in the selectionmodmenu, in common/IO.

def clear(menuitem, microstructure):
    ms = ooflib.common.microstructure.microStructures[microstructure]
    selection = ms.getSelectionContext()
    selection.reserve()
    selection.begin_writing()
    try:
        selection.start()
        selection.clear()
    finally:
        selection.end_writing()
        selection.cancel_reservation()
    switchboard.notify('pixel selection changed', selection)
    switchboard.notify('redraw')

def undo(menuitem, microstructure):
    ms = ooflib.common.microstructure.microStructures[microstructure]
    selection = ms.getSelectionContext()
    selection.reserve()
    selection.begin_writing()
    try:
        selection.undo()
    finally:
        selection.end_writing()
        selection.cancel_reservation()
    switchboard.notify('pixel selection changed', selection)
    switchboard.notify('redraw')

def redo(menuitem, microstructure):
    ms = ooflib.common.microstructure.microStructures[microstructure]
    selection = ms.getSelectionContext()
    selection.reserve()
    selection.begin_writing()
    try:
        selection.redo()
    finally:
        selection.end_writing()
        selection.cancel_reservation()
    switchboard.notify('pixel selection changed', selection)
    switchboard.notify('redraw')


#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Selection methods derived from SelectionModifier are automatically
# put into the PixelSelection menu, via a switchboard call in their
# Registration's __init__.

class SelectionModifier(registeredclass.RegisteredClass):
    registry = []
    def __call__(self):
        pass

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# OOFMenu callback, installed automatically for each SelectionModifier
# class by the switchboard callback invoked when the class is
# registered.

def doSelectionMod(menuitem, microstructure, **params):
    registration = menuitem.data
    # create the SelectionModifier
    selectionModifier = registration(**params)
    # apply the SelectionModifier
    ms = ooflib.common.microstructure.microStructures[microstructure].getObject()
    selection = ms.pixelselection
    selection.reserve()
    selection.begin_writing()
    try:
        selectionModifier(ms, selection)
    finally:
        selection.end_writing()
        selection.cancel_reservation()
    # Switchboard signals:

    # "pixel selection changed" is caught by GUI components that
    # display the number of selected pixels, or the selected pixels
    # themselves, or contain widgets whose sensitivity depends on the
    # selection state.
    switchboard.notify('pixel selection changed', selection)
    # "modified pixel selection" indicates that a pixel selection
    # modifier has been applied.  It's caught by the Pixel Page to
    # update its historian.
    switchboard.notify('modified pixel selection', selectionModifier)
    # "new pixel selection" is similar to "modified pixel selection",
    # except that it's used by the pixel selection toolbox.
    ## TODO OPT: Do we really need both "pixel selection changed" and
    ## "modified pixel selection"?
    switchboard.notify('new pixel selection', None, None)

    switchboard.notify('redraw')

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Invert(SelectionModifier):
    def __call__(self, ms, selection):
        selection.start()
        selection.invert()

registeredclass.Registration(
    'Invert',
    SelectionModifier,
    Invert,
    ordering=0.0,
    tip="Select all unselected pixels and unselect all selected pixels.",
    discussion="""<para>
    Selected pixels will be unselected and unselelcted ones will be
    selected.</para>""")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

# Different ways that groups and shapes can be used when modifying
# selections.

## TODO 3.1: Can these be used in Skeleton selection operations as well?

class PixelSelectionOperator(registeredclass.RegisteredClass):
    registry = []

class Select(PixelSelectionOperator):
    def operate(self, selection, courier):
        selection.select(courier)

class SelectOnly(PixelSelectionOperator):
    def operate(self, selection, courier):
        selection.clearAndSelect(courier)

class Unselect(PixelSelectionOperator):
    def operate(self, selection, courier):
        selection.unselect(courier)

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
    'Select',
    PixelSelectionOperator,
    Select,
    ordering=0,
    tip="Select new objects, leaving the old ones selected.")

registeredclass.Registration(
    "Select Only",
    PixelSelectionOperator,
    SelectOnly,
    ordering=1,
    tip="Select new objects after deselecting the old ones.")

registeredclass.Registration(
    "Unselect",
    PixelSelectionOperator,
    Unselect,
    ordering=2,
    tip="Unselect only the given objects, leaving others selected.")

registeredclass.Registration(
    "Intersect",
    PixelSelectionOperator,
    Intersect,
    ordering=3,
    tip="Unselect all objects that are not in the given set.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class GroupSelector(SelectionModifier):
    def __init__(self, group, operator):
        self.group = group
        self.operator = operator
    def __call__(self, ms, selection):
        group = ms.findGroup(self.group)
        if group is not None:
            selection.start()
            self.operator.operate(
                selection, pixelselectioncourier.GroupSelection(ms, group))

registeredclass.Registration(
    'Group',
    SelectionModifier,
    GroupSelector,
    ordering=1,
    params=[
        pixelgroupparam.PixelGroupParameter('group',
                                            tip='Pixel group to work with.'),
        parameter.RegisteredParameter(
            'operator', PixelSelectionOperator,
            tip="How to use the group to modify the current selection.")],
    tip="Modify the current selection via boolean operations"
    " with the pixels in a pixel group.")

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

## Geometrical selection.  These will have GUI counterparts
## when we figure out how to click and drag on the 3D canvas.

# The selection methods operate upon sets of pixels defined by shapes
# from the SelectionShape class.  The SelectionShape subclasses don't
# actually have methods that extract the selected voxels because the
# scope would be wrong -- they're really just containers for the shape
# parameters, and they're used for things other than voxels.  However,
# we *do* want to use the SelectionShape classes themselves, and not
# derive VoxelSelectionShape classes from them, because it makes sense
# to use the same shape classes when selecting other sorts of objects.
# So here we create a dict that maps the SelectionShape classes to
# functions that return the appropriate courier objects.

# These couriers are used in activeareamod.py as well.

couriers = {}

def _box_courier(shape, ms):
    return pixelselectioncourier.BoxSelection(
        ms, shape.point0, shape.point1)
couriers[selectionshape.BoxSelectionShape] = _box_courier

def _circ_courier(shape, ms):
    return pixelselectioncourier.CircleSelection(ms, shape.center, shape.radius)
couriers[selectionshape.CircleSelectionShape] = _circ_courier

def _elps_courier(shape, ms):
    return pixelselectioncourier.EllipseSelection(
        ms, shape.point0, shape.point1)
couriers[selectionshape.EllipseSelectionShape] = _elps_courier

#=--=##=--=##=--=##=--=##=--=#

class RegionSelector(SelectionModifier):
    def __init__(self, shape, units, operator):
        self.shape = shape
        self.units = units
        self.operator = operator
    def __call__(self, ms, selection):
        selection.start()
        scaled = self.units.scale(ms, self.shape)
        courier = couriers[self.shape.__class__](scaled, ms)
        self.operator.operate(selection, courier)

registeredclass.Registration(
    "Region",
    SelectionModifier,
    RegionSelector,
    ordering=1.5,
    params=[
        parameter.RegisteredParameter(
            'shape', selectionshape.SelectionShape,
            tip='The shape of the region to select.'),
        parameter.RegisteredParameter(
            'units', ooflib.common.units.UnitsRC,
            value=ooflib.common.units.PhysicalUnits(),
            tip="The units for the shape's length parameters."),
        parameter.RegisteredParameter(
            'operator', PixelSelectionOperator,
            tip="How to use the region to modify the current selection.")
        ],
    tip="Modify the current selection via boolean operations using the pixels"
    " within a given geometrically defined region."
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Despeckle(SelectionModifier):
    def __init__(self, neighbors):
        self.neighbors = neighbors
    def __call__(self, ms, selection):
        selection.start()
        selection.select(pixelselectioncourier.DespeckleSelection(
            ms, selection.getSelectionAsGroup(), self.neighbors))
        
class Elkcepsed(SelectionModifier):
    def __init__(self, neighbors):
        self.neighbors = neighbors
    def __call__(self, ms, selection):
        selection.start()
        selection.unselect(pixelselectioncourier.ElkcepsedSelection(
            ms, selection.getSelectionAsGroup(), self.neighbors))

# The allowed ranges for the parameters are determined by geometry.
# Settings outside of the allowed ranges either select all pixels or
# no pixels and aren't useful.
if config.dimension() == 2:
    despeckleRange = (4, 8)
    despeckleDefault = 8
    elkcepsedRange = (1, 4)
    elkcepsedDefault = 3
else:
    despeckleRange = (10, 26)
    despeckleDefault = 15
    elkcepsedRange = (1, 13)
    elkcepsedDefault = 9

registeredclass.Registration(
    'Despeckle',
    SelectionModifier,
    Despeckle,
    ordering=2.0,
    params=[parameter.IntRangeParameter(
            'neighbors', despeckleRange, despeckleDefault,
            tip="Select pixels with at least this many selected neighbors")
    ],
    tip="Recursively select all pixels with a minimum number of selected neighbors. This fills in small holes in the selection.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/despeckle.xml')
    )

registeredclass.Registration(
    'Elkcepsed',
    SelectionModifier,
    Elkcepsed,
    ordering=2.1,
    params=[parameter.IntRangeParameter(
            'neighbors', elkcepsedRange, elkcepsedDefault,
       tip="Deselect pixels with fewer than this many selected neighbors.")
    ],
    tip="Recursively deselect all pixels with fewer than a minimum number of selected neighbors.  This has the effect of removing small islands and peninsulas, and is the opposite of 'Despeckle'.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/elkcepsed.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class Expand(SelectionModifier):
    def __init__(self, radius):
        self.radius = radius
    def __call__(self, ms, selection):
        selection.start()
        selection.select(pixelselectioncourier.ExpandSelection(
            ms, selection.getSelectionAsGroup(), self.radius))

class Shrink(SelectionModifier):
    def __init__(self, radius):
        self.radius = radius
    def __call__(self, ms, selection):
        selection.start()
        selection.unselect(pixelselectioncourier.ShrinkSelection(
            ms, selection.getSelectionAsGroup(), self.radius))

## TODO 3.1: Allow radius to be set in either physical or pixel units
## by adding a "units" parameter.

registeredclass.Registration(
    'Expand',
    SelectionModifier,
    Expand,
    ordering=3.0,
    params=[
        parameter.FloatParameter(
            'radius', 1.0,
            tip='Select pixels within this distance of other selected pixels.'),
    ],
    tip="Select all pixels within a given distance of the current selection.",
    discussion=xmlmenudump.loadFile("DISCUSSIONS/common/menu/expand_pixsel.xml")
    )

registeredclass.Registration(
    'Shrink',
    SelectionModifier,
    Shrink,
    ordering=3.1,
    params=[
        parameter.FloatParameter(
            'radius', 1.0,
            tip='Deselect pixels within this distance.')
    ],
    tip="Deselect all pixels within a given distance of the boundaries of the current selection.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/shrink_pixsel.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class CopyPixelSelection(SelectionModifier):
    def __init__(self, source):
        self.source = source
    def __call__(self, ms, selection):
        selection.start()
        sourceMS = ooflib.common.microstructure.microStructures[self.source]
        selection.selectFromGroup(
            sourceMS.getObject().pixelselection.getSelectionAsGroup())

registeredclass.Registration(
    'Copy',
    SelectionModifier,
    CopyPixelSelection,
    ordering=4.0,
    params=[
    whoville.WhoParameter('source', ooflib.common.microstructure.microStructures,
                          tip="Copy the current selection from this Microstructure.")],
    tip="Copy the current selection from another Microstructure.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/menu/copy_pixsel.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

