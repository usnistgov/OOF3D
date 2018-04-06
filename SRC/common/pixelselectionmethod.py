# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 


# Each way of selecting pixels is described by a VoxelSelectionMethod
# subclass.  VoxelSelectionMethod is a RegisteredClass.  Instances of
# the subclasses are used as arguments to the Select command in the
# VoxelSelection menu, defined in pixelselectionmenu.py.  Selection
# methods that can use mouse input can have GUIs assigned to them.
# See SelectionMethodGUI and selectionGUIfor in genericselectGUI.py.

# See NOTES/selection_machinery.txt

from ooflib.SWIG.common import config
from ooflib.SWIG.common import geometry
from ooflib.SWIG.common import ooferror
from ooflib.SWIG.common import pixelselectioncourier
from ooflib.common import debug
from ooflib.common import pixelselection
from ooflib.common.IO import pixelselectionmenu
from ooflib.common.IO import pointparameter
from ooflib.common.IO import xmlmenudump

# Select a single pixel.  Although the select function is written to
# accept a list of points, it only receives one point because the
# registration only requests 'up'.

class PointSelector(pixelselection.VoxelSelectionMethod):
    def __init__(self, point, operator):
        self.point = point
        self.operator = operator
    def select(self, source, selection):
        ms = source.getMicrostructure()
        self.operator.operate(selection,
                         pixelselectioncourier.PointSelection(ms, self.point))

pixelselection.VoxelSelectionMethodRegistration(
    'Point',
    PointSelector,
    ordering=0.1,
    whoclasses=['Microstructure', 'Image'],
    params=[pointparameter.PointParameter('point'),
            pixelselectionmenu.passiveOperatorParam],
    tip="Select a single pixel.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/common/reg/pointselect.xml')
    )

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class RectangularPrismSelector(pixelselection.VoxelSelectionMethod):
    def __init__(self, corner0, corner1, operator):
        self.corner0 = corner0
        self.corner1 = corner1
        self.operator = operator
    def select(self, source, selection):
        ms = source.getMicrostructure()
        self.operator.operate(
            selection,
            pixelselectioncourier.BoxSelection(
                ms, geometry.CRectangularPrism(self.corner0, self.corner1)))

pixelselection.VoxelSelectionMethodRegistration(
    'Box',
    RectangularPrismSelector,
    ordering=0.2,
    params=[pointparameter.PointParameter('corner0'),
            pointparameter.PointParameter('corner1'),
            pixelselectionmenu.operatorParam],
    whoclasses=['Microstructure', 'Image'],
    tip="Click to select a box-shaped region."
    )


