# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

from ooflib.SWIG.common import config
from ooflib.SWIG.common.IO import canvaslayers
from ooflib.common import color
from ooflib.common import debug
from ooflib.common import enum
from ooflib.common.IO import display
from ooflib.common.IO import parameter
from ooflib.common import registeredclass

## TODO: When a VoxelSetBdyDisplay is visible, why aren't voxels
## selectable in an ImageDisplay?

class VoxelSetBdyDisplay(display.DisplayMethod):
    def __init__(self, category, color, line_width):
        self.category = category
        self.color = color
        self.line_width = line_width
        display.DisplayMethod.__init__(self)

    def newLayer(self):
        return canvaslayers.LineSegmentLayer(self.gfxwindow.oofcanvas,
                                             "VoxelSetBdy")
    def setParams(self):
        self.canvaslayer.set_color(self.color)
        self.canvaslayer.set_lineWidth(self.line_width)
        ms = self.who().getObject(self.gfxwindow)
        if ms:
            ms.drawVoxelSetBoundary(self.canvaslayer, self.category)
    def whoChanged(self):
        return True             # call setParams

if debug.debug:        
    registeredclass.Registration(
        "VoxelSetBdy",
        display.DisplayMethod,
        VoxelSetBdyDisplay,
        ordering=1000,
        layerordering=display.Linear,
        params=[
            parameter.IntParameter("category", 0),
            color.ColorParameter('color', color.RGBColor(0, 0.7, 0.3)),
            parameter.IntRangeParameter('line_width', (1, 10), 4)
        ],
        whoclasses = ('Microstructure',),
        tip="Display boundary loops of voxel categories"
    )

# class Normal(enum.EnumClass("Positive", "Negative", "Any")):
#     pass

# class Direction(enum.EnumClass("X", "Y", "Z", "All")):
#     pass

# dirDict = {Direction("X") : 0,
#            Direction("Y") : 1,
#            Direction("Z") : 2,
#            Direction("All") : -1}

# nrmlDict = {Normal("Positive") : 1,
#             Normal("Negative") : -1,
#             Normal("Any") : 0}

# class VoxelSetBdyDisplay(display.DisplayMethod):
#     def __init__(self, category, direction, offset, normal,
#                  cross_section, color, line_width):
#         self.category = category
#         self.direction = direction
#         self.offset = offset
#         self.normal = normal
#         self.cross_section = cross_section
#         self.color = color
#         self.line_width = line_width
#         display.DisplayMethod.__init__(self)

#     def newLayer(self):
#         return canvaslayers.LineSegmentLayer(self.gfxwindow.oofcanvas,
#                                              "VoxelSetBdy")
#     def setParams(self):
#         self.canvaslayer.set_color(self.color)
#         self.canvaslayer.set_lineWidth(self.line_width)
#         ms = self.who().getObject(self.gfxwindow)
#         if ms:
#             if not self.cross_section:
#                 ms.drawVoxelSetBoundaryLoops(self.canvaslayer, self.category,
#                                              dirDict[self.direction],
#                                              self.offset, nrmlDict[self.normal])
#             else:
#                 ms.drawVoxelSetCrossSection(self.canvaslayer, self.category,
#                                             dirDict[self.direction],
#                                             self.offset, nrmlDict[self.normal])
#     def whoChanged(self):
#         return True             # call setParams

# if debug.debug:        
#     registeredclass.Registration(
#         "VoxelSetBdy",
#         display.DisplayMethod,
#         VoxelSetBdyDisplay,
#         ordering=1000,
#         layerordering=display.Linear,
#         params=[
#             parameter.IntParameter("category", 0),
#             enum.EnumParameter('direction', Direction, "All"),
#             parameter.IntParameter("offset", 0),
#             enum.EnumParameter("normal", Normal, "Positive"),
#             parameter.BooleanParameter('cross_section', False),
#             color.ColorParameter('color', color.RGBColor(0, 0.7, 0.3)),
#             parameter.IntRangeParameter('line_width', (1, 10), 4)
#         ],
#         whoclasses = ('Microstructure',),
#         tip="Display boundary loops of voxel categories"
#     )
