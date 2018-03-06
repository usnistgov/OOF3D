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
from ooflib.common.IO import mousehandler
from ooflib.common.IO import parameter
from ooflib.common.IO import voxelregionselectiondisplay

# See genericselectionop.py for a list of methods and class-level data
# that each VoxelSelectionOp subclass must provide.

class VoxelSelectionOp(registeredclass.RegisteredClass):
    registry = []

class VoxelSelectionRegistration(registeredclass.Registration):
    def __init__(self, name, subclass, ordering, params=[], secret=0, **kwargs):
        registeredclass.Registration(self,
                                     name=name,
                                     registeredclass=VoxelSelectionOp,
                                     subclass=subclass,
                                     ordering=ordering,
                                     params=params,
                                     secret=secret,
                                     widgetType=None,
                                     **kwargs)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectPoint(VoxelSelectionOp):
    def up(self, x, y, button, ctrl, shift, gfxwindow):
        pass

VoxelSelectionRegistration(
    'PointNew',
    SelectPoint,
    ordering=0,
    mouseBehavior=genericselectionop.MouseBehavior('SingleClick'),
    sources=('Microstructure', 'Image'),
    tip='Select a single voxel.')
    


# class VoxelSelectionOp(object):
#     target = 'Voxel'
#     params = []       # override in subclasses
#     widgetType = None # subclasses can set this to a DisplayMethod subclass
#     # Subclasses that don't set widgetType must redefine at least one
#     # of up(), down(), or move().
#     def up(self, *args):
#         debug.fmsg("VoxelSelectionOp base class")
#     def down(self, *args):
#         debug.fmsg("VoxelSelectionOp base class")
#     def move(self, *args):
#         debug.fmsg("VoxelSelectionOp base class")

# @genericselectionop.register
# class PointNEW(VoxelSelectionOp):
#     sources = ('Microstructure', 'Image')
#     mouseBehavior = genericselectionop.MouseBehavior('SingleClick')
#     tip = "Select a single voxel."
#     order = 0
#     # def select(self, ms, operator, point):
#     #     operator.operate(ms.getSelectionContext(),
#     #                      pixelselectioncourier.PointSelection(ms, point))
#     def up(self, x, y, button, ctrl, shift, gfxwindow):
#         view = gfxwindow.getView()
#         # TODO: Use self.sources and gfxwindow to get the top relevant
#         # layer.
#         # Get boolean operation from shift/ctrl.
#         pt = gfxwindow.findClickedCellCenter(immidge, (x, y), view)
#         menuitem(courier(pt), booleanoperator)

#=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=##=--=#

class SelectBox(VoxelSelectionOp):
    def select(self):
        pass

boxreg = VoxelSelectionRegistration(
    'BoxNEW',
    SelectBox,
    ordering=1,
    sources=('Microstructure', 'Image'),
    widgetType=voxelregionselectiondisplay.VoxelRegionSelectionDisplay,
    mouseBehavior=genericselectionop.MouseBehavior('MultiDrag'),
    tip="Select a rectangular box of voxels.",
    instructions = """\
Press the Start button, and then click and drag the
sides of the blue box on the canvas.  Voxels inside
the box will be selected when you press the Done button."""
)
        
# @genericselectionop.register
# class BoxNEW(VoxelSelectionOp):
#     sources = ('Microstructure', 'Image')
#     mouseBehavior = genericselectionop.MouseBehavior('MultiDrag')
#     tip = "Select a rectangular box of voxels."
#     order = 1
#     widgetType = voxelregionselectiondisplay.VoxelRegionSelectionDisplay
#     instructions = """\
# Press the Start button, and then click and drag the
# sides of the blue box on the canvas.  Voxels inside
# the box will be selected when you press the Done button."""
#     # def select(self, ms, operator, point0, point1):
#     #     operator.operate(ms.getSelectionContext(),
#     #                      pixelselectioncourier.BoxSelection(ms, point0, point1))


# ## This should be in the image subdirectory
# ## importing burn is temporary
# from ooflib.SWIG.image.burn import *
# @genericselectionop.register
# class ColorNEW(VoxelSelectionOp):
#     sources = ("Image",)
#     mouseBehavior = genericselectionop.MouseBehavior('SingleClick')
#     params = [colordiffparameter.ColorDifferenceParameter(
#         'range', tip='Acceptable deviation from the reference color.')]
#     tip = "Select similarly colored voxels."
#     order = 2
    
# @genericselectionop.register
# class BurnNEW(VoxelSelectionOp):
#     sources = ("Image",)
#     mouseBehavior = genericselectionop.MouseBehavior('SingleClick')
#     params = [
#         parameter.FloatRangeParameter(
#             'local_flammability',
#             range=(0, 1, 0.001), value=0.1,
#             tip=("Maximum difference in neighboring pixel values across which"
#                  " a burn will extend.")),
#         parameter.FloatRangeParameter(
#             'global_flammability',
#             range=(0, 1, 0.001), value=0.2,
#             tip=("Difference from initial pixel value beyond which a burn"
#                  " will not spread.")),
#         enum.EnumParameter(
#             'color_space_norm', ColorNorm, value=L1,
#             tip=("How to compute the difference between two colors"
#                  " in RGB space.")),
#         parameter.BooleanParameter(
#             'next_nearest', value=0, tip="Burn next-nearest neighbors?")
#     ]
#     tip = "Select contiguous similar voxels."
#     order = 3
