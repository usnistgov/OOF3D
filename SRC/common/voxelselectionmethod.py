# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# Various ways of specifying a set of voxels to select.  In OOF2 and
# earlier versions of OOF3D, each selection method had its own menu
# item, which was built automatically from the PixelSelectionMethod
# registration.  In OOF3D not all selection methods work well with the
# same set of arguments, so there's just one menu item, but it takes a
# VoxelSelectionMethod argument.  Each VoxelSelectionMethod class has
# a courier() method, which returns a C++ VoxelSelectionCourier object
# to efficiently pass the selection to the CMicro

from ooflib.SWIG.common import config
from ooflib.SWIG.common import ooferror
from ooflib.common import genericselectionop
from ooflib.SWIG.common import pixelselectioncourier
from ooflib.common import debug
from ooflib.common.IO import parameter
from ooflib.common import primitives

class VoxelSelectionOp(genericselectionop.SelectionOperator):
    target = 'Voxel'

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

@genericselectionop.register
class Point(VoxelSelectionOp):
    sources = ('Microstructure', 'Image')
    mouseBehavior = genericselectionop.MouseBehavior('SingleClick')
    tip = "Select a single voxel."
    # def select(self, ms, operator, point):
    #     operator.operate(ms.getSelectionContext(),
    #                      pixelselectioncourier.PointSelection(ms, point))

@genericselectionop.register
class Box(VoxelSelectionOp):
    sources = ('Microstructure', 'Image')
    mouseBehavior = genericselectionop.MouseBehavior('MultiDrag+')
    tip = "Select a rectangular box of voxels."

    # def select(self, ms, operator, point0, point1):
    #     operator.operate(ms.getSelectionContext(),
    #                      pixelselectioncourier.BoxSelection(ms, point0, point1))


## This should be in the image subdirectory
@genericselectionop.register
class Color(VoxelSelectionOp):
    sources = ("Image")
    mouseBehavior = genericselectionop.MouseBehavior('SingleClick')
    params = [colordiffparameter.ColorDifferenceParameter(
        'range', tip='Acceptable deviation from the reference color.')]
    tip = "Select similarly colored voxels."

@genericselectionop.register
class Burn(VoxelSelectionOp):
    sources = ("Image")
    mouseBehavior = genericselectionop.MouseBehavior('SingleClick')
    params = [ flammabilities ]
    tip = "Select contiguous similar voxels."
