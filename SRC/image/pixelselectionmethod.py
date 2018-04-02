# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

# See NOTES/selection_machinery.txt

from ooflib.SWIG.common import config
from ooflib.SWIG.common.IO import vtkutils
from ooflib.SWIG.image import pixelselectioncourieri
from ooflib.common import debug
from ooflib.common import pixelselectionmethod
from ooflib.common.IO import colordiffparameter
from ooflib.common.IO import pointparameter
from ooflib.common.IO import xmlmenudump

class ColorSelector(pixelselectionmethod.VoxelSelectionMethod):
    def __init__(self, point, range):
        self.point = point
        self.range = range
    def select(self, source, selection, operator):
        ms = source.getMicrostructure()
        pt = ms.pixelFromPoint(self.point)
        image = source.getObject() # OOFImage3D
        ref_color = image[pt]
        operator.operate(
            selection,
            pixelselectioncourieri.ColorSelection(ms, image,
                                                  ref_color, self.range))

pixelselectionmethod.VoxelSelectionRegistration(
    'Color',
    ColorSelector,
    ordering=0.6,
    events=['up'],
    params=[
        pointparameter.PointParameter('point'),
        colordiffparameter.ColorDifferenceParameter(
        'range', tip='Acceptable deviation from the reference color.')],
    whoclasses=['Image'],
    tip="""\
Select voxels whose color is close
to that of a selected reference voxel.
Click to select just the target voxels.
Shift click to retain previously selected voxels.
Control click to toggle the target voxels.
Shift-control click to deselect the target voxels.""",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/image/reg/colorselect.xml')
    )

