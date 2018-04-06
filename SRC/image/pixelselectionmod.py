# -*- python -*-

# This software was produced by NIST, an agency of the U.S. government,
# and by statute is not subject to copyright in the United States.
# Recipients of this software assume all responsibilities associated
# with its operation, modification and maintenance. However, to
# facilitate maintenance we ask that before distributing modified
# versions of this software, you first contact the authors at
# oof_manager@nist.gov. 

## Pixel selection modifiers make selections without mouse input.

from ooflib.SWIG.image import pixelselectioncourieri
from ooflib.common import color
from ooflib.common import pixelselection
from ooflib.common import registeredclass
from ooflib.common.IO import colordiffparameter
from ooflib.common.IO import parameter
from ooflib.common.IO import whoville

# TODO: Add operatorParam

class ColorRange(pixelselection.VoxelSelectionModifier):
    def __init__(self, image, reference, range):
        self.image = image
        self.reference = reference
        self.range = range
    def select(self, ms, selection):
        curselection = selection.getObject()
        # 'cause my teeth are perly...
        image = whoville.getClass('Image')[self.image]
        imageobj = image.getObject()
        ms = image.getMicrostructure()
        selection.clearAndSelect(
            pixelselectioncourieri.ColorSelection(ms, imageobj,
                                                  self.reference, self.range))

pixelselection.VoxelSelectionModRegistration(
    'Color Range',
    ColorRange,
    ordering=3.14,
    params=[whoville.WhoParameter('image', whoville.getClass('Image'),
                                  tip=parameter.emptyTipString),
            color.NewColorParameter('reference', tip='Reference color.'),
            colordiffparameter.ColorDifferenceParameter('range',
                                 tip='Deviation from the reference color.')
            ],
    tip="Select all pixels similar to a reference color.",
    discussion= """<para>

    Select all pixels in an &image; within a given
    <varname>range</varname> of a given <varname>refererence</varname>
    color.  This command basically does the same thing that <xref
    linkend='MenuItem:OOF.Graphics_n.Toolbox.Pixel_Select.Color'/>
    does except the latter takes its <varname>reference</varname>
    input from a mouse click in the Graphics window.

    </para>""")
