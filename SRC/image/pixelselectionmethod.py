# -*- python -*-
# $RCSfile: pixelselectionmethod.py,v $
# $Revision: 1.8.18.8 $
# $Author: langer $
# $Date: 2014/11/05 16:55:02 $

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov.

from ooflib.SWIG.common import config
from ooflib.SWIG.common.IO import vtkutils
from ooflib.SWIG.image import pixelselectioncourieri
from ooflib.common import debug
from ooflib.common import pixelselectionmethod
from ooflib.common import primitives
from ooflib.common.IO import colordiffparameter
from ooflib.common.IO import xmlmenudump

class ColorSelector(pixelselectionmethod.SelectionMethod):
    def __init__(self, range):
        self.range = range
    def select(self, immidge, gfxwindow, pointlist, view, selector):
        ms = immidge.getMicrostructure()
        if config.dimension() == 2:
            isize = ms.sizeInPixels()
            psize = primitives.Point(*ms.sizeOfPixels())
            pt = ms.pixelFromPoint(pointlist[0])
        else:                   # 3D
            cell = gfxwindow.findClickedCell(immidge, pointlist[0], view)
            if cell is not None:
                coord = vtkutils.cell2coord(cell)
                pt = ms.pixelFromPoint(coord)
            else:
                return
        pic = immidge.getObject()
        pic.update() 
        ref_color = pic[pt]
        selector(pixelselectioncourieri.ColorSelection(ms, pic, ref_color,
                                                       self.range))

pixelselectionmethod.PixelSelectionRegistration(
    'Color',
    ColorSelector,
    ordering=0.6,
    events=['up'],
    params=[colordiffparameter.ColorDifferenceParameter('range',
                                                        tip='Acceptable deviation from the reference color.')],
    whoclasses=['Image'],
    tip="Select pixels whose color is close to that of a reference pixel.",
    discussion=xmlmenudump.loadFile('DISCUSSIONS/image/reg/colorselect.xml')
    )

