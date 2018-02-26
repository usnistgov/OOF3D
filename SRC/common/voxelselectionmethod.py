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
from ooflib.SWIG.common import pixelselectioncourier
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common import genericselectionop
from ooflib.common import primitives
from ooflib.common.IO import colordiffparameter
from ooflib.common.IO import parameter

# See genericselectionop.py for a list of methods and class-level data
# that each VoxelSelectionOp subclass must provide.

class VoxelSelectionOp(object):
    target = 'Voxel'
    params = []                 # override in subclasses

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

@genericselectionop.register
class PointNEW(VoxelSelectionOp, mousehandler.SingleClickMouseHandler):
    sources = ('Microstructure', 'Image')
    mouseBehavior = genericselectionop.MouseBehavior('SingleClick')
    tip = "Select a single voxel."
    order = 0
    # def select(self, ms, operator, point):
    #     operator.operate(ms.getSelectionContext(),
    #                      pixelselectioncourier.PointSelection(ms, point))
    def doUp(self, x, y, button, ctrl, shift, gfxwindow):
        view = gfxwindow.getView()
        # TODO: How does this get the source and booleanoperator?
        # Should it call back to the GenericSelectToolbox?
        pt = gfxwindow.findClickedCellCenter(immidge, (x, y), view)
        menuitem(courier(pt), booleanoperator)

@genericselectionop.register
class BoxNEW(VoxelSelectionOp):
    sources = ('Microstructure', 'Image')
    mouseBehavior = genericselectionop.MouseBehavior('MultiDrag+')
    tip = "Select a rectangular box of voxels."
    order = 1
    # def select(self, ms, operator, point0, point1):
    #     operator.operate(ms.getSelectionContext(),
    #                      pixelselectioncourier.BoxSelection(ms, point0, point1))


## This should be in the image subdirectory
## importing burn is temporary
from ooflib.SWIG.image.burn import *
@genericselectionop.register
class ColorNEW(VoxelSelectionOp):
    sources = ("Image",)
    mouseBehavior = genericselectionop.MouseBehavior('SingleClick')
    params = [colordiffparameter.ColorDifferenceParameter(
        'range', tip='Acceptable deviation from the reference color.')]
    tip = "Select similarly colored voxels."
    order = 2
    
@genericselectionop.register
class BurnNEW(VoxelSelectionOp):
    sources = ("Image",)
    mouseBehavior = genericselectionop.MouseBehavior('SingleClick')
    params = [
        parameter.FloatRangeParameter(
            'local_flammability',
            range=(0, 1, 0.001), value=0.1,
            tip=("Maximum difference in neighboring pixel values across which"
                 " a burn will extend.")),
        parameter.FloatRangeParameter(
            'global_flammability',
            range=(0, 1, 0.001), value=0.2,
            tip=("Difference from initial pixel value beyond which a burn"
                 " will not spread.")),
        enum.EnumParameter(
            'color_space_norm', ColorNorm, value=L1,
            tip=("How to compute the difference between two colors"
                 " in RGB space.")),
        parameter.BooleanParameter(
            'next_nearest', value=0, tip="Burn next-nearest neighbors?")
    ]
    tip = "Select contiguous similar voxels."
    order = 3